ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

#Use global variable to define the airflow image we use (apache and versions)
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

#Define the airflow home variable
ENV AIRFLOW_HOME=/opt/airflow 

#To copy the requirements.txt file from our local directory to the root dir. of the Docker image file system
COPY requirements.txt /

#nstalls the specified version of airflow and the packages in requirements.txt 
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt