# SPDX-License-Identifier: GPL-2.0+
# Copyright 2018 Mike Bonnet <mikeb@redhat.com>

import json
import os
import unittest
from mock import MagicMock, patch
with patch.dict(os.environ, DATAGREPPER_CONFIG='/dev/null'):
    import datagrepper.app

class TestAPI(unittest.TestCase):

    def setUp(self):
        datagrepper.app.app.testing = True
        self.client = datagrepper.app.app.test_client()


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_raw_defaults(self, grep):
        resp = self.client.get('/raw')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(grep.call_args[0], ())
        kws = grep.call_args[1]
        self.assertIsNone(kws['start'])
        self.assertIsNone(kws['end'])
        self.assertEqual(kws['page'], 1)
        self.assertEqual(kws['rows_per_page'], 25)
        self.assertEqual(kws['order'], 'desc')
        for arg in ['users', 'packages', 'categories', 'topics', 'contains',
                    'not_users', 'not_packages', 'not_categories', 'not_topics']:
            self.assertEqual(kws[arg], [])


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_raw_default_result(self, grep):
        resp = self.client.get('/raw')
        self.assertEqual(resp.status_code, 200)
        result = json.loads(resp.get_data())
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['pages'], 0)
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['raw_messages'], [])


    @patch('datagrepper.app.dm.Message.query', autospec=True)
    def test_id(self, query):
        msg = query.filter_by.return_value.first.return_value
        msg.__json__ = MagicMock(return_value={'key': 'value'})
        resp = self.client.get('/id?id=one')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(query.filter_by.call_args, ((), {'msg_id': 'one'}))


    @patch('datagrepper.app.count_all_messages', autospec=True, return_value=42)
    def test_count(self, count_all_messages):
        resp = self.client.get('/messagecount')
        self.assertEqual(resp.status_code, 200)
        result = json.loads(resp.get_data())
        self.assertEqual(result, {'messagecount': 42})


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_chart_line(self, grep):
        resp = self.client.get('/charts/line')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'image/svg+xml')
        self.assertIn('<svg xmlns:xlink="http://www.w3.org/1999/xlink',
                      resp.get_data())
