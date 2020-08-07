import unittest
import datetime


from nose.tools import eq_
from freezegun import freeze_time

from datagrepper.util import assemble_timerange

utc = datetime.timezone.utc


class TestTimerange(unittest.TestCase):

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_none_none(self):
        start, end, delta = assemble_timerange(None, None, None)
        eq_(None, start)
        eq_(None, end)
        eq_(None, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_none_none(self):
        start, end, delta = assemble_timerange(None, None, 5)
        eq_(1325375995.0, start)
        eq_(1325376000.0, end)
        eq_(5, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_start_none(self):
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=700)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, None, None)
        eq_(1325375300.0, start)
        eq_(1325376000.0, end)
        eq_(700, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_start_none(self):
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, None, 5)
        eq_(1325375400.0, start)
        eq_(1325375405.0, end)
        eq_(5, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_none_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start, end, delta = assemble_timerange(None, end, None)
        eq_(1325374800.0, start)
        eq_(1325375400.0, end)
        eq_(600, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_none_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start, end, delta = assemble_timerange(None, end, 5)
        eq_(1325375395.0, start)
        eq_(1325375400.0, end)
        eq_(5, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_none_start_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=800)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, end, None)
        eq_(1325375200.0, start)
        eq_(1325375400.0, end)
        eq_(200, delta)

    @freeze_time(datetime.datetime.fromtimestamp(1325376000, tz=utc))
    def test_delta_start_end(self):
        end = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
        end = datetime.datetime.timestamp(end)
        start = datetime.datetime.utcnow() - datetime.timedelta(seconds=800)
        start = datetime.datetime.timestamp(start)
        start, end, delta = assemble_timerange(start, end, 5)
        eq_(1325375200.0, start)
        eq_(1325375400.0, end)
        eq_(200, delta)
