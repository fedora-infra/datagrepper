import unittest
import datetime


from freezegun import freeze_time

from datagrepper.util import assemble_timerange

utc = datetime.timezone.utc


class TestTimerange(unittest.TestCase):

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_none_none(self):
        start, end, delta = assemble_timerange(None, None, None)
        assert start is None
        assert end is None
        assert delta is None

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_none_none(self):
        start, end, delta = assemble_timerange(None, None, 5)
        assert 1325375995.0 == start
        assert 1325376000.0 == end
        assert 5 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_start_none(self):
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=700)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, None, None)
        assert 1325375300.0 == start
        assert 1325376000.0 == end
        assert 700 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_start_none(self):
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, None, 5)
        assert 1325375400.0 == start
        assert 1325375405.0 == end
        assert 5 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_none_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start, end, delta = assemble_timerange(None, end, None)
        assert 1325374800.0 == start
        assert 1325375400.0 == end
        assert 600 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_none_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start, end, delta = assemble_timerange(None, end, 5)
        assert 1325375395.0 == start
        assert 1325375400.0 == end
        assert 5 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_start_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=800)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, end, None)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_start_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=800)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, end, 5)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta
