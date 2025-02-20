import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

URL = (
    "https://3867087.extforms.netsuite.com/app/site/hosting/scriptlet.nl?"
    "script=1183&deploy=1&compid=3867087&ns-at=AAEJ7tMQo3zDG9o8drR5sYhZx-"
    "SzIrCmA26Jo-BI8lM707JC8Hc&type=All"
)

STATUS_ORDER = {
    "In Port": 1,
    "Confirmed": 2,
    "Scheduled": 3,
    "Departed": 4
}

def get_status_rank(status):
    """Returns the sorting order for a given status."""
    return STATUS_ORDER.get(status, 99)

def determine_vessel_class(cargo_type):
    """
    Determine vessel class based on Cargo Type.
    - If Cargo Type == "Passenger", classify as "Passenger"
    - Otherwise, classify as "Cargo"
    """
    return "Passenger" if cargo_type.strip().lower() == "passenger" else "Cargo"


def is_tug_boat(vessel_name):
    """
    Determine if a vessel is a tug boat.
    - If the vessel name starts with "TG", it is a tug boat.
    """
    return vessel_name.strip().upper().startswith("TG")

def parse_datetime(date_str, time_str):
    """Parse date and time into a sortable datetime object."""
    if not date_str or not time_str:
        return datetime.min
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
    except ValueError:
        return datetime.min

def fetch_ship_schedule():
    """Fetch and parse the ship schedule from the remote page."""
    try:
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        html = response.text
    except Exception as err:
        _LOGGER.error("Error fetching schedule: %s", err)
        return None

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="ship-schedule")
    if not table:
        _LOGGER.warning("Table not found in the fetched HTML.")
        return None

    # Extract header row
    header = []
    thead = table.find("thead")
    if thead:
        header = [th.get_text(strip=True) for th in thead.find_all("th")]
    else:
        first_row = table.find("tr")
        header = [cell.get_text(strip=True) for cell in first_row.find_all(["td", "th"])]

    schedule_data = []

    # Extract body rows
    tbody = table.find("tbody")
    if tbody:
        rows = tbody.find_all("tr")
    else:
        rows = table.find_all("tr")[1:]  # skip header if no tbody

    for row in rows:
        cells = row.find_all(["td", "th"])
        cell_values = [cell.get_text(strip=True) for cell in cells]

        # Skip legend rows
        if cell_values and "Legend:" in cell_values[0]:
            continue

        if cell_values:
            row_dict = {
                header[i]: cell_values[i]
                for i in range(min(len(header), len(cell_values)))
            }

            # Determine vessel class based on Cargo Type
            cargo_type = row_dict.get("Cargo Type", "")
            row_dict["Vessel Class"] = determine_vessel_class(cargo_type)

            # Determine if it's a tug boat
            vessel_name = row_dict.get("Vessel", "")
            row_dict["Is Tug Boat"] = is_tug_boat(vessel_name)

            schedule_data.append(row_dict)

    # Sort data by status order, then by arrival datetime ascending
    schedule_data.sort(
        key=lambda ship: (
            get_status_rank(ship.get("Status", "")),
            parse_datetime(ship.get("Arrival Date", ""), ship.get("ETA Time", ""))
        ),
        reverse=False
    )

    return schedule_data
