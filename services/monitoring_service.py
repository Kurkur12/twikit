from utils.database import get_connection
from config import db_config

def get_dashboard_stats():
    """Get global system statistics"""
    conn = None
    cursor = None
    stats = {}
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Total Tweets
        cursor.execute("SELECT COUNT(*) as total FROM tweets")
        stats['total_tweets'] = cursor.fetchone()['total']
        
        # Success vs Failed (Last 24h)
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count
            FROM scraping_logs 
            WHERE executed_at >= NOW() - INTERVAL 1 DAY
        """)
        counts = cursor.fetchone()
        stats['today_success'] = counts['success_count'] or 0
        stats['today_failed'] = counts['failed_count'] or 0
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        stats = {'error': str(e)}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return stats

def get_account_health():
    """Get status of all accounts"""
    conn = None
    cursor = None
    accounts = []
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT username, status, last_used, rate_limit_reset 
            FROM accounts 
            ORDER BY last_used DESC
        """)
        accounts = cursor.fetchall()
        
    except Exception as e:
        print(f"Error getting accounts: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return accounts

def get_recent_logs(limit=10):
    """Get recent activity logs"""
    conn = None
    cursor = None
    logs = []
    
    try:
        conn = get_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT account_username, status, message, tweets_count, executed_at 
            FROM scraping_logs 
            ORDER BY executed_at DESC 
            LIMIT %s
        """, (limit,))
        logs = cursor.fetchall()
        
    except Exception as e:
        print(f"Error getting logs: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return logs
