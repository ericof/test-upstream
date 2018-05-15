"""Test upstream responses."""
import pytest
import requests

from prettyconf import config


@pytest.fixture
def base_url():
    host = config('UPSTREAM_IP', default='127.0.0.1')
    port = config('UPSTREAM_PORT', default='8080')
    return f'http://{host}:{port}'


test_data = [
    '/foo',
    '/foo/bar/foobar/barfoo',
]

@pytest.mark.parametrize('endpoint', test_data)
def test_get(base_url, endpoint):
    """Test GET verb."""
    resp = requests.get(f'{base_url}{endpoint}')
    assert resp.headers['Content-Type'] == 'application/json'
    assert resp.status_code == 200
    assert resp.json()['route'] == endpoint
    assert resp.json()['verb'] == 'GET'


test_data = [
    ('/foo/bar/?foobar=moo&barfoo=ca', '/foo/bar/', 'foobar', 'moo'),
    ('/foo/bar/?foobar=moo&barfoo=ca', '/foo/bar/', 'barfoo', 'ca'),
]

@pytest.mark.parametrize('endpoint,route,key,value', test_data)
def test_get_query_string(base_url, endpoint, route, key, value):
    """Test GET verb with query string."""
    resp = requests.get(f'{base_url}{endpoint}')
    assert resp.headers['Content-Type'] == 'application/json'
    assert resp.status_code == 200
    assert resp.json()['route'] == route
    assert resp.json()['verb'] == 'GET'
    assert isinstance(resp.json()['query_data'], dict) is True
    assert resp.json()['query_data'][key] == value

test_data = [
    ('/foo/', {'key': 'value'}),
    ('/foo/bar', {'key': 'value'}),
]
@pytest.mark.parametrize('endpoint,payload', test_data)
def test_post(base_url, endpoint, payload):
    resp = requests.post(f'{base_url}{endpoint}', data=payload)
    assert resp.headers['Content-Type'] == 'application/json'
    assert resp.status_code == 200
    assert resp.json()['route'] == endpoint
    assert resp.json()['verb'] == 'POST'
    assert isinstance(resp.json()['form_data'], dict) is True

test_data = [
    '/sleep/1',
    '/sleep/2',
]
@pytest.mark.parametrize('endpoint', test_data)
def test_sleep(base_url, endpoint):
    """Test sleep route with GET."""
    resp = requests.get(f'{base_url}{endpoint}')
    assert resp.headers['Content-Type'] == 'application/json'
    assert resp.status_code == 200
    assert resp.json()['route'] == endpoint
    assert resp.json()['verb'] == 'GET'


test_data = [
    ('/error/404', 404),
    ('/error/500', 500),
    ('/error/502', 502),
    ('/error/503', 503),
    ('/error/504', 504),
]
@pytest.mark.parametrize('endpoint,status_code', test_data)
def test_error_route(base_url, endpoint, status_code):
    """Test sleep route with GET."""
    resp = requests.get(f'{base_url}{endpoint}')
    assert resp.status_code == status_code
