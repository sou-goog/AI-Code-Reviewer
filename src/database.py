import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional


class ReviewDatabase:
    """Database for storing review history and analytics."""
    
    def __init__(self, db_path: str = "reviews.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    diff_type TEXT NOT NULL,
                    file_count INTEGER DEFAULT 0,
                    critical_count INTEGER DEFAULT 0,
                    warning_count INTEGER DEFAULT 0,
                    suggestion_count INTEGER DEFAULT 0,
                    review_text TEXT,
                    duration_seconds REAL DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    review_id INTEGER,
                    severity TEXT NOT NULL,
                    message TEXT,
                    file_path TEXT,
                    line_number INTEGER,
                    FOREIGN KEY (review_id) REFERENCES reviews(id)
                )
            """)
            
            conn.commit()
    
    def save_review(self, review_data: Dict) -> int:
        """Save a review to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO reviews (
                    diff_type, file_count, critical_count, 
                    warning_count, suggestion_count, review_text, duration_seconds
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                review_data.get('diff_type', 'unknown'),
                review_data.get('file_count', 0),
                review_data.get('critical_count', 0),
                review_data.get('warning_count', 0),
                review_data.get('suggestion_count', 0),
                review_data.get('review_text', ''),
                review_data.get('duration_seconds', 0)
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_total_reviews(self) -> int:
        """Get total number of reviews."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM reviews")
            return cursor.fetchone()[0]
    
    def get_total_issues(self) -> Dict[str, int]:
        """Get total issues by severity."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    SUM(critical_count) as critical,
                    SUM(warning_count) as warning,
                    SUM(suggestion_count) as suggestion
                FROM reviews
            """)
            row = cursor.fetchone()
            return {
                'critical': row[0] or 0,
                'warning': row[1] or 0,
                'suggestion': row[2] or 0
            }
    
    def get_recent_reviews(self, limit: int = 10) -> List[Dict]:
        """Get recent reviews."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM reviews 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_review_stats(self) -> Dict:
        """Get comprehensive review statistics."""
        stats = {
            'total_reviews': self.get_total_reviews(),
            'total_issues': self.get_total_issues(),
            'avg_duration': self._get_avg_duration(),
        }
        return stats
    
    def _get_avg_duration(self) -> float:
        """Get average review duration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT AVG(duration_seconds) FROM reviews")
            result = cursor.fetchone()[0]
            return round(result, 2) if result else 0.0
