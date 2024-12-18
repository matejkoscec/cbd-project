#!/bin/bash

mkdir -p /opt/bitnami/spark/project

cp -r /mnt/files/* /opt/bitnami/spark/project
rm -rf /opt/bitnami/spark/project/output/*

if [ "$1" == "--init" ]; then
  cd /opt/bitnami/spark/project/data || exit
  echo "> Extracting dataset"
  tar -xvf access.log.tar

  echo "Installing python packages"
  pip install pyyaml numpy pandas scikit-learn matplotlib
fi
