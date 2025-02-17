"""Initialize the Port Canaveral Ships integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

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


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up Port Canaveral Ships from a config entry (UI-based).
    This is called when the user adds or updates the integration in the UI.
    """
    # For user-editable settings, read from entry.options, fallback to defaults
    track_statuses = entry.options.get(CONF_TRACK_STATUSES, DEFAULT_STATUSES)
    update_interval_minutes = entry.options.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL)
    vessel_classes = entry.options.get(CONF_VESSEL_CLASSES, DEFAULT_VESSEL_CLASSES)

    # Create the coordinator (polling logic)
    coordinator = PortCanaveralShipsCoordinator(
        hass,
        track_statuses=track_statuses,
        vessel_classes=vessel_classes,
        update_interval=timedelta(minutes=update_interval_minutes),
    )

    # Store the coordinator in hass.data so we can access it from sensor.py
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Initialize the coordinator (fetch initial data)
    await coordinator.async_config_entry_first_refresh()

    # Forward the entry to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
