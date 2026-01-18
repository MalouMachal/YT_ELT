from airflow import DAG
import pendulum 
from datetime import datetime,timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

from datawarehouse.dwh import staging_table, core_table

#define the local timezone
local_tz= pendulum.timezone("Europe/Paris")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,1,1,tzinfo=local_tz),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs':1,
    'dagrun_timeout':timedelta(hours=1)
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    # 'end_date': datetime(2026,1,1,tzinfo=local_tz),
}

with DAG(
     dag_id="produce_json",
     default_args=default_args,
     description='DAG to produce JSON file with raw data',
     #start_date=datetime.datetime(2021, 1, 1),
     catchup=False,
     schedule="0 14 * * *",  #https://crontab.guru to hep define it
 ) as dag:

    #Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    #Define depedencies (order will the tasks run from left to right?)
    playlist_id >> video_ids >> extract_data >> save_to_json_task
    

with DAG(
     dag_id="update_db",
     default_args=default_args,
     description='DAG to process JSON file and insert data into both staging and core schemas',
     #start_date=datetime.datetime(2021, 1, 1),
     catchup=False,
     schedule="0 15 * * *",  #https://crontab.guru to hep define it
 ) as dag:

    #Define tasks
    update_staging = staging_table()
    update_core = core_table()

    #Define depedencies (order will the tasks run from left to right?)
    update_staging >> update_core
    
