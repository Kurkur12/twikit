from utils.database import get_connection
from mysql.connector import Error
from datetime import datetime

def get_active_account(db_config):
    """Get a random active account that is not rate limited"""
    conn = None
    cursor = None
    account = None
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT * FROM accounts 
        WHERE status = 'active' 
        AND (rate_limit_reset IS NULL OR rate_limit_reset < NOW())
        ORDER BY last_used ASC 
        LIMIT 1
        """
        
        cursor.execute(query)
        account = cursor.fetchone()
        
        if account:
            update_query = "UPDATE accounts SET last_used = NOW() WHERE id = %s"
            cursor.execute(update_query, (account['id'],))
            conn.commit()
            
    except Error as e:
        print(f"Error getting active account: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return account

def update_account_status(db_config, username, status, rate_limit_reset=None):
    """Update account status (e.g. to 'rate_limited' or 'auth_failed')"""
    conn = None
    cursor = None
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "UPDATE accounts SET status = %s, rate_limit_reset = %s WHERE username = %s"
        cursor.execute(query, (status, rate_limit_reset, username))
        conn.commit()
        print(f"Updated account {username} status to {status}")
        
    except Error as e:
        print(f"Error updating account status: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_account(db_config, username, password, email=None):
    """Helper to add account to DB"""
    conn = None
    cursor = None
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "INSERT IGNORE INTO accounts (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error adding account: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def check_username_exists(db_config, username):
    """Check if a username exists in the database"""
    conn = None
    cursor = None
    exists = False
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "SELECT 1 FROM accounts WHERE username = %s"
        cursor.execute(query, (username,))
        exists = cursor.fetchone() is not None
        
    except Error as e:
        print(f"Error checking username: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    return exists
