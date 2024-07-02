# Airflow-ETL-and-Processing

# ETL Pipeline Project

This project demonstrates an ETL (Extract, Transform, Load) pipeline using Airflow and sqlite.

## Project Structure

- `dags/`: Airflow DAGs and initialization scripts.
- `sql/`: SQL queries and schema creation scripts.
- `data/`: Sample data for testing (I have used interaction_data.csv as sample file for testing).

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
   ![docker_containers](https://github.com/SID2015/Airflow-ETL-and-Processing/blob/main/imgs/docker_container.png)

   Access Airflow UI at http://localhost:8080 and verify it's running

   You can set user name and password for airflow UI using docker-compose.yml file or by running below command
   
   airflow users create --username admin –password admin –firstname admin –lastname admin –role Admin –email admin@email.com


3.  **Start Airflow DAGs:**

   Open Airflow UI (http://localhost:8080).
   Turn on the init_postgres_schema DAG.)
    ![airflow_setup](https://github.com/SID2015/Airflow-ETL-and-Processing/blob/main/imgs/airflow_setup.png)
   Turn on the etl_pipeline DAG and enable auto-refresh to auto update the pipeline status on UI.

   ![airflow_run](https://github.com/SID2015/Airflow-ETL-and-Processing/blob/main/imgs/airflow_run.png)
   

4.  **Monitor and Manage DAGs:**

   Use Airflow UI to monitor DAG runs, task statuses, and logs.

   ![airflow_run](https://github.com/SID2015/Airflow-ETL-and-Processing/blob/main/imgs/airflow_run.png)

   ![airflow_xcom](https://github.com/SID2015/Airflow-ETL-and-Processing/blob/main/imgs/airflow_xcom.png)
   
   Adjust DAG schedules or task dependencies as needed.

   Note : Data Ingestion: Place your data files (e.g., interaction_data.csv) in the data/ directory.


