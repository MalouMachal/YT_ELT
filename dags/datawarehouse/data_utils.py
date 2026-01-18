from airflow.providers.postgres.hooks.postgres¶ import PostgresHook
from psycopg2.extras import RealdIDCursor 

table  = "yt_api"

def get_conn_cursor():
    hook = PostrgresHook(postgres_con_id="postgres_db_yt_elt",database="elt_db")     
    #arg1: we already define postgres_con_id in the .yaml that the connection URL can be writter as this 
            #env variable AIRFLOW_CONN_POSTGRES_DB_YT_ELT: 'postgresql://${ELT_DATABASE_USERNAME}:${ELT_DATABASE_PASSWORD}@${POSTGRES_CONN_HOST}:${POSTGRES_CONN_PORT}/${ELT_DATABASE_NAME}'
    #arg2 :we already define database in the .env : ELT_DATABASE_NAME=elt_db

    conn = hook.get_conn()
    cur = conn.cursor(curosr_factory=RealdIDCursor) 
    #arg1 : we use the cursor because it changes how the data is returned when exectue a query using the cursor
        # and the cursor in our case will return the data from SQL query as a python dictionary instead ot the default tuple
        #we dont need it right now but for example :
        #cur.execute("SELECT * FROM table")

    return conn,cur

def close_conn_cursor(con,cur):
    cur.close()
    conn.close()

def create_schema(schema):

    conn,cur= get_conn_cursor()

    scehma_sql= f"CREATE SCHEMA IF NOT EXISTS {schema};"

    cur.execute(schema_sql)

    conn.commit()

    close_conn_cursor(conn,cur)

#each table we'll have slightly different column so we need the following functions

def created_table(scehma):

    conn, cur get_conn_cursor()

    if schema == "staging":
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT   
                );
            """
    else:
        table_sql = f"""
                  CREATE TABLE IF NOT EXISTS {schema}.{table} (
                      "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                      "Video_Title" TEXT NOT NULL,
                      "Upload_Date" TIMESTAMP NOT NULL,
                      "Duration" TIME NOT NULL,
                      "Video_Type" VARCHAR(10) NOT NULL,
                      "Video_Views" INT,
                      "Likes_Count" INT,
                      "Comments_Count" INT    
                  ); 
              """

    cur.execute(table_sql)

    conn.commit()

    close_conn_cursor(conn, cur)


    #one last function has to get all the video IDs in either the staging or the correlat table
    #helpful when we come to loop thrgoug the rows of data inside the table so we can first define:

def get_video_ids(cur, schema):

    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall()    #we'll give a list of directionaries 
    
    #for example it will give [{'Video_ID ; 'abc123'},{'Video_ID ; 'xyz456'},{'Video_ID ; 'def789'}]

    video_ids = [row["Video_ID"] for row in ids]   #so we are going inside the video id key and extracting the value so an example return will be :

    #['abc123','xyz456','def789']

    return video_ids
