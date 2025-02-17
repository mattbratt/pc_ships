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
)
from .coordinator import PortCanaveralShipsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up Port Canaveral Ships from a config entry (UI-based).
    This is called when the user adds or updates the integration in the UI.
    """
    # Extract config/option data from the config entry
    track_statuses = entry.data.get(CONF_TRACK_STATUSES)
    update_interval_minutes = entry.data.get(CONF_UPDATE_INTERVAL_MINUTES)
    vessel_classes = entry.data.get(CONF_VESSEL_CLASSES)

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
