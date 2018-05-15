# -*- coding: utf-8 -*-
"""Simple echo chamber service."""
import bottle
import json

from prettyconf import config
from time import sleep


PORT = config('PORT', default=8080)


@bottle.route('/sleep/<how_long:int>', method='ANY')
def sleep_route(how_long):
    """Sleep for the time given as parameter
       then return a JSON response with the same url.
    """
    request = bottle.request
    method = request.method
    headers = request.headers
    headers_data = dict([(key, headers[key]) for key in headers])
    query_data = dict([(key, request.query[key]) for key in request.query])
    form_data = dict([(key, request.forms[key]) for key in request.forms])
    body = {
        'route': f'/sleep/{how_long}',
        'verb': method,
        'headers': headers_data,
        'form_data': form_data,
        'query_data': query_data,
    }

    return bottle.HTTPResponse(
        status=200,
        content_type='application/json',
        body=json.dumps(body)
    )


@bottle.route('/error/<status_code:int>', method='ANY')
def error_route(status_code):
    """Return the status code."""
    request = bottle.request
    method = request.method
    headers = request.headers
    headers_data = dict([(key, headers[key]) for key in headers])
    query_data = dict([(key, request.query[key]) for key in request.query])
    form_data = dict([(key, request.forms[key]) for key in request.forms])
    body = {
        'route': f'/error/{status_code}',
        'verb': method,
        'headers': headers_data,
        'form_data': form_data,
        'query_data': query_data,
    }

    return bottle.HTTPResponse(
        status=status_code,
        content_type='application/json',
        body=json.dumps(body)
    )


@bottle.route('<name:path>', method='ANY')
def catch_all(name):
    """Catch all requests, return a JSON response with the same url."""
    name = name if name.startswith('/') else '/{}'.format(name)
    request = bottle.request
    method = request.method
    headers = request.headers
    headers_data = dict([(key, headers[key]) for key in headers])
    query_data = dict([(key, request.query[key]) for key in request.query])
    form_data = dict([(key, request.forms[key]) for key in request.forms])
    body = {
        'route': name,
        'verb': method,
        'headers': headers_data,
        'form_data': form_data,
        'query_data': query_data,
    }

    return bottle.HTTPResponse(
        status=200,
        content_type='application/json',
        body=json.dumps(body)
    )

bottle.run(host='0.0.0.0', port=PORT)
