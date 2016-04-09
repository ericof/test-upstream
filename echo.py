# -*- coding: utf-8 -*-
"""Simple echo chamber service."""
import bottle
import json
import re


PATTERN = re.compile(r"'(?P<route>[\?A-Za-z0-9_\./\\-]*)'")


@bottle.error(404)
def error404(error):
    """Catch all requests, return a JSON response with the same url."""
    match = re.search(PATTERN, error.body)
    if match:
        body = match.groupdict()
    else:
        body = {'route': error.body}

    return bottle.HTTPResponse(
        status=200,
        content_type='application/json',
        body=json.dumps(body)
    )

bottle.run(host='0.0.0.0', port=8080)
