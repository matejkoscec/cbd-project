# Cloud and Big Data

**[Course project]**

This is a PoC end-to-end application that serves to show the application of Cloud and Big Data principles.

**Description**

The idea is to analyze large-scale log files from a website to identify traffic patterns, user behavior, and peak usage
hours.
In order to have a healthy working application it's necessary to monitor the activity for potential anomalies or
attacks.

Log files grow rapidly (hundreds of GBs) all the time, which requires distributed processing and storage.
Having multiple services running and being able to monitor them quickly becomes difficult, because of sheer volume of
data being produced.

**Data**

[Link to dataset](
https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs
) (Size 3.5GB)

The dataset represents a log file from a web service.
Every log record represents user or bot traffic towards the site.
The log format is represented as a standard Apache HTTP Server
access log format.

**Application**

The idea was to make a cloud native application that could be easily adopted to a local or a cloud environment.
This is a CLI application that is intended to be used in batch processing scenarios.
In this project the application works with locally available data, but it can easily be put behind an interface to use
the available cloud storage or Dataproc clusters needed to run the Spark machinery.
Data flow of the application is as follows:

```text
(Raw Data) -> [Spark] -> (Structured Data) -> [ML Model] -> (Analysis)
                            or directly    -> [Analysis]
```



The project structure is as follows:

```text
project/
├─ logs.py -> entrypoint to the application
├─ data/
├─ src/
│  ├─ callback/
│  │  ├─ [job]_cb.py
│  │  └─ ...
│  ├─ config.py
│  ├─ model.py
│  └─ spark_jobs.py
├─ spark_jobs/
│  ├─ [job].py
│  └─ ...
└─ config.yaml
```

**Usage**

**Advanced features**

**Conclusions**
