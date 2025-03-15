

# Real-Time Fraud Detection Pipeline

This repository contains the code and resources for building a real-time fraud detection and alerting system using Apache Kafka, Spark, and machine learning models. The system integrates fraud prevention strategies with various storage solutions and provides visualization dashboards. Additionally, the project includes CI/CD pipelines, performance testing, and A/B testing for fraud detection models.

## Project Structure

The project is organized into the following main folders:

- **`data-pipeline/`**: Contains Kafka producer and Spark Streaming for real-time data processing.
- **`fraud_prevention/`**: Holds all scripts related to fraud prevention, including real-time fraud detection, fraud alerting, user verification, and the fraud case management dashboard.
- **`model/`**: Includes machine learning models for fraud detection, model training, inference, and model explainability scripts.
- **`data/`**: Folder for storing transaction and feature data files.
- **`storage_security/`**: Contains scripts for data storage and security with Cassandra, PostgreSQL, BigQuery, encryption, role-based access, and compliance management.
- **`visualization_dashboard/`**: Contains the frontend (React/Next.js) and backend (Python API) for the fraud dashboard, with integrations for Apache Superset and Metabase.
- **`ci_cd_testing_deployment/`**: Holds testing scripts, performance testing, CI/CD pipeline configurations (GitHub Actions, Docker, Terraform), and A/B testing scripts.

## Requirements

To run this project, you need the following:

- Python 3.x
- Apache Kafka and Spark setup
- Required Python dependencies in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. **Kafka Producer**:  
   Set up your Kafka server and topic in `config.py`. The Kafka producer in `kafka_producer.py` sends transaction data to the Kafka topic.

2. **Spark Streaming**:  
   The `spark_streaming.py` script uses Spark Streaming to consume and process real-time data from Kafka.

3. **Fraud Prevention System**:  
   The fraud prevention system is built in the `fraud_prevention/` folder. Key scripts include:
   - `real_time_fraud_prevention.py` for applying fraud detection models.
   - `fraud_alerting.py` for sending fraud alerts via Twilio, Slack, and email.

4. **Machine Learning Model**:  
   The models for fraud detection are stored in `model/`. Use `train_model.py` and `train_tf_model.py` to train your models. Model inference is handled by `inference/`.

5. **Data Storage and Security**:  
   Data storage and security mechanisms are in place using scripts in `storage_security/`, which include Cassandra, PostgreSQL, and BigQuery integrations. It also includes encryption and role-based access for securing the data.

6. **Dashboard**:  
   The fraud detection dashboard is built with a React.js frontend and a Python backend. The `visualization_dashboard/` folder contains:
   - The frontend in `frontend/`.
   - The backend API in `backend/`, which serves fraud data.
   - Integration with Apache Superset and Metabase for reporting.

7. **CI/CD Pipeline**:  
   The `ci_cd_testing_deployment/` folder contains:
   - Testing scripts.
   - Performance testing with Locust or K6 in `performance_testing/`.
   - CI/CD pipeline configurations for GitHub Actions, Docker, and Terraform in `ci_cd_pipeline/`.

## Usage

1. **Run Kafka Producer**:
   Start the Kafka producer to send real-time transaction data to the Kafka topic.
   ```bash
   python kafka_producer.py
   ```

2. **Run Spark Streaming**:
   Start Spark Streaming to consume and process the data from Kafka.
   ```bash
   python spark_streaming.py
   ```

3. **Start Flask Application for Fraud Case Management Dashboard**:
   Navigate to `fraud_prevention/` and run the Flask application.
   ```bash
   python fraud_case_management_dashboard.py
   ```

4. **Trigger Fraud Alerting**:
   Use `fraud_alerting.py` to send alerts for detected fraud cases.

5. **Run the Machine Learning Model**:
   Train models or use pre-trained models from the `model/` folder for fraud detection.

## Testing

Unit tests for fraud detection can be found in `tests/test_fraud_detection.py`. To run the tests:

```bash
pytest tests/test_fraud_detection.py
```
Directories
data-pipeline/
├── kafka_producer.py               # Kafka producer for real-time data streaming
├── spark_streaming.py              # Spark Streaming for processing data in real-time
├── config.py                       # Configuration file for managing settings
├── requirements.txt                # Python dependencies for the project
├── tests/
│   └── test_fraud_detection.py     # Unit tests for fraud detection
├── fraud_prevention/               # Folder for all fraud prevention-related scripts
│   ├── real_time_fraud_prevention.py
│   ├── fraud_alerting.py
│   ├── user_verification.py
│   ├── fraud_case_management_dashboard.py
│   ├── config.py
│   └── templates/
│       └── index.html
├── model/                           # Folder for machine learning models and related scripts
│   ├── train_model.py
│   ├── train_tf_model.py
│   ├── inference/
│   ├── explainability/
│   └── models/
├── data/                           # Folder for storing data files
│   ├── transactions.csv
│   └── features.csv
├── storage_security/               # Folder for data storage & security
│   ├── cassandra_storage.py
│   ├── postgres_storage.py
│   ├── bigquery_storage.py
│   ├── encryption.py
│   ├── role_based_access.py
│   └── compliance.py
├── visualization_dashboard/        # New folder for visualization and dashboard
│   ├── frontend/                   # React.js/Next.js frontend
│   │    ├── public/                # Static assets like images, icons
│   │    ├── src/                   # React components and pages
│   │    └── package.json           # NPM dependencies for React app
│   ├── backend/                    # Backend API to serve data to the frontend
│   │    ├── fraud_dashboard_api.py  # Python API to fetch fraud data and insights
│   │    └── config.py              # Backend configuration file
│   ├── superset_integration.py     # Integration with Apache Superset for reporting
│   └── metabase_integration.py     # Integration with Metabase for reporting
├── ci_cd_testing_deployment/       # New folder for CI/CD, testing, and deployment
│   ├── tests/                      # Unit & integration tests for fraud detection
│   │    └── test_fraud_detection.py
│   ├── performance_testing/        # Performance testing using Locust or K6
│   │    └── locustfile.py          # Locust script for simulating transactions
│   ├── ci_cd_pipeline/             # CI/CD pipeline configuration
│   │    ├── github_actions.yml     # GitHub Actions CI/CD pipeline
│   │    ├── dockerfile             # Dockerfile for the app container
│   │    └── terraform.tf           # Terraform configuration for deployment
│   └── ab_testing/                 # Folder for A/B testing scripts
│        ├── ab_test.py             # A/B testing script for fraud models
│        └── ab_test_results.py     # Script for analyzing A/B test results
