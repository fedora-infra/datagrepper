config = {
    # We don't really want to *run* datanommer, but we do want
    # access to its DB.
    'datanommer.enabled': False,
    # This is generally not safe.. you probably want to use a real DB.
    'datanommer.sqlalchemy.url': 'sqlite:////tmp/datanommer.db',
    # Enable this to enable the datagrepper job runner.
    'fedmsg.consumers.datagrepper-runner.enabled': True,

    # For production
    #'fedmenu_url': 'https://apps.fedoraproject.org/fedmenu',
    #'fedmenu_data_url': 'https://apps.fedoraproject.org/js/data.js',

    # For development
    #'fedmenu_url': 'http://threebean.org/fedmenu',
    #'fedmenu_data_url': 'http://threebean.org/fedmenu/dev-data.js',

    #'websocket_address': 'wss://hub.fedoraproject.org:9939',

    #'content_security_policy': 'connect-src https://*.fedoraproject.org wss://*.fedoraproject.org'

    #'datagrepper_logo': 'static/datagrepper.png',
    #'theme_css_url': 'https://apps.fedoraproject.org/global/fedora-bootstrap-1.0/fedora-bootstrap.min.css',
    #'message_bus_link': 'http://fedmsg.com',
    #'message_bus_shortname': 'fedmsg',
    #'message_bus_longname': 'fedmsg bus',
}
