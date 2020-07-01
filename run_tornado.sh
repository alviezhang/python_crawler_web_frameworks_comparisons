#!/bin/bash

gunicorn tornado_server:app -k tornado -b '0.0.0.0:8080'
