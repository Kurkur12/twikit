import mysql.connector

def get_connection(db_config):
    return mysql.connector.connect(**db_config)
