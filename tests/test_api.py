# SPDX-License-Identifier: GPL-2.0+
# Copyright 2018 Mike Bonnet <mikeb@redhat.com>

import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import datagrepper.app


class TestAPI(unittest.TestCase):
    def setUp(self):
        datagrepper.app.app.testing = True
        self.client = datagrepper.app.app.test_client()

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_reference(self, grep):
        resp = self.client.get("/reference")
        self.assertEqual(resp.status_code, 200)
        response = resp.get_data()
        self.assertIn(b"General API notes", response)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_charts(self, grep):
        resp = self.client.get("/charts")
        self.assertEqual(resp.status_code, 200)
        response = resp.get_data()
        self.assertIn(b"Charts and Graphs", response)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_widget(self, grep):
        resp = self.client.get("/widget")
        self.assertEqual(resp.status_code, 200)
        response = resp.get_data()
        self.assertIn(b"Embeddable Widget", response)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_defaults(self, grep):
        resp = self.client.get("/raw")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(grep.call_args[0], ())
        kws = grep.call_args[1]
        self.assertIsNone(kws["start"])
        self.assertIsNone(kws["end"])
        self.assertEqual(kws["page"], 1)
        self.assertEqual(kws["rows_per_page"], 25)
        self.assertEqual(kws["order"], "desc")
        for arg in [
            "users",
            "packages",
            "categories",
            "topics",
            "contains",
            "not_users",
            "not_packages",
            "not_categories",
            "not_topics",
        ]:
            self.assertEqual(kws[arg], [])

    @patch("datagrepper.app.count_all_messages", autospec=True, return_value=42)
    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_index(self, grep, count_all_messages):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        response = resp.get_data()
        self.assertIn(b"Datagrepper's documentation", response)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_default_result(self, grep):
        resp = self.client.get("/raw")
        self.assertEqual(resp.status_code, 200)
        result = json.loads(resp.get_data())
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["pages"], 0)
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["raw_messages"], [])

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_contains_delta(self, grep):
        # At one point, this would produce a traceback/500.
        resp = self.client.get("/raw?delta=14400&category=wat&contains=foo")
        self.assertEqual(resp.status_code, 200)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_contains_delta_and_start(self, grep):
        resp = self.client.get("/raw?start=1564503781&delta=600")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(grep.call_args[0], ())
        kws = grep.call_args[1]

        expected_start = datetime.fromtimestamp(1564503781)
        self.assertEqual(kws["start"], expected_start)

        expected_end = expected_start + timedelta(seconds=600)
        self.assertEqual(kws["end"], expected_end)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 180})
    def test_raw_default_query_delta(self, grep):
        resp = self.client.get("/raw")
        self.assertEqual(resp.status_code, 200)
        kws = grep.call_args[1]
        # Verify the default query delta was applied
        self.assertEqual((kws["end"] - kws["start"]).total_seconds(), 180.0)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 180})
    def test_raw_default_query_delta_with_start(self, grep):
        resp = self.client.get("/raw?start=1564503781")
        self.assertEqual(resp.status_code, 200)
        kws = grep.call_args[1]
        # Verify the default query delta was not applied
        self.assertNotEqual((kws["end"] - kws["start"]).total_seconds(), 180.0)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 180})
    def test_raw_default_query_delta_with_delta(self, grep):
        resp = self.client.get("/raw?delta=7200")
        self.assertEqual(resp.status_code, 200)
        kws = grep.call_args[1]
        # Verify the default query delta was not applied
        self.assertEqual((kws["end"] - kws["start"]).total_seconds(), 7200.0)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    @patch.dict(datagrepper.app.app.config, {"DEFAULT_QUERY_DELTA": 180})
    def test_raw_default_query_delta_with_end(self, grep):
        resp = self.client.get("/raw?end=1564503781")
        self.assertEqual(resp.status_code, 200)
        kws = grep.call_args[1]
        self.assertEqual((kws["end"] - kws["start"]).total_seconds(), 180.0)

    @patch("datagrepper.app.dm.Message.grep", side_effect=Exception)
    def test_raw_exception(self, grep):
        resp = self.client.get("/raw")
        self.assertEqual(resp.status_code, 500)
        response = resp.get_data()
        self.assertNotIn(b'"tb": ["Traceback', response)

    @patch("datagrepper.app.dm.Message.grep", side_effect=Exception)
    @patch.dict(datagrepper.app.app.config, {"DEBUG": True})
    def test_raw_exception_debug_true(self, grep):
        resp = self.client.get("/raw")
        self.assertEqual(resp.status_code, 500)
        response = resp.get_data()
        self.assertIn(b'"tb": ["Traceback', response)
        self.assertIn(b"Exception", response)

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_default_query_with_start_and_end_native(self, grep):
        resp = self.client.get(
            "/raw?start=2012-01-02T03:04:05%2B00:00&end=2012-01-02T04:04:05%2B00:00"
        )
        self.assertEqual(resp.status_code, 200)
        kws = grep.call_args[1]
        self.assertEqual(
            kws["start"].astimezone(timezone.utc),
            datetime(2012, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(
            kws["end"].astimezone(timezone.utc),
            datetime(2012, 1, 2, 4, 4, 5, tzinfo=timezone.utc),
        )

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_contains_without_delta(self, grep):
        """https://github.com/fedora-infra/datagrepper/issues/206"""
        resp = self.client.get("/raw?category=wat&contains=foo")
        self.assertEqual(resp.status_code, 400)
        target = b"When using contains, specify a start at most eight months"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_exceptions_contains_and_not_categories_topics(self, grep):
        timestamp = datetime.utcnow()
        resp = self.client.get(f"/raw?contains=hello&start={timestamp}")
        self.assertEqual(resp.status_code, 400)
        target = b"When using contains, specify either a topic or a category as well"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_exceptions_page_less_than_zero(self, grep):
        resp = self.client.get("/raw?page=0")
        self.assertEqual(resp.status_code, 400)
        target = b"page must be &gt; 0"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_exceptions_rows_per_page_over_100(self, grep):
        resp = self.client.get("/raw?rows_per_page=101")
        self.assertEqual(resp.status_code, 400)
        target = b"rows_per_page must be &lt;= 100"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_exceptions_order_not_in_list(self, grep):
        resp = self.client.get("/raw?order=notinlist")
        self.assertEqual(resp.status_code, 400)
        target = b"order must be either &#x27;desc&#x27; or &#x27;asc&#x27;"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_raw_exceptions_possible_sizes_not_in_list(self, grep):
        resp = self.client.get("/raw?size=suchastring")
        self.assertEqual(resp.status_code, 400)
        target = b"size must be in one of these:"
        assert target in resp.data, f"{target!r} not in {resp.data!r}"

    @patch("datagrepper.app.dm.Message.query", autospec=True)
    def test_id(self, query):
        msg = query.filter_by.return_value.first.return_value
        msg.as_dict = MagicMock(return_value={"key": "value"})
        resp = self.client.get("/id?id=one")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(query.filter_by.call_args, ((), {"msg_id": "one"}))

    @patch("datagrepper.app.count_all_messages", autospec=True, return_value=42)
    def test_count(self, count_all_messages):
        resp = self.client.get("/messagecount")
        self.assertEqual(resp.status_code, 200)
        result = json.loads(resp.get_data())
        self.assertEqual(result, {"messagecount": 42})

    @patch("datagrepper.app.dm.Message.grep", return_value=(0, 0, []))
    def test_chart_line(self, grep):
        resp = self.client.get("/charts/line")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, "image/svg+xml")
        self.assertIn(
            b'<svg xmlns:xlink="http://www.w3.org/1999/xlink"',
            resp.get_data(),
        )

    def test_healthz_liveness(self):
        """Test the /healthz/live check endpoint"""
        resp = self.client.get("/healthz/live")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b"OK\n")

    @patch("datagrepper.app.dm.session.execute")
    def test_healthz_readiness_ok(self, execute):
        """Test the /healthz/ready check endpoint"""
        resp = self.client.get("/healthz/ready")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b"OK\n")

    @patch("datagrepper.app.dm.session.execute", side_effect=Exception)
    def test_healthz_readiness_not_ok(self, execute):
        """Test the /healthz/ready check endpoint when not ready"""
        resp = self.client.get("/healthz/ready")
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.data, b"Can't connect to the database\n")

    def test_widget_js(self):
        resp = self.client.get("/widget.js")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, "application/javascript")
        response = resp.get_data()
        self.assertIn(b"$('script#datagrepper-widget')", response)
        self.assertIn(b"datagrepper-widget", response)

    def test_widget_css(self):
        resp = self.client.get("/widget.js?css=true")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, "application/javascript")
        response = resp.get_data()
        self.assertIn(b"/static/css/bootstrap.css", response)
