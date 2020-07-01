## Python Web Frameworks Performance Comparisons

### Purpose

We want to use Python to build a new spider framework, and we care about performance, so we have this test to
compare performance between different frameworks.

### Frameworks

- starlette
- Flask
- tornado

### Test items

Because this is a test for the web frameworks, so we only focus on web performance with single and multiple HTTP requests to a third-party server.

- Slow single HTTP request
- Slow multiple HTTP requests

### How to test

First of all, install the requirements:

```bash
python -m venv .venv
source.venv/bin/activate
pip install -r requirements.txt
```

Seconds, start the `gosleep` server, which listen on `0.0.0.0:8090`:

```bash
./run_sleep_server.sh
```

Run one of the following web server

- `run_flask.sh`
- `run_starlette.sh`
- `run_tornado.sh`

Then run the benchmark command:

```bash
wrk -d30s -t50 -c10000 --timeout 30 http://127.0.0.1:8080/single
wrk -d30s -t50 -c10000 --timeout 30 http://127.0.0.1:8080/multiple
```
