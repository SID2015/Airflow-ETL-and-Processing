# Airflow-ETL-and-Processing

# ETL Pipeline Project

This project demonstrates an ETL (Extract, Transform, Load) pipeline using Airflow and PostgreSQL.

## Project Structure

- `dags/`: Airflow DAGs and initialization scripts.
- `scripts/`: Python scripts for ETL operations.
- `sql/`: SQL queries and schema creation scripts.
- `data/`: Sample data for testing.

## Setup Instructions

### Prerequisites

- Docker installed on your system.
- Git installed on your system.
- If you are using Windows O.S. just like I used for this scenario, you would need to install WSL (Window Subsytem for Linux) https://learn.microsoft.com/en-us/windows/wsl/install

### Steps to Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/etl_project.git
   cd etl_project

2. **Setup Docker environment:**
   ```bash
   Build the Docker image for Airflow:

   docker build -t airflow-local .

   Run docker compose command

   Access Airflow UI at http://localhost:8080 and verify it's running

3.  **Start Airflow DAGs:**

   Open Airflow UI (http://localhost:8080).
   Turn on the init_postgres_schema DAG.
   Turn on the etl_pipeline DAG.

4.  **Monitor and Manage DAGs:**

   Use Airflow UI to monitor DAG runs, task statuses, and logs.
   Adjust DAG schedules or task dependencies as needed.

   Note : Data Ingestion: Place your data files (e.g., interaction_data.csv) in the data/ directory.


