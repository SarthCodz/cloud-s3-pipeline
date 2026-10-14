# Cloud-Backed S3 Data Processing Pipeline

A containerized Python data engineering pipeline that automates secure file ingestion, processing, and storage management using AWS S3 and Pandas.

## Tech Stack
* **Language:** Python
* **Cloud Infrastructure:** AWS S3 (`boto3`)
* **Data Manipulation:** Pandas
* **Containerization:** Docker

## Project Architecture
1. Connects securely to an AWS S3 bucket via environment-based credentials.
2. Downloads raw data files dynamically into execution memory.
3. Cleans and transforms the dataset using Pandas.
4. Uploads the processed output back to a designated `processed/` folder in the S3 bucket.
5. Containerized via Docker for portable, environment-agnostic execution.