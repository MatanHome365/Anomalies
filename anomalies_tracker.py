# pass
from configuration import db_connections as db
from datetime import date
import datetime
import json


def adding_rows(rows, id_name, anomaly_type_id, anomaly_type_name, handling_by, start_date, days_unresolved, key_reference_id):
    conn = db.create_postgres_connection()
    cursor = conn.cursor()
    for index, row in rows.iterrows():
        id = row[id_name]
        reference_id = row[key_reference_id]
        postgres_insert_query = """ INSERT INTO "Anomalies_Tracker" 
        (anomaly_id, anomaly_type_id, anomaly_type_name, start_date, handled_date, handling_by, json_fields,
         days_unresolved, reference_id) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (id, anomaly_type_id, anomaly_type_name, start_date, None, handling_by,
                            json.dumps(dict(row)), days_unresolved, reference_id)
        cursor.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    conn.close()


def update_rows(rows, id_name, today_date):
    conn = db.create_postgres_connection()
    cursor = conn.cursor()
    for index, row in rows.iterrows():
        id = row[id_name]
        start_date = row['start_date']
        days_unresolved = (today_date - start_date).days
        query = """ UPDATE "Anomalies_Tracker" SET days_unresolved = %s where anomaly_id = %s """
        cursor.execute(query, (days_unresolved, id))

    conn.commit()
    conn.close()


def close_rows(rows, id_name, yesterday_date):
    conn = db.create_postgres_connection()
    cursor = conn.cursor()
    for index, row in rows.iterrows():
        id = row[id_name]
        query = """ UPDATE "Anomalies_Tracker" SET handled_date = %s where anomaly_id = %s """
        cursor.execute(query, (yesterday_date, id))

    conn.commit()
    conn.close()


def close_all(anomaly_type_id):
    conn = db.create_postgres_connection()
    cursor = conn.cursor()
    today_date = date.today()
    yesterday_date = today_date - datetime.timedelta(days=1)
    query = ''' select * from "Anomalies_Tracker" where handled_date is null and anomaly_type_id = ''' + str(anomaly_type_id)
    anomalies_tracker_table = db.importDataFromPG(query)
    for index, row in anomalies_tracker_table.iterrows():
        id = row['anomaly_id']
        query = """ UPDATE "Anomalies_Tracker" SET handled_date = %s where anomaly_id = %s and handled_date is null """
        cursor.execute(query, (yesterday_date, id))

    conn.commit()
    conn.close()


def tracking_anomalies(df, id_name, anomaly_type_id, anomaly_type_name, handling_by, key_reference_id):
    anomaly_id = 'anomaly_id'
    df[id_name] = df[id_name].astype("string")
    today_date = date.today()
    yesterday_date = today_date - datetime.timedelta(days=1)
    query = ''' select * from "Anomalies_Tracker" where handled_date is null and anomaly_type_id = ''' + str(anomaly_type_id)
    anomalies_tracker_table = db.importDataFromPG(query)
    rows_to_update = anomalies_tracker_table[anomalies_tracker_table[anomaly_id].isin(df[id_name])]
    rows_to_close = anomalies_tracker_table[~anomalies_tracker_table[anomaly_id].isin(rows_to_update[anomaly_id])]
    rows_to_create = df[~df[id_name].isin(anomalies_tracker_table[anomaly_id])]

    update_rows(rows_to_update, anomaly_id, today_date)
    close_rows(rows_to_close, anomaly_id, yesterday_date)
    adding_rows(rows_to_create, id_name, anomaly_type_id, anomaly_type_name, handling_by, today_date, 0, key_reference_id)