# -*- coding: utf-8 -*-
"""Test upstream responses."""
import requests
import os
import unittest


class UpstreamTestCase(unittest.TestCase):
    """Testcase for upstream docker container."""

    def setUp(self):
        """Setup testcase."""
        self.baseurl = 'http://{host}:{port}'.format(
            host=os.environ.get('UPSTREAM_IP', '127.0.0.1'),
            port=os.environ.get('UPSTREAM_PORT', '8080')
        )

    def get_url(self, endpoint):
        """Return the url for a given endpoint."""
        return '{base_url}{endpoint}'.format(
            base_url=self.baseurl,
            endpoint=endpoint
        )

    def test_get(self):
        """Test GET verb."""
        endpoint = '/foo'
        resp = requests.get(
            self.get_url(endpoint)
        )
        self.assertEqual('application/json', resp.headers['Content-Type'])
        self.assertEqual(200, resp.status_code)
        self.assertEqual(endpoint, resp.json()['route'])
        self.assertEqual('GET', resp.json()['verb'])

        endpoint = '/foo/bar/foobar/barfoo'
        resp = requests.get(
            self.get_url(endpoint)
        )
        self.assertEqual(endpoint, resp.json()['route'])

    def test_get_query_string(self):
        """Test GET verb with query string."""
        endpoint = '/foo/bar/?foobar=moo&barfoo=ca'
        resp = requests.get(
            self.get_url(endpoint)
        )
        self.assertEqual('application/json', resp.headers['Content-Type'])
        self.assertEqual(200, resp.status_code)
        self.assertEqual('/foo/bar/', resp.json()['route'])
        self.assertIsInstance(resp.json()['query_data'], dict)
        self.assertEqual(resp.json()['query_data']['foobar'], 'moo')

    def test_post(self):
        """Test POST verb."""
        endpoint = '/foo'
        payload = {'some': 'data'}
        resp = requests.post(
            self.get_url(endpoint),
            data=payload
        )
        self.assertEqual('application/json', resp.headers['Content-Type'])
        self.assertEqual(200, resp.status_code)
        self.assertEqual(endpoint, resp.json()['route'])
        self.assertEqual('POST', resp.json()['verb'])
        self.assertIsInstance(resp.json()['form_data'], dict)

        endpoint = '/foo/bar/foobar/barfoo'
        resp = requests.post(
            self.get_url(endpoint),
            data=payload
        )
        self.assertEqual(endpoint, resp.json()['route'])
