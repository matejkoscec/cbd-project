import os
import pandas as pd
import matplotlib.pyplot as plt

from src.config import output_path


def run(config, job: str):
    job_output = f"{output_path(config)}/{job}"

    csv_files = [os.path.join(job_output, f) for f in os.listdir(job_output) if f.endswith(".csv")]

    df_list = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    plt.figure(figsize=(10, 6))
    plt.bar(combined_df['user_agent'].astype(str), combined_df['count'])
    plt.xlabel('User Agent')
    plt.ylabel('Count')
    plt.title('User Agent Distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()

    output_plot_path = f"{output_path(config)}/{job}_user_agent_distribution.png"
    plt.savefig(output_plot_path)
    plt.close()
