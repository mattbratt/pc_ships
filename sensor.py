import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def format_epoch_as_date_time(epoch):
    """
    Given a UNIX timestamp, return (date_str, time_str) in the forms:
      - date_str: MM/DD/YYYY
      - time_str: HH:MM (24-hour)
    If epoch is None, return placeholders.
    """
    if epoch is None:
        return ("??/??/????", "??:??")

    dt = datetime.utcfromtimestamp(epoch)
    date_str = dt.strftime("%m/%d/%Y")  # e.g. "02/02/2025"
    time_str = dt.strftime("%H:%M")     # e.g. "16:15"
    return (date_str, time_str)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """
    Set up sensor entities based on a config entry.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]

    count_sensor = PortCanaveralShipCountSensor(coordinator, entry)
    formatted_sensor = PortCanaveralShipFormattedSensor(coordinator, entry)

    async_add_entities([count_sensor, formatted_sensor], True)


class PortCanaveralShipCountSensor(CoordinatorEntity, SensorEntity):
    """Sensor that shows how many ships match the chosen statuses."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Port Canaveral Ships Count"
        self._attr_unique_id = f"{entry.entry_id}-count"
        self._attr_icon = "mdi:ship-wheel"

    @property
    def state(self):
        data = self.coordinator.data
        return len(data) if data else 0

    @property
    def extra_state_attributes(self):
        # Return the coordinator data as well as last_checked. 
        return {
            "filtered_schedule": self.coordinator.data,
            "last_checked": datetime.now().isoformat()  # Add last checked timestamp
        }


class PortCanaveralShipFormattedSensor(CoordinatorEntity, SensorEntity):
    """Sensor that provides a multi-line formatted schedule in an attribute."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Port Canaveral Ships Formatted"
        self._attr_unique_id = f"{entry.entry_id}-formatted"
        self._attr_icon = "mdi:ship-wheel"

    @property
    def state(self):
        return "See 'formatted_schedule' attribute"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data:
            return {
                "formatted_schedule": "No data.",
                "last_checked": datetime.now().isoformat()  # Add last checked timestamp
            }

        lines = []
        for ship in data:
            vessel = ship.get("Vessel", "")
            status = ship.get("Status", "")
            cargo_type = ship.get("Cargo Type", "")
            flag = ship.get("Flag", "")
            berth = ship.get("Arrival Berth", ship.get("Berth", ""))

            arrival_date_str, arrival_time_str = format_epoch_as_date_time(ship.get("arrival_epoch"))
            departure_date_str, departure_time_str = format_epoch_as_date_time(ship.get("departure_epoch"))

            lines.append(
                f"Vessel: {vessel}\n"
                f"Status: {status}\n"
                f"Flag: {flag}\n"
                f"Berth: {berth}\n"
                f"Arrival Date: {arrival_date_str}\n"
                f"Arrival Time: {arrival_time_str}\n"
                f"Departure Date: {departure_date_str}\n"
                f"Departure Time: {departure_time_str}\n"
                f"Cargo Type: {cargo_type}\n"
            )

        # Combine the lines into a single multi-line string
        return {
            "formatted_schedule": "\n".join(lines),
            "last_checked": datetime.now().isoformat()  # Add last checked timestamp
        }
