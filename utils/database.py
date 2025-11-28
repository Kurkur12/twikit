import mysql.connector
from mysql.connector import Error

def get_connection(db_config):
    return mysql.connector.connect(**db_config)

def init_db(db_config):
    """Initialize database tables from schema.sql"""
    conn = None
    cursor = None
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        with open('schema.sql', 'r') as f:
            schema = f.read()
            
        commands = schema.split(';')
        for command in commands:
            if command.strip():
                cursor.execute(command)
        
        conn.commit()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def save_tweets(db_config, tweets):
    """Save a list of tweets to the database"""
    if not tweets:
        return 0
        
    conn = None
    cursor = None
    saved_count = 0
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = """
        INSERT IGNORE INTO tweets (
            id, created_at_datetime, user_id, user_name, user_screen_name, 
            text, lang, retweet_count, favorite_count, reply_count, 
            quote_count, view_count, place_id, place_name, place_full_name, 
            place_country, place_country_code, url
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        values = []
        for t in tweets:
            val = (
                t.get('id'), t.get('created_at_datetime'), t.get('user_id'), t.get('user_name'), t.get('user_screen_name'),
                t.get('text'), t.get('lang'), t.get('retweet_count', 0), t.get('favorite_count', 0), t.get('reply_count', 0),
                t.get('quote_count', 0), t.get('view_count', 0), t.get('place_id'), t.get('place_name'), t.get('place_full_name'),
                t.get('place_country'), t.get('place_country_code'), t.get('url')
            )
            values.append(val)
            
        cursor.executemany(query, values)
        conn.commit()
        saved_count = cursor.rowcount
        
    except Error as e:
        print(f"Error saving tweets: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return saved_count

def log_activity(db_config, username, status, message, tweets_count=0):
    """Log scraping activity"""
    conn = None
    cursor = None
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO scraping_logs (account_username, status, message, tweets_count) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, status, message, tweets_count))
        conn.commit()
        
    except Error as e:
        print(f"Error logging activity: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
