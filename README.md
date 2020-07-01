## Python Web Frameworks Performance Comparisons

This requires Python 3.6+

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

You need to adjust parameter for `-c` concurrent connections option, and find a minimum number to push python server CPU to about 80%~100%.

### Test Result

OS: Archlinux host in KVM

CPU: 4 x AMD Ryzen 3 PRO 3200G with Radeon Vega Graphics (1 Socket)

Memory: 8 GiB

#### Not reuse connections

| Single req  | Flask | Starlette | tornado |
| ----------- | ----- | --------- | ------- |
| RPS         | 131.6 | 516.8     | 521.1   |
| Latency     | 3.71s | 5.46s     | 4.98s   |
| Connections | 500   | 3000      | 1000    |
| Threads     | 50    | 300       | 100     |

| Multi req   | Flask | Starlette | tornado |
| ----------- | ----- | --------- | ------- |
| RPS         | 131.6 | 382.0     | 169.0   |
| Latency     | 3.71s | 7.12s     | 5.60s   |
| Connections | 500   | 3000      | 1000    |
| Threads     | 50    | 300       | 100     |

#### Reuse connections

| Single req  | Flask | Starlette | tornado |
| ----------- | ----- | --------- | ------- |
| RPS         | 148.1 | 744.9s    | 713.0   |
| Latency     | 3.11s | 3.75s     | 3.91s   |
| Connections | 500   | 3000      | 3000    |
| Threads     | 50    | 300       | 300     |

| Multi req   | Flask | Starlette | tornado |
| ----------- | ----- | --------- | ------- |
| RPS         | 230.4 | 548.5     | 493.2   |
| Latency     | 2.10s | 2.63s     | 2.89s   |
| Connections | 500   | 1500      | 1500    |
| Threads     | 50    | 150       | 150     |

It's wired that Flask's result multiple requests performance is better than single,  maybe my code has something wrong. 
And it is obviously that tornado and Starlette has similar performance when we reuse connections, but has bad performance
when we don't reuse connections.
