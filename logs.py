import os
import argparse

import yaml

from src.config import update_config
from src.model import train_model
from src.spark_jobs import submit_spark_jobs

parser = argparse.ArgumentParser(description="Logs CLI program.")
parser.add_argument("--run-callbacks",
                    action="store_true",
                    help="Run a callback function after the job is complete")
parser.add_argument("--analyze",
                    action="store_true",
                    help="Train a classification model to find anomalies")
parser.add_argument("--spark-args",
                    type=str,
                    help="Additional arguments for the submit task")

script_path = os.path.dirname(os.path.abspath(__file__))
pwd = script_path.removesuffix("/src")

default_config = {
    "app": {
        "pwd": pwd,
        "spark": {
            "jobs": "spark_jobs",
            "data": "data",
            "output": "output",
            "callbacks": False,
            "args": "",
        },
        "ml": {
            "enabled": False,
            "job": None
        }
    }
}

if __name__ == "__main__":
    args = parser.parse_args()
    with open(f"{pwd}/config.yaml", "r") as file:
        yaml_config = yaml.safe_load(file)

    config = update_config(default_config, yaml_config, args)
    print(f"{config=}")

    print("\nRunning Spark jobs")
    submit_spark_jobs(config)

    if config["app"]["ml"]["enabled"]:
        print("\nRunning a ML model to detect anomalies")
        train_model(config)
