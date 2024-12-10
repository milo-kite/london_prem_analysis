# Use an official Airflow image as the base image
FROM apache/airflow:2.7.0

# Set the working directory in the container
WORKDIR /opt/airflow

# Copy your requirements.txt to the container
COPY requirements.txt /opt/airflow/

# Install any additional dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code directory (including your DAGs, scripts, etc.) into the container

COPY code/* /opt/airflow/dags

RUN mkdir -p /opt/airflow/credentials
COPY credentials/* /opt/airflow/credentials

RUN mkdir -p /opt/airflow/data

RUN ls -al /opt/airflow/credentials

# Set the Airflow home directory (if you want to change it)
ENV AIRFLOW_HOME=/opt/airflow

# Initialize the database (you should run this once before starting the webserver and scheduler)
RUN airflow db init

# Expose the port the Airflow webserver will run on (default: 8080)
EXPOSE 8080

# Set the entrypoint and the command to start the webserver and scheduler
# Run both the webserver and scheduler in the container
CMD ["bash", "-c", "airflow webserver & airflow scheduler"]
