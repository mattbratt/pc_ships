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
    from homeassistant.components.frontend import async_register_built_in_panel

    lovelace = hass.data.get(LOVELACE_DOMAIN)
    if lovelace is None:
        _LOGGER.warning("Lovelace not available; skipping PC Ships dashboard creation")
        return

    dashboards = getattr(lovelace, "dashboards", None)
    if dashboards is None:
        _LOGGER.warning("Lovelace dashboards not available; skipping PC Ships dashboard creation")
        return

    # Check existence — dashboards is a dict in HA 2025.x, a collection in older HA
    if isinstance(dashboards, dict):
        if _DASHBOARD_URL_PATH in dashboards:
            _LOGGER.debug("PC Ships dashboard already exists at /%s", _DASHBOARD_URL_PATH)
            return
    elif any(item.get("url_path") == _DASHBOARD_URL_PATH for item in dashboards.async_items()):
        _LOGGER.debug("PC Ships dashboard already exists at /%s", _DASHBOARD_URL_PATH)
        return

    config_file = Path(__file__).parent / "pc_ships_default.yaml"

    def _load_yaml():
        with open(config_file, encoding="utf-8") as f:
            return yaml.safe_load(f)

    config = await hass.async_add_executor_job(_load_yaml)

    if not isinstance(dashboards, dict):
        # Older HA: use the collection API
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
    else:
        # HA 2025.x: dashboards is a plain dict — create manually
        try:
            from homeassistant.components.lovelace.dashboard import LovelaceStorage

            dashboard_meta = {
                "id": "pc_ships_default",
                "url_path": _DASHBOARD_URL_PATH,
                "title": "PC Ships",
                "icon": "mdi:ferry",
                "show_in_sidebar": True,
                "require_admin": False,
                "mode": "storage",
            }

            # Save dashboard config to HA storage
            store = Store(hass, 1, f"lovelace.{_DASHBOARD_URL_PATH}")
            await store.async_save({"config": config})

            # Add LovelaceStorage instance to the in-memory dashboards dict
            dashboards[_DASHBOARD_URL_PATH] = LovelaceStorage(hass, dashboard_meta)

            # Register the sidebar panel so it appears immediately
            async_register_built_in_panel(
                hass,
                "lovelace",
                "PC Ships",
                "mdi:ferry",
                _DASHBOARD_URL_PATH,
                {"mode": "storage"},
                require_admin=False,
                update=True,
            )

            # Persist dashboard metadata so it survives HA restart
            dashboards_store = Store(hass, 1, "lovelace_dashboards")
            registry = await dashboards_store.async_load() or {}
            items = registry.get("items", [])
            if not any(item.get("url_path") == _DASHBOARD_URL_PATH for item in items):
                items.append(dashboard_meta)
                registry["items"] = items
                await dashboards_store.async_save(registry)

        except Exception as err:
            _LOGGER.error("Failed to create PC Ships dashboard: %s", err)
            return

    _LOGGER.info("PC Ships dashboard created at /%s", _DASHBOARD_URL_PATH)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry. The dashboard is left intact for the user."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
