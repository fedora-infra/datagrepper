config = {
    # We don't really want to *run* datanommer, but we do want
    # access to its DB.
    'datanommer.enabled': False,
    # This is generally not safe.. you probably want to use a real DB.
    'datanommer.sqlalchemy.url': 'sqlite:////tmp/datanommer.db',
}
