import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

def get_db_connection():
    """Get PostgreSQL database connection"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def save_review(filename: str, language: str, review_data: dict, duration: float):
    """Save review to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO reviews (
                filename, language, timestamp,
                critical_count, warning_count, suggestion_count, positive_count,
                duration, summary,
                critical_issues, warning_issues, suggestion_issues, positive_issues
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            filename,
            language,
            datetime.now(),
            len(review_data.get('critical', [])),
            len(review_data.get('warnings', [])),
            len(review_data.get('suggestions', [])),
            len(review_data.get('positive', [])),
            duration,
            review_data.get('summary', ''),
            json.dumps(review_data.get('critical', [])),
            json.dumps(review_data.get('warnings', [])),
            json.dumps(review_data.get('suggestions', [])),
            json.dumps(review_data.get('positive', []))
        ))
        
        review_id = cursor.fetchone()['id']
        conn.commit()
        return review_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_reviews():
    """Get all reviews from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, filename, language, timestamp,
                   critical_count, warning_count, suggestion_count, positive_count,
                   duration, summary
            FROM reviews
            ORDER BY timestamp DESC
        """)
        
        reviews = cursor.fetchall()
        return reviews
    
    finally:
        cursor.close()
        conn.close()

def get_review_stats():
    """Get statistics from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_reviews,
                SUM(critical_count) as total_critical,
                SUM(warning_count) as total_warnings,
                SUM(suggestion_count) as total_suggestions,
                AVG(duration) as avg_duration
            FROM reviews
        """)
        
        stats = cursor.fetchone()
        return stats
    
    finally:
        cursor.close()
        conn.close()
