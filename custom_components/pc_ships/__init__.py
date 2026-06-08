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
_DASHBOARDS_STORAGE_KEY = "lovelace_dashboards"


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

    hass.async_create_task(_async_create_dashboard(hass))

    return True


async def _async_create_dashboard(hass: HomeAssistant) -> None:
    """Write the PC Ships dashboard to HA storage if it doesn't already exist.

    The dashboard appears in the sidebar after the next HA restart (one-time only).
    It is never overwritten or removed on unload, preserving any user customisations.
    """
    # Check if already registered in persistent storage — avoids a restart loop
    dashboards_store = Store(hass, 1, _DASHBOARDS_STORAGE_KEY)
    registry = await dashboards_store.async_load() or {}
    items = registry.get("items", [])

    if any(item.get("url_path") == _DASHBOARD_URL_PATH for item in items):
        _LOGGER.debug("PC Ships dashboard already registered in storage")
        return

    # Load the bundled default config
    config_file = Path(__file__).parent / "pc_ships_default.yaml"

    def _load_yaml():
        with open(config_file, encoding="utf-8") as f:
            return yaml.safe_load(f)

    config = await hass.async_add_executor_job(_load_yaml)

    # Write the dashboard config
    config_store = Store(hass, 1, f"lovelace.{_DASHBOARD_URL_PATH}")
    await config_store.async_save({"config": config})

    # Register the dashboard in the lovelace dashboards registry
    items.append({
        "id": _DASHBOARD_URL_PATH,
        "url_path": _DASHBOARD_URL_PATH,
        "title": "PC Ships",
        "icon": "mdi:ferry",
        "show_in_sidebar": True,
        "require_admin": False,
        "mode": "storage",
    })
    registry["items"] = items
    await dashboards_store.async_save(registry)

    _LOGGER.warning(
        "PC Ships dashboard registered. Restart Home Assistant once for it to appear in the sidebar."
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry. The dashboard is left intact for the user."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
