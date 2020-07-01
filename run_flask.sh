#!/bin/bash

gunicorn flask_server:app -k meinheld.gmeinheld.MeinheldWorker -b '0.0.0.0:8080'
