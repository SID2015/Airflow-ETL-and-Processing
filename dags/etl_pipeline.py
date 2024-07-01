from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
from sqlalchemy import create_engine
import logging
import sqlite3
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Assume data_ingestion returns a DataFrame
def data_ingestion(**kwargs):
    try:
        csv_file_path = os.path.join(os.path.dirname(__file__), 'interaction_data.csv')
        df = pd.read_csv(csv_file_path)
        kwargs['ti'].xcom_push(key='df', value=df)  # Pushing DataFrame to XCom
    except Exception as e:
        logging.error(f"Error in data_ingestion: {str(e)}")
        raise

# Assume data_cleaning requires a DataFrame input
def data_cleaning(**kwargs):
    try:
        ti = kwargs['ti']
        df = ti.xcom_pull(key='df', task_ids='data_ingestion')  # Pulling DataFrame from XCom
        # Data cleaning steps
        df.fillna({'action': 'unknown'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        ti.xcom_push(key='df', value=df)  # Pushing DataFrame to XCom for next task
    except Exception as e:
        logging.error(f"Error in data_cleaning: {str(e)}")
        raise

# Assume data_transformation requires a DataFrame input
def data_transformation(**kwargs):
    try:
        ti = kwargs['ti']
        df = ti.xcom_pull(key='df', task_ids='data_cleaning')  # Pulling DataFrame from XCom
        # Data transformation steps
        user_interaction_counts = df.groupby('user_id').size().reset_index(name='interaction_count_user')
        product_interaction_counts = df.groupby('product_id').size().reset_index(name='interaction_count_product')
        df = df.merge(user_interaction_counts, on='user_id', how='left')
        df = df.merge(product_interaction_counts, on='product_id', how='left')
        ti.xcom_push(key='df', value=df)  # Pushing DataFrame to XCom for next task
    except Exception as e:
        logging.error(f"Error in data_transformation: {str(e)}")
        raise

# Assume data_loading requires a DataFrame input
def data_loading(**kwargs):
    try:
        ti = kwargs['ti']
        df = ti.xcom_pull(key='df', task_ids='data_transformation')  # Pulling DataFrame from XCom
        # Data loading to SQLite database
        # engine = create_engine('sqlite:///interaction_data.db', echo=True)
        # df.to_sql('interactions', con=engine, index=False, if_exists='replace')
        db_path = os.path.join(os.path.dirname(__file__), 'interaction_data.db')
        conn = sqlite3.connect(db_path)
        df.to_sql('interaction_data', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        logging.error(f"Error in data_loading: {str(e)}")
        raise

# Define the DAG
with DAG('etl_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    ingest_data = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion,
        provide_context=True
    )

    clean_data = PythonOperator(
        task_id='data_cleaning',
        python_callable=data_cleaning,
        provide_context=True
    )

    transform_data = PythonOperator(
        task_id='data_transformation',
        python_callable=data_transformation,
        provide_context=True
    )

    load_data = PythonOperator(
        task_id='data_loading',
        python_callable=data_loading,
        provide_context=True
    )

    # Define task dependencies
    ingest_data >> clean_data >> transform_data >> load_data
