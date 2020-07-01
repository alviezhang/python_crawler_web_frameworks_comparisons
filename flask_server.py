#!/usr/bin/env python
from meinheld import patch
patch.patch_all()

import json
from email.utils import formatdate

import requests
from flask import Flask, make_response

# setup

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


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
    url = f'http://192.168.10.18:8090/?seconds={seconds}'
    response = requests.get(url)
    body = response.content
    return json_response(body.decode('utf-8'))


@app.route("/multiple")
def multiple():
    seconds = 3
    url = f'http://192.168.10.18:8090/?seconds={seconds}'
    body_list = []
    response = requests.get(url)
    body_list.append(response.content)

    response = requests.get(url)
    body_list.append(response.content)
    return json_response(b'\n'.join(body_list).decode('utf-8'))


try:
    import meinheld

    meinheld.server.set_access_logger(None)
    meinheld.set_keepalive(120)
except ImportError:
    pass

# entry point for debugging
if __name__ == "__main__":
    app.run(debug=False)

