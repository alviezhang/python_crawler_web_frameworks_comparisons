#!/usr/bin/env python
from meinheld import patch

patch.patch_all()

import json
import os
from email.utils import formatdate

import requests.adapters
from flask import Flask, make_response

GO_SLEEP_ADDRESS = os.getenv('GO_SLEEP_ADDRESS', '127.0.0.1:8090')

# setup
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

adapter = requests.adapters.HTTPAdapter(pool_connections=10000, pool_maxsize=10000)
session = requests.session()
session.mount('http', adapter)


# views

# flask.jsonify doesn't allow array at top level for security concern.
# So we should have oriiginal one.
def json_response(obj):
    res = make_response(json.dumps(obj))
    res.mimetype = "application/json"
    return add_date_header(res)


def add_date_header(res):
    res.headers['Date'] = formatdate(timeval=None, localtime=False, usegmt=True)
    return res


@app.route("/single")
def single():
    seconds = 3
    url = f'http://{GO_SLEEP_ADDRESS}/?seconds={seconds}'
    response = session.get(url)
    body = response.content
    return json_response(body.decode('utf-8'))


@app.route("/multiple")
def multiple():
    seconds = 1.5
    url = f'http://{GO_SLEEP_ADDRESS}/?seconds={seconds}'
    body_list = []
    response = session.get(url)
    body_list.append(response.content)

    response = session.get(url, params={'r': response.content[0]})
    body_list.append(response.content)
    return json_response(b'\n'.join(body_list).decode('utf-8'))


try:
    import meinheld

    meinheld.server.set_access_logger(None)
except ImportError:
    pass

# entry point for debugging
if __name__ == "__main__":
    app.run(debug=False)
