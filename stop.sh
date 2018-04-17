#!/bin/bash

kill -9 `ps aux |grep gunicorn |grep antrian-rx |awk '{ print $2 }'`
