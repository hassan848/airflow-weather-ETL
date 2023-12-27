sudo apt-get update
sudo apt install python3-pip

# Create a virtual environment & activate it
sudo apt install python3.10-venv
python3 -m venv airflow_venv
source /home/ubuntu/airflow_venv/bin/activate

# Install the python packages from the requirements.txt
sudo pip install -r requirements.txt

# Begin Airflow & get AWS session token
airflow standalone
sudo apt  install awscli
aws configure
aws sts get-session-token