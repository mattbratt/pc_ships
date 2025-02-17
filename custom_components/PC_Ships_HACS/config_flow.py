import voluptuous as vol
import logging

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    # We still import these from const.py as needed:
    CONF_TRACK_STATUSES,
    CONF_UPDATE_INTERVAL_MINUTES,
    CONF_VESSEL_CLASSES,
    CONF_SENSOR_COUNT_IN_PORT,
    CONF_SENSOR_COUNT_CONFIRMED,
    CONF_SENSOR_COUNT_SCHEDULED,
    CONF_SENSOR_COUNT_DEPARTED,
    VALID_STATUSES,
    DEFAULT_STATUSES,
    VALID_VESSEL_CLASSES,
    DEFAULT_VESSEL_CLASSES,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_SENSOR_COUNT,
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
            # Create a config entry with minimal or empty data,
            # putting user-editable settings in 'options'.
            return self.async_create_entry(
                title="Port Canaveral Ships",
                data={},  # Or store only a unique_id/credentials if relevant
                options={
                    CONF_VESSEL_CLASSES: user_input.get("Vessel Class", DEFAULT_VESSEL_CLASSES),
                    CONF_TRACK_STATUSES: user_input.get("Status/es to Track", DEFAULT_STATUSES),
                    CONF_UPDATE_INTERVAL_MINUTES: user_input.get("Refresh Interval (minutes)", DEFAULT_UPDATE_INTERVAL),
                    CONF_SENSOR_COUNT_IN_PORT: user_input.get("Sensors for In Port", DEFAULT_SENSOR_COUNT),
                    CONF_SENSOR_COUNT_CONFIRMED: user_input.get("Sensors for Confirmed", DEFAULT_SENSOR_COUNT),
                    CONF_SENSOR_COUNT_SCHEDULED: user_input.get("Sensors for Scheduled", DEFAULT_SENSOR_COUNT),
                    CONF_SENSOR_COUNT_DEPARTED: user_input.get("Sensors for Departed", DEFAULT_SENSOR_COUNT),
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
            vol.Optional("Sensors for In Port", default=DEFAULT_SENSOR_COUNT):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Confirmed", default=DEFAULT_SENSOR_COUNT):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Scheduled", default=DEFAULT_SENSOR_COUNT):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Departed", default=DEFAULT_SENSOR_COUNT):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
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
            # Update the config entry options, ignoring data
            return self.async_create_entry(
                title="",
                data={},  # data stays empty; we store everything in options
                options={
                    CONF_VESSEL_CLASSES: user_input.get("Vessel Class"),
                    CONF_TRACK_STATUSES: user_input.get("Status/es to Track"),
                    CONF_UPDATE_INTERVAL_MINUTES: user_input.get("Refresh Interval (minutes)"),
                    CONF_SENSOR_COUNT_IN_PORT: user_input.get("Sensors for In Port"),
                    CONF_SENSOR_COUNT_CONFIRMED: user_input.get("Sensors for Confirmed"),
                    CONF_SENSOR_COUNT_SCHEDULED: user_input.get("Sensors for Scheduled"),
                    CONF_SENSOR_COUNT_DEPARTED: user_input.get("Sensors for Departed"),
                }
            )

        # Grab current settings from entry.options (or fallback to defaults)
        current_vessel_classes = self.config_entry.options.get(CONF_VESSEL_CLASSES, DEFAULT_VESSEL_CLASSES)
        current_track_statuses = self.config_entry.options.get(CONF_TRACK_STATUSES, DEFAULT_STATUSES)
        current_update_interval = self.config_entry.options.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL)
        current_sensor_in_port = self.config_entry.options.get(CONF_SENSOR_COUNT_IN_PORT, DEFAULT_SENSOR_COUNT)
        current_sensor_confirmed = self.config_entry.options.get(CONF_SENSOR_COUNT_CONFIRMED, DEFAULT_SENSOR_COUNT)
        current_sensor_scheduled = self.config_entry.options.get(CONF_SENSOR_COUNT_SCHEDULED, DEFAULT_SENSOR_COUNT)
        current_sensor_departed = self.config_entry.options.get(CONF_SENSOR_COUNT_DEPARTED, DEFAULT_SENSOR_COUNT)

        data_schema = vol.Schema({
            vol.Optional("Vessel Class", default=current_vessel_classes): cv.multi_select(VALID_VESSEL_CLASSES),
            vol.Optional("Status/es to Track", default=current_track_statuses): cv.multi_select(VALID_STATUSES),
            vol.Optional("Refresh Interval (minutes)", default=current_update_interval):
                vol.All(vol.Coerce(int), vol.Range(min=15)),
            vol.Optional("Sensors for In Port", default=current_sensor_in_port):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Confirmed", default=current_sensor_confirmed):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Scheduled", default=current_sensor_scheduled):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional("Sensors for Departed", default=current_sensor_departed):
                vol.All(vol.Coerce(int), vol.Range(min=1)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=self._errors,
        )
