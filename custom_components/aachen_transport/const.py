from datetime import timedelta

DOMAIN = "aachen_transport"
SCAN_INTERVAL = timedelta(seconds=60)
API_ENDPOINT = "https://abfahrt.avv.de/index.php?fw_goto=Preview/build&id="

DEFAULT_ICON = "mdi:clock"

CONF_DEPARTURES = "departures"
CONF_DEPARTURES_NAME = "name"
CONF_DEPARTURES_STOP_ID = "stop_id"
CONF_DEPARTURES_WALKING_TIME = "walking_time"
CONF_DEPARTURES_TRACK = "track"
CONF_TYPE_SUBURBAN = "suburban"
CONF_TYPE_SUBWAY = "subway"
CONF_TYPE_TRAM = "tram"
CONF_TYPE_BUS = "BUS"
CONF_TYPE_FERRY = "ferry"
CONF_TYPE_TRAIN = "RAILWAY"

TRANSPORT_TYPE_VISUALS = {
    CONF_TYPE_SUBURBAN: {
        "code": "S",
        "icon": "mdi:subway-variant",
        "color": "#008D4F",
    },
    CONF_TYPE_SUBWAY: {
        "code": "U",
        "icon": "mdi:subway",
        "color": "#2864A6",
    },
    CONF_TYPE_TRAM: {
        "code": "M",
        "icon": "mdi:tram",
        "color": "#D82020",
    },
    CONF_TYPE_BUS: {
        "code": "BUS",
        "icon": "mdi:bus",
        "color": "#A5027D"
    },
    CONF_TYPE_FERRY: {
        "code": "F",
        "icon": "mdi:ferry",
        "color": "#0080BA"
    },
    CONF_TYPE_TRAIN: {
        "code": "TRAIN",
        "icon": "mdi:train",
        "color": "#F01414"
    }
}
