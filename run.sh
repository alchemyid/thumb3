#!/bin/bash
gunicorn --chdir /opt -w 2 --threads 8 -b 0.0.0.0:8000 --timeout 120 --access-logfile '-' 'app:http()'