#!/bin/bash

gunicorn server:app :8000 -n antrian-rx -D
echo 'antrian-rx running on port 8000'
