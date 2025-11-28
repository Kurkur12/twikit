from utils.database import get_connection
from mysql.connector import Error
from datetime import datetime

def get_active_account(db_config):
    """Get a random active account from data_login table"""
    conn = None
    cursor = None
    account = None
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT * FROM data_login 
        WHERE valid = 1
        ORDER BY RAND()
        LIMIT 1
        """
        
        cursor.execute(query)
        account = cursor.fetchone()
            
    except Error as e:
        print(f"Error getting active account: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return account

def update_account_status(db_config, name, valid_status):
    """Update account valid status in data_login table"""
    conn = None
    cursor = None
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "UPDATE data_login SET valid = %s WHERE name = %s"
        cursor.execute(query, (valid_status, name))
        conn.commit()
        print(f"Updated account {name} valid status to {valid_status}")
        
    except Error as e:
        print(f"Error updating account status: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_account(db_config, name, password):
    """Helper to add account to data_login table"""
    conn = None
    cursor = None
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "INSERT IGNORE INTO data_login (name, password, valid) VALUES (%s, %s, 1)"
        cursor.execute(query, (name, password))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error adding account: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def check_username_exists(db_config, name):
    """Check if a username exists in the data_login table"""
    conn = None
    cursor = None
    exists = False
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "SELECT 1 FROM data_login WHERE name = %s"
        cursor.execute(query, (name,))
        exists = cursor.fetchone() is not None
        
    except Error as e:
        print(f"Error checking username: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    return exists
