from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import boto3
from botocore.config import Config
from botocore import UNSIGNED

def fetch_cocktail_data():
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
    if response.status_code == 200:
        data = response.json()
        cocktail_name = data['drinks'][0]['strDrink']
        cocktail_instructions = data['drinks'][0]['strInstructions']
        return f"<html><body><h1>Today's Cocktail: {cocktail_name}</h1><p>{cocktail_instructions}</p></body></html>"
    else:
        return "<html><body><h1>Error fetching cocktail data</h1></body></html>"

def save_to_s3(html_content, bucket_name='biscoairflow', file_name='todays_cocktail.html'):    
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=html_content, ContentType='text/html', ACL='public-read')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1),
    'retry_delay': timedelta(minutes=5),
    'retries': 1
}

dag = DAG(
    'daily_cocktail_suggestion',
    default_args=default_args,
    description='A DAG to fetch daily cocktail suggestions and save to S3 without credentials',
    schedule_interval='*/30 * * * *',  # Every 30 minutes
    catchup=False
)

fetch_data = PythonOperator(
    task_id='fetch_cocktail',
    python_callable=fetch_cocktail_data,
    provide_context=True,
    dag=dag
)

save_data = PythonOperator(
    task_id='save_to_s3',
    python_callable=save_to_s3,
    provide_context=True,
    op_kwargs={'html_content': "{{ ti.xcom_pull(task_ids='fetch_cocktail') }}"},
    dag=dag
)

fetch_data >> save_data
