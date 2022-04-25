APP_PATH = "https://apps.fedoraproject.org/datagrepper"
CORS_DOMAINS = [".*"]
CORS_METHODS = ["GET", "OPTIONS"]
CORS_HEADERS = [".*"]
CORS_MAX_AGE = "600"
DEFAULT_QUERY_DELTA = 0
DATANOMMER_SQLALCHEMY_URL = "postgresql://datanommer:datanommer@localhost/messages"
DATAGREPPER_APPROXIMATE_COUNT = True
BUS_INFO = {
    "link": "https://fedora-messaging.readthedocs.io",
    "shortname": "Fedora Messaging",
    "longname": "Fedora Messaging bus",
    "docs": "https://fedora-messaging.readthedocs.io",
}
THEME_CSS_URL = (
    "https://apps.fedoraproject.org/global/fedora-bootstrap-1.0/"
    "fedora-bootstrap.min.css"
)

# Example: "wss://hub.fedoraproject.org:9939"
WEBSOCKET_URL = None
# Only allow websockets connections to fedoraproject.org, for instance:
# "connect-src https://*.fedoraproject.org wss://*.fedoraproject.org"
CONTENT_SECURITY_POLICY = None

HEALTHZ = {
    "live": "datagrepper.app.liveness",
    "ready": "datagrepper.app.readiness",
}
