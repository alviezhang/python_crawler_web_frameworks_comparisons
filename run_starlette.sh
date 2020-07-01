#!/bin/bash

gunicorn starlette_server:app -k uvicorn.workers.UvicornWorker -b '0.0.0.0:8080'
