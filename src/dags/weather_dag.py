from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import boto3
from botocore.exceptions import NoCredentialsError
# import pandas as pd
from dotenv import load_dotenv
import os
import csv

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get('api_key')
aws_access_key = os.environ.get('aws_access_key')
aws_secret_key = os.environ.get('aws_secret_access_key')

city = 'London'

host = 'https://api.openweathermap.org'
endpoint_string = f'/data/2.5/weather?q={city}&units=metric&APPID={api_key}'
# endpoint_string is a custom paramater api string for OpenWeather

# aws credentials - this is used mainly to send the s3 transformed data into the s3 bucket
aws_credentials = {
    "aws_access_key_id": aws_access_key,
    "aws_secret_access_key": aws_secret_key,
    "region_name": "eu-west-2"
}

# Default args to set my DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 20),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    # Retreive data from the get request api call in 'data' variable
    city = data['name']
    weather_description = data['weather'][0]['description']
    temp_c = data['main']['temp']
    
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    pressure = data['main']['pressure']

    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    
    transformed_data = {
        "Region": city,
        "Description": weather_description,
        "Temperature (C)": temp_c,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Pressure": pressure,
        "Sunrise (Local Time)": str(sunrise_time),
        "Sunset (Local Time)": str(sunset_time),
        "Time of Record": time_of_record
    }
    
    now = datetime.now()
    string_to_add = now.strftime("%d%m%Y%H%M%S")
    string_to_add = f'current_weather_data_{city}_' + string_to_add
    
    
    write_to_csv(transformed_data, f'{string_to_add}.csv')
    load_to_s3_bucket(f'{string_to_add}.csv')
    
        
def load_to_s3_bucket(filename):
    # Create an S3 client
    s3 = boto3.client('s3', **aws_credentials)
    
    # Upload the CSV file to S3
    try:
        s3.upload_file(filename, 'weather-details-bucket', f"weather-details-bucket/{filename}")
    except NoCredentialsError:
        print('Credentials not available')
    
    
def write_to_csv(data, filename):
    with open(filename, 'w', newline="") as f:
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)

with DAG('weather_dag',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:


        is_weather_api_ready = HttpSensor(
        task_id ='is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint=endpoint_string
        )
        
        extract_weather_data = SimpleHttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint=endpoint_string,
        method = 'GET',
        response_filter= lambda r: json.loads(r.text),
        log_response=True
        )
        
        transform_load_weather_data = PythonOperator(
        task_id= 'transform_load_weather_data',
        python_callable=transform_load_data
        )
        
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data