config = {
    # We don't really want to *run* datanommer, but we do want
    # access to its DB.
    'datanommer.enabled': False,
    # This is generally not safe.. you probably want to use a real DB.
    'datanommer.sqlalchemy.url': 'postgres://datanommer:bunbunbun@localhost/datanommer',
    # Enable this to enable the datagrepper job runner.
    'fedmsg.consumers.datagrepper-runner.enabled': True,
}
