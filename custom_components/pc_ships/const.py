DOMAIN = "port_canaveral_ships"

CONF_TRACK_STATUSES = "track_statuses"
CONF_UPDATE_INTERVAL_MINUTES = "update_interval_minutes"
CONF_VESSEL_CLASSES = "vessel_classes"

# New keys for sensor counts per status
CONF_SENSOR_COUNT_IN_PORT = "sensor_count_in_port"
CONF_SENSOR_COUNT_CONFIRMED = "sensor_count_confirmed"
CONF_SENSOR_COUNT_SCHEDULED = "sensor_count_scheduled"
CONF_SENSOR_COUNT_DEPARTED = "sensor_count_departed"

VALID_STATUSES = ["In Port", "Confirmed", "Scheduled", "Departed"]
DEFAULT_STATUSES = ["In Port", "Confirmed"]

VALID_VESSEL_CLASSES = ["Passenger", "Cargo"]  # "Cruise" changed to "Passenger"
DEFAULT_VESSEL_CLASSES = ["Passenger", "Cargo"]

DEFAULT_UPDATE_INTERVAL = 20  # minutes

DEFAULT_SENSOR_COUNT = 15
