# airflow-weather-ETL
* A data engineering project consisting of building an ETL pipeline using Apache Airflow and AWS (Amazon Web Services) with Python, Amazon S3 and EC2.
* I built an ETL process that extracts weather data from the Open Weather API, this is transformed and then loaded into a simple storage service (AWS s3 bucket).
* The extraction, transformation and loading of the data is done in airflow dags written in python code. the Apache Airflow itself is running on an EC2 instance (please see flowchart in repo). 
* The project is an automated process where the ETL pipeline runs everyday and the airflow dags are invoked - a csv file is then sent to the s3 bucket of the new transformed clean data.

I first created an EC2 instance where I configured the Airflow and python code. The python code consists of creating tasks for an Ariflow dag - and then multiple functions for the different tasks. The dag tasks involve 
* Using a httpsensor to check wheather the API query is ready and working
* Make an actual GET request to the API server with the request string with custom parameters
* Transforming the returned weather data object from the API
* Loading the transformed data object into an S3 bucket as a CSV file

An S3 bucket should also be created as a pre-requisite for which the clean transformed data can be loaded and stored in. This was done using cloudformation and a bash script via a YAML file as Infrastructure as Code (IaC).



I extract, transform the data in python with tasks on a dag within Apache Airflow - the Apache Airflow is running on an AWS EC2 instance (A virtual server)
