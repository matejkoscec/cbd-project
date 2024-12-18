import glob

import pandas as pd
from sklearn.ensemble import IsolationForest

from src.config import output_path


def train_model(config):
    file_list = glob.glob(f"{output_path(config)}/{config["app"]["ml"]["job"]}/*.csv")

    df_list = [pd.read_csv(file) for file in file_list]
    combined_df = pd.concat(df_list, ignore_index=True)

    X = combined_df[["status", "bytes", "endpoint_length", "method_index"]]

    clf = IsolationForest(random_state=42, n_estimators=100, contamination=0.01)
    print("Training the model...")
    clf.fit(X)

    predictions = clf.predict(X)
    anomalies = combined_df[predictions == -1]

    num_anomalies = len(anomalies)
    num_total = len(combined_df)
    anomaly_ratio = num_anomalies / num_total * 100

    print("Number of anomalies detected:", num_anomalies)
    print("Total records:", num_total)
    print("Anomaly ratio: {:.2f}%".format(anomaly_ratio))
    print("\nSample anomaly rows:")
    print(anomalies.head())
    print("\nDescriptive statistics of anomaly features:")
    print(anomalies[["status", "bytes", "endpoint_length", "method_index"]].describe())
