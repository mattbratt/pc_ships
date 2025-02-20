import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_TRACK_STATUSES,
    CONF_SENSOR_COUNT_IN_PORT,
    CONF_SENSOR_COUNT_CONFIRMED,
    CONF_SENSOR_COUNT_SCHEDULED,
    CONF_SENSOR_COUNT_DEPARTED,
    DEFAULT_SENSOR_COUNT,
)
from . import coordinator as coord_module  # or import the function(s) you need
# e.g. from .coordinator import parse_date_time_to_epoch

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
    return dt.strftime("%m/%d/%Y"), dt.strftime("%H:%M")


def get_sorted_ships_for_status(ships, status):
    """Return ships sorted according to the rules for each status."""
    if status in ("Confirmed", "Scheduled"):
        # Order by arrival time (earliest first)
        return sorted(
            ships,
            key=lambda ship: ship.get("arrival_epoch")
            if ship.get("arrival_epoch") is not None else float("inf")
        )
    elif status == "In Port":
        # Order by departure time ascending (first to depart is first)
        return sorted(
            ships,
            key=lambda ship: ship.get("departure_epoch")
            if ship.get("departure_epoch") is not None else float("inf")
        )
    elif status == "Departed":
        # Order by departure time descending (most recent first)
        return sorted(
            ships,
            key=lambda ship: ship.get("departure_epoch")
            if ship.get("departure_epoch") is not None else float("-inf"),
            reverse=True
        )
    else:
        # Fallback: arrival time ascending
        return sorted(
            ships,
            key=lambda ship: ship.get("arrival_epoch")
            if ship.get("arrival_epoch") is not None else float("inf")
        )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """
    Set up sensor entities based on a config entry.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    # Because track_statuses is now in options, we read from entry.options:
    tracked_statuses = entry.options.get(CONF_TRACK_STATUSES, [])

    # For each tracked status, get the number of sensors configured (also in options)
    for status in tracked_statuses:
        if status == "In Port":
            count = entry.options.get(CONF_SENSOR_COUNT_IN_PORT, DEFAULT_SENSOR_COUNT)
        elif status == "Confirmed":
            count = entry.options.get(CONF_SENSOR_COUNT_CONFIRMED, DEFAULT_SENSOR_COUNT)
        elif status == "Scheduled":
            count = entry.options.get(CONF_SENSOR_COUNT_SCHEDULED, DEFAULT_SENSOR_COUNT)
        elif status == "Departed":
            count = entry.options.get(CONF_SENSOR_COUNT_DEPARTED, DEFAULT_SENSOR_COUNT)
        else:
            count = 0

        for index in range(1, count + 1):
            sensors.append(
                PortCanaveralShipSensor(coordinator, entry, status, index)
            )

    async_add_entities(sensors, True)


class PortCanaveralShipSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity representing a specific ship slot for a given status."""

    def __init__(self, coordinator, entry, status: str, slot: int):
        """
        :param coordinator: The update coordinator.
        :param entry: The config entry.
        :param status: The status this sensor represents (e.g., "In Port").
        :param slot: The 1-indexed sensor number for the given status.
        """
        super().__init__(coordinator)
        self._entry = entry
        self.status_type = status
        self.slot = slot

        self._attr_name = f"Port Canaveral Ships {status} {slot}"
        self._attr_unique_id = f"{entry.entry_id}_{status.replace(' ', '_').lower()}_{slot}"
        self._attr_icon = "mdi:ship-wheel"

    @property
    def state(self):
        """Return the vessel name if available, else 'No Data'."""
        ship = self._get_ship_for_slot()
        if ship:
            return ship.get("Vessel", "Unknown")
        return "No Data"

    def _get_ship_for_slot(self):
        """Filter coordinator data for this sensor’s status and return the ship for this slot."""
        if not self.coordinator.data:
            return None

        # Filter the ships by the sensor's status
        ships = [ship for ship in self.coordinator.data if ship.get("Status") == self.status_type]
        if not ships:
            return None

        sorted_ships = get_sorted_ships_for_status(ships, self.status_type)
        # slot is 1-indexed
        if len(sorted_ships) >= self.slot:
            return sorted_ships[self.slot - 1]
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes with details about the ship assigned to this sensor slot."""
        ship = self._get_ship_for_slot()
        attributes = {
            "status_type": self.status_type,
            "sensor_slot": self.slot,
            "last_updated": datetime.now().isoformat(),
        }
        if ship:
            arrival_date, arrival_time = format_epoch_as_date_time(ship.get("arrival_epoch"))
            departure_date, departure_time = format_epoch_as_date_time(ship.get("departure_epoch"))
            attributes.update({
                "vessel": ship.get("Vessel", "Unknown"),
                "status": ship.get("Status", "Unknown"),
                "cargo_type": ship.get("Cargo Type", "Unknown"),
                "vessel_class": ship.get("Vessel Class", "Unknown"),
                "flag": ship.get("Flag", "Unknown"),
                "berth": ship.get("Arrival Berth", ship.get("Berth", "Unknown")),
                "arrival_date": arrival_date,
                "arrival_time": arrival_time,
                "departure_date": departure_date,
                "departure_time": departure_time,
                "is_tug_boat": ship.get("Is Tug Boat", False),
            })
        else:
            attributes["message"] = "No data available for this slot."
        return attributes
