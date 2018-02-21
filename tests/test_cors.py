# SPDX-License-Identifier: GPL-2.0+
# Copyright 2018 Mike Bonnet <mikeb@redhat.com>

import os
import re
import unittest
from mock import patch
with patch.dict(os.environ, DATAGREPPER_CONFIG='/dev/null'):
    import datagrepper.app

class TestCORS(unittest.TestCase):

    def setUp(self):
        datagrepper.app.app.testing = True
        self.client = datagrepper.app.app.test_client()


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_no_cors(self, grep):
        resp = self.client.get('/raw')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in resp.headers)


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_cors(self, grep):
        resp = self.client.get('/raw', headers={'Origin': 'http://cors.example.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://cors.example.com')


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_cors_no_preflight(self, grep):
        resp = self.client.get('/raw', headers={'Origin': 'http://cors.example.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://cors.example.com')
        self.assertFalse('Origin' in resp.headers.get('Vary', ''))
        self.assertFalse('Access-Control-Max-Age' in resp.headers)


    @patch.dict(datagrepper.app.app.config, CORS_DOMAINS=[re.compile(r'http://safe\.site'),
                                                          re.compile(r'http://.*\.honest')])
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_cors_list(self, grep):
        resp = self.client.get('/raw', headers={'Origin': 'http://safe.site'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://safe.site')
        resp = self.client.get('/raw', headers={'Origin': 'http://really.honest'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://really.honest')


    @patch.dict(datagrepper.app.app.config, CORS_DOMAINS=[re.compile(r'http://safe\.site'),
                                                          re.compile(r'http://.*\.honest')])
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_cors_reject(self, grep):
        resp = self.client.get('/raw', headers={'Origin': 'http://malicious.site'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in resp.headers)


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_no_cors(self, grep):
        resp = self.client.options('/raw')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in resp.headers)


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertFalse('Access-Control-Allow-Methods' in resp.headers)
        self.assertFalse('Access-Control-Allow-Headers' in resp.headers)
        self.assertTrue('Origin' in resp.headers.get('Vary', ''))
        self.assertTrue('Access-Control-Max-Age' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Max-Age'], '600')


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_methods(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com',
                                                    'Access-Control-Request-Method': 'GET'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertTrue('Access-Control-Allow-Methods' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Methods'], 'GET, OPTIONS')
        self.assertFalse('Access-Control-Allow-Headers' in resp.headers)


    @patch.dict(datagrepper.app.app.config, CORS_METHODS=['POST', 'OPTIONS'])
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_alternate_methods(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com',
                                                    'Access-Control-Request-Method': 'GET'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertTrue('Access-Control-Allow-Methods' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Methods'], 'POST, OPTIONS')
        self.assertFalse('Access-Control-Allow-Headers' in resp.headers)


    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_headers(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com',
                                                    'Access-Control-Request-Method': 'GET',
                                                    'Access-Control-Request-Headers': 'Content-Type, X-Custom-Header'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertTrue('Access-Control-Allow-Methods' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Methods'], 'GET, OPTIONS')
        self.assertTrue('Access-Control-Allow-Headers' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Headers'], 'Content-Type, X-Custom-Header')


    @patch.dict(datagrepper.app.app.config, CORS_HEADERS=[re.compile(r'Content-.*'),
                                                          re.compile(r'X-Other-.*')])
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_headers_filter(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com',
                                                    'Access-Control-Request-Method': 'GET',
                                                    'Access-Control-Request-Headers': 'Content-Type, X-Custom-Header'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertTrue('Access-Control-Allow-Methods' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Methods'], 'GET, OPTIONS')
        self.assertTrue('Access-Control-Allow-Headers' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Headers'], 'Content-Type')


    @patch.dict(datagrepper.app.app.config, CORS_HEADERS=[re.compile(r'Content-.*'),
                                                          re.compile(r'X-Other-.*')])
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_headers_no_match(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com',
                                                    'Access-Control-Request-Method': 'GET',
                                                    'Access-Control-Request-Headers': 'X-Some-Header, X-Custom-Header'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertTrue('Access-Control-Allow-Methods' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Methods'], 'GET, OPTIONS')
        self.assertFalse('Access-Control-Allow-Headers' in resp.headers)


    @patch.dict(datagrepper.app.app.config, CORS_MAX_AGE='1800')
    @patch('datagrepper.app.dm.Message.grep', return_value=(0, 0, []))
    def test_preflight_cors_max_age(self, grep):
        resp = self.client.options('/raw', headers={'Origin': 'http://preflight.example.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Allow-Origin'], 'http://preflight.example.com')
        self.assertFalse('Access-Control-Allow-Methods' in resp.headers)
        self.assertFalse('Access-Control-Allow-Headers' in resp.headers)
        self.assertTrue('Origin' in resp.headers.get('Vary', ''))
        self.assertTrue('Access-Control-Max-Age' in resp.headers)
        self.assertEqual(resp.headers['Access-Control-Max-Age'], '1800')
