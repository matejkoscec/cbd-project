import os
import subprocess
import importlib.util

from src.config import jobs_path, output_path, data_path, callback_path


def submit_spark_jobs(config):
    jp = jobs_path(config)
    op = output_path(config)
    input_file = f"{data_path(config)}/access.log"

    files = [f for f in os.listdir(jp) if os.path.isfile(os.path.join(jp, f))]
    files = sorted(files)

    for file in files:
        job_file = f"{jp}/{file}"
        file_name = file.removesuffix(".py")
        command = ["spark-submit", job_file, file_name, input_file, op, config["app"]["spark"]["args"]]

        print(f"Running job '{file_name}'\n", flush=True)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ''):
            print(line, end='')

        process.stdout.close()
        code = process.wait()
        if code == 0:
            print(f"\033[32mJob '{file_name}' finished successfully\033[0m\n", flush=True)
        else:
            print(f"\033[31mJob '{file_name}' exited with code {code}\033[0m\n", flush=True)

        if not config["app"]["spark"]["callbacks"]:
            continue

        callback_file = callback_path(config, job=file_name)
        if not (os.path.exists(callback_file) and os.path.isfile(callback_file)):
            print(f"Callback file {file_name} not found, starting next job.")
            continue

        spec = importlib.util.spec_from_file_location("external_module", callback_file)
        if spec is None:
            print("Unable to load external_module, starting next job.")
            continue

        external_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(external_module)
        external_module.run(config, file_name)
