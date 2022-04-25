import datetime
import unittest
from unittest.mock import patch

from dateutil import tz

import datagrepper.app
from datagrepper.util import assemble_timerange, datetime_to_seconds


utc = datetime.timezone.utc


class TestTimerange(unittest.TestCase):
    ctx = datagrepper.app.app.app_context()

    def setUp(self):
        self.now = datetime.datetime.fromtimestamp(1325376000, tz=utc)
        patcher = unittest.mock.patch("datagrepper.util.datetime.datetime")
        self.addCleanup(patcher.stop)
        mock_dt = patcher.start()
        # https://docs.python.org/3/library/unittest.mock-examples.html#mock-patching-methods
        mock_dt.now.return_value = self.now
        mock_dt.fromtimestamp.side_effect = (
            lambda *args, **kw: datetime.datetime.fromtimestamp(*args, **kw)
        )
        datagrepper.app.app.testing = True
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_none_none_none(self):
        start, end, delta = assemble_timerange(None, None, None)
        assert start is None
        assert end is None
        assert delta is None

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 400})
    def test_none_none_none_with_default_delta(self):
        start, end, delta = assemble_timerange(None, None, None)
        assert 1325375600.0 == start
        assert 1325376000.0 == end
        assert 400 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_delta_none_none(self):
        start, end, delta = assemble_timerange(None, None, 5)
        assert 1325375995.0 == start
        assert 1325376000.0 == end
        assert 5 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_none_start_none(self):
        start = self.now - datetime.timedelta(seconds=700)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, None, None)
        assert 1325375300.0 == start
        assert 1325376000.0 == end
        assert 700 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_delta_start_none(self):
        start = self.now - datetime.timedelta(seconds=600)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, None, 5)
        assert 1325375400.0 == start
        assert 1325375405.0 == end
        assert 5 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 600})
    def test_none_none_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start, end, delta = assemble_timerange(None, end, None)
        assert 1325374800.0 == start
        assert 1325375400.0 == end
        assert 600 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_delta_none_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start, end, delta = assemble_timerange(None, end, 5)
        assert 1325375395.0 == start
        assert 1325375400.0 == end
        assert 5 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_none_start_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start = self.now - datetime.timedelta(seconds=800)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, end, None)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_delta_start_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start = self.now - datetime.timedelta(seconds=800)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, end, 5)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_none_start_end_parse(self):
        end = "2012-01-01T01:00:00+00:00"
        start = "2012-01-01T00:00:00+00:00"
        start, end, delta = assemble_timerange(start, end, None)
        assert 1325376000.0 == start
        assert 1325376000.0 + 3600 == end
        assert 3600 == delta

    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 0})
    def test_timedelta_to_seconds(self):
        start = datetime.datetime.now(tz.tzutc())
        time = datetime_to_seconds(start)
        assert time == 1325376000.0
