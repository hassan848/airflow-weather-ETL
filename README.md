# airflow-weather-ETL
A data engineering project consisting of building an ETL pipeline using Apache Airflow and AWS (Amazon Web Services) with Python, Amazon S3 and EC2.
I built an ETL process that extracts weather data from the Open Weather API, this is transformed and then loaded into a simple storage service (AWS s3 bucket).
The project is an automated process where the ETL pipeline runs everyday and the airflow dags are invoked - a csv file is then sent to the s3 bucket of the new transformed clean data.

I first created an EC2 instance where I configured the Airflow and python code. 
I extract, transform the data in python with tasks on a dag within Apache Airflow - the Apache Airflow is running on an AWS EC2 instance (A virtual server)
