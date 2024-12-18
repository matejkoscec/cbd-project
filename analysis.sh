#!/bin/bash

#export MPLCONFIGDIR=/tmp/my_matplotlib
#mkdir -p /tmp/my_matplotlib

rm -rf /opt/bitnami/spark/project/output/*

cd /opt/bitnami/spark/project || exit 1
python logs.py --run-callbacks --analyze