"""Config flow for Port Canaveral Ships integration."""
import voluptuous as vol
import logging

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_TRACK_STATUSES,
    CONF_UPDATE_INTERVAL_MINUTES,
    CONF_VESSEL_CLASSES,
    VALID_STATUSES,
    DEFAULT_STATUSES,
    VALID_VESSEL_CLASSES,
    DEFAULT_VESSEL_CLASSES,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class PortCanaveralShipsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Port Canaveral Ships."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """
        Initial step when the user first sets up this integration.
        """
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Port Canaveral Ships",
                data={
                    CONF_VESSEL_CLASSES: user_input.get("Vessel Class", DEFAULT_VESSEL_CLASSES),
                    CONF_TRACK_STATUSES: user_input.get("Status/es to Track", DEFAULT_STATUSES),
                    CONF_UPDATE_INTERVAL_MINUTES: user_input.get("Refresh Interval (minutes)", DEFAULT_UPDATE_INTERVAL),
                }
            )

        return await self._show_user_form()

    async def _show_user_form(self):
        """
        Show the form for user input.
        """
        data_schema = vol.Schema({
            vol.Optional("Vessel Class", default=DEFAULT_VESSEL_CLASSES): cv.multi_select(VALID_VESSEL_CLASSES),
            vol.Optional("Status/es to Track", default=DEFAULT_STATUSES): cv.multi_select(VALID_STATUSES),
            vol.Optional("Refresh Interval (minutes)", default=DEFAULT_UPDATE_INTERVAL):
                vol.All(vol.Coerce(int), vol.Range(min=15)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Tell HA how to get an Options Flow for this entry."""
        return PortCanaveralShipsOptionsFlow(config_entry)


class PortCanaveralShipsOptionsFlow(config_entries.OptionsFlow):
    """Options flow to adjust settings after initial setup."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Store the config entry so we can modify it."""
        self.config_entry = config_entry
        self._errors = {}

    async def async_step_init(self, user_input=None):
        """
        The Options step the user sees when clicking "Configure" on the integration.
        """
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_VESSEL_CLASSES: user_input.get("Vessel Class"),
                    CONF_TRACK_STATUSES: user_input.get("Status/es to Track"),
                    CONF_UPDATE_INTERVAL_MINUTES: user_input.get("Refresh Interval (minutes)"),
                }
            )

        # Get current settings
        current_vessel_classes = self.config_entry.data.get(CONF_VESSEL_CLASSES, DEFAULT_VESSEL_CLASSES)
        current_track_statuses = self.config_entry.data.get(CONF_TRACK_STATUSES, DEFAULT_STATUSES)
        current_update_interval = self.config_entry.data.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL)

        data_schema = vol.Schema({
            vol.Optional("Vessel Class", default=current_vessel_classes): cv.multi_select(VALID_VESSEL_CLASSES),
            vol.Optional("Status/es to Track", default=current_track_statuses): cv.multi_select(VALID_STATUSES),
            vol.Optional("Refresh Interval (minutes)", default=current_update_interval):
                vol.All(vol.Coerce(int), vol.Range(min=15)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=self._errors,
        )
