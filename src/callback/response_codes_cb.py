import os

import matplotlib.pyplot as plt
import pandas as pd

from src.config import output_path


def run(config, job: str):
    job_output = f"{output_path(config)}/{job}"

    csv_files = [os.path.join(job_output, f) for f in os.listdir(job_output) if f.endswith(".csv")]

    df_list = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    plt.figure(figsize=(10, 6))
    plt.bar(combined_df["status_code"].astype(str), combined_df["count"])
    plt.xlabel("HTTP Status Code")
    plt.ylabel("Count")
    plt.title("Distribution of HTTP Status Codes")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_plot_path = f"{config["app"]["pwd"]}/misc/{job}.png"
    plt.savefig(output_plot_path)
    plt.close()
