from argparse import Namespace


def jobs_path(config):
    return f"{config["app"]["pwd"]}/{config["app"]["spark"]["jobs"]}"


def data_path(config):
    return f"{config["app"]["pwd"]}/{config["app"]["spark"]["data"]}"


def output_path(config):
    return f"{config["app"]["pwd"]}/{config["app"]["spark"]["output"]}"


def callback_path(config, job):
    return f"{config["app"]["pwd"]}/src/callback/{job}_cb.py"


def update_config(original, updates, args: Namespace):
    new_config = update(original, updates)

    if args.run_callbacks:
        new_config["app"]["spark"]["callbacks"] = True
    if args.analyze:
        new_config["app"]["ml"]["enabled"] = True
    if args.spark_args:
        new_config["app"]["spark"]["args"] = args.spark_args

    return new_config


def update(original, updates):
    for key, val in updates.items():
        if val is None:
            continue

        if isinstance(val, dict):
            original[key] = update(original.get(key, {}), val)
        else:
            original[key] = val

    return original

class SparkJobConfig:

    def __init__(self, argv):
        self.name = argv[1]
        self.input_path = argv[2]
        self.output_path = argv[3]
