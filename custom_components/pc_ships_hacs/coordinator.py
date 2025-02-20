import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import data_fetcher

_LOGGER = logging.getLogger(__name__)


def parse_date_time_to_epoch(date_str: str, time_str: str):
    """
    Convert 'MM/DD/YYYY' + 'HH:MM' to a UNIX timestamp (float),
    or None if parsing fails/empty.
    """
    date_str = date_str.strip()
    time_str = time_str.strip()
    if not date_str or not time_str:
        return None
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
        return dt.timestamp()  # seconds from epoch (UTC)
    except ValueError:
        _LOGGER.warning("Failed to parse date/time from '%s %s'", date_str, time_str)
        return None


class PortCanaveralShipsCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch and filter Port Canaveral Ships data."""

    def __init__(
        self,
        hass: HomeAssistant,
        track_statuses: list,
        vessel_classes: list,
        update_interval: timedelta,
    ):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="PortCanaveralShipsCoordinator",
            update_interval=update_interval,
        )
        self._track_statuses = track_statuses
        self._vessel_classes = vessel_classes

    async def _async_update_data(self):
        """
        Fetch the ship schedule, filter by chosen statuses and vessel class,
        convert date/time to UNIX timestamps.
        """
        loop = asyncio.get_event_loop()
        raw_data = await loop.run_in_executor(None, data_fetcher.fetch_ship_schedule)
        if raw_data is None:
            raise UpdateFailed("Failed to fetch or parse ship schedule.")

        # Filter by statuses
        filtered_data = [
            ship for ship in raw_data
            if ship.get("Status") in self._track_statuses
        ]

        # Filter by vessel class
        filtered_data = [
            ship for ship in filtered_data
            if ship.get("Vessel Class") in self._vessel_classes
        ]

        # Convert arrival/departure dates to epoch
        for ship in filtered_data:
            ship["arrival_epoch"] = parse_date_time_to_epoch(
                ship.get("Arrival Date", ""),
                ship.get("ETA Time", "")
            )
            ship["departure_epoch"] = parse_date_time_to_epoch(
                ship.get("Departure Date", ""),
                ship.get("ETD Time", "")
            )

        return filtered_data
