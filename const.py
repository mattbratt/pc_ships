DOMAIN = "port_canaveral_ships"

CONF_TRACK_STATUSES = "track_statuses"
CONF_UPDATE_INTERVAL_MINUTES = "update_interval_minutes"
CONF_VESSEL_CLASSES = "vessel_classes"

VALID_STATUSES = ["In Port", "Confirmed", "Scheduled", "Departed"]
DEFAULT_STATUSES = ["In Port", "Confirmed"]

VALID_VESSEL_CLASSES = ["Passenger", "Cargo"]  # ✅ "Cruise" changed to "Passenger"
DEFAULT_VESSEL_CLASSES = ["Passenger", "Cargo"]

DEFAULT_UPDATE_INTERVAL = 20  # Minimum of 15 enforced in config flow
