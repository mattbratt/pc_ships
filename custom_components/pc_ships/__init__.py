"""Initialize the Port Canaveral Ships integration."""
import logging
import yaml
from datetime import timedelta
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import (
    DOMAIN,
    CONF_TRACK_STATUSES,
    CONF_UPDATE_INTERVAL_MINUTES,
    CONF_VESSEL_CLASSES,
    DEFAULT_STATUSES,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_VESSEL_CLASSES,
)
from .coordinator import PortCanaveralShipsCoordinator

_LOGGER = logging.getLogger(__name__)

_WWW_REGISTERED = False
_DASHBOARD_URL_PATH = "pc-ships"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Port Canaveral Ships from a config entry."""
    global _WWW_REGISTERED
    if not _WWW_REGISTERED:
        www_path = Path(__file__).parent / "www"
        await hass.http.async_register_static_paths(
            [StaticPathConfig("/pc_ships", str(www_path), False)]
        )
        _WWW_REGISTERED = True
        _LOGGER.debug("Registered static path /pc_ships -> %s", www_path)

    track_statuses = entry.options.get(CONF_TRACK_STATUSES, DEFAULT_STATUSES)
    update_interval_minutes = entry.options.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL)
    vessel_classes = entry.options.get(CONF_VESSEL_CLASSES, DEFAULT_VESSEL_CLASSES)

    coordinator = PortCanaveralShipsCoordinator(
        hass,
        track_statuses=track_statuses,
        vessel_classes=vessel_classes,
        update_interval=timedelta(minutes=update_interval_minutes),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Create the dashboard asynchronously so lovelace is guaranteed ready
    hass.async_create_task(_async_create_dashboard(hass))

    return True


async def _async_create_dashboard(hass: HomeAssistant) -> None:
    """Create the PC Ships Lovelace dashboard if it doesn't already exist."""
    from homeassistant.components.lovelace import DOMAIN as LOVELACE_DOMAIN

    lovelace = hass.data.get(LOVELACE_DOMAIN)
    dashboards = getattr(lovelace, "dashboards", None)
    if dashboards is None:
        _LOGGER.warning("Lovelace dashboards not available; skipping PC Ships dashboard creation")
        return

    # Skip silently if the dashboard already exists (e.g. after a reload)
    if any(item.get("url_path") == _DASHBOARD_URL_PATH for item in dashboards.async_items()):
        _LOGGER.debug("PC Ships dashboard already exists at /%s", _DASHBOARD_URL_PATH)
        return

    config_file = Path(__file__).parent / "pc_ships_default.yaml"

    def _load_yaml():
        with open(config_file, encoding="utf-8") as f:
            return yaml.safe_load(f)

    config = await hass.async_add_executor_job(_load_yaml)

    try:
        await dashboards.async_create_item({
            "url_path": _DASHBOARD_URL_PATH,
            "icon": "mdi:ferry",
            "title": "PC Ships",
            "show_in_sidebar": True,
            "require_admin": False,
        })
    except Exception as err:
        _LOGGER.error("Failed to register PC Ships dashboard: %s", err)
        return

    store = Store(hass, 1, f"lovelace.{_DASHBOARD_URL_PATH}")
    await store.async_save({"config": config})
    _LOGGER.info("PC Ships dashboard created at /%s", _DASHBOARD_URL_PATH)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry. The dashboard is left intact for the user."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
