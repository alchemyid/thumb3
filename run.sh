#!/bin/bash
export PATH="$PATH:/opt/.local/bin"
gunicorn --chdir /opt -w 2 --threads 8 -b 0.0.0.0:8000 --timeout 120 --access-logfile '-' 'app:http()'