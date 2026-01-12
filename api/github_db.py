"""
GitHub database operations for Supabase integration.
"""
import os
from database import get_db_connection
import json
from datetime import datetime

def save_github_integration(github_id: int, username: str, access_token: str, 
                            refresh_token: str = None, installation_id: int = None) -> int:
    """Save GitHub integration to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Use github_id as user_id for now
        user_id = f"github_{github_id}"
        
        cursor.execute("""
            INSERT INTO github_integrations (
                user_id, github_id, github_username, access_token, 
                refresh_token, installation_id, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                github_username = EXCLUDED.github_username,
                access_token = EXCLUDED.access_token,
                refresh_token = EXCLUDED.refresh_token,
                installation_id = EXCLUDED.installation_id,
                updated_at = EXCLUDED.updated_at
            RETURNING id
        """, (
            user_id,
            github_id,
            username,
            access_token,
            refresh_token,
            installation_id,
            datetime.now()
        ))
        
        integration_id = cursor.fetchone()['id']
        conn.commit()
        return integration_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_github_integration(github_username: str) -> dict:
    """Get GitHub integration by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM github_integrations 
            WHERE github_username = %s
        """, (github_username,))
        
        return cursor.fetchone()
    
    finally:
        cursor.close()
        conn.close()

def save_repo_settings(integration_id: int, repo_full_name: str, 
                       auto_review_enabled: bool = True, 
                       review_config: dict = None) -> int:
    """Save repository settings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO repo_settings (
                integration_id, repo_full_name, auto_review_enabled, review_config
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_full_name)
            DO UPDATE SET
                auto_review_enabled = EXCLUDED.auto_review_enabled,
                review_config = EXCLUDED.review_config
            RETURNING id
        """, (
            integration_id,
            repo_full_name,
            auto_review_enabled,
            json.dumps(review_config or {})
        ))
        
        settings_id = cursor.fetchone()['id']
        conn.commit()
        return settings_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def is_auto_review_enabled(repo_full_name: str) -> bool:
    """Check if auto-review is enabled for repository"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT auto_review_enabled FROM repo_settings 
            WHERE repo_full_name = %s
        """, (repo_full_name,))
        
        result = cursor.fetchone()
        return result['auto_review_enabled'] if result else False
    
    finally:
        cursor.close()
        conn.close()

def save_pr_review(repo_full_name: str, pr_number: int, review_data: dict, 
                   github_review_id: int = None, status: str = 'completed') -> int:
    """Save PR review to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First, save the review to the reviews table
        from database import save_review
        review_id = save_review(
            filename=f"PR#{pr_number}",
            language="mixed",
            review_data=review_data,
            duration=0
        )
        
        # Then save the PR review reference
        cursor.execute("""
            INSERT INTO pr_reviews (
                repo_full_name, pr_number, review_id, 
                github_review_id, status, comments_posted
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            repo_full_name,
            pr_number,
            review_id,
            github_review_id,
            status,
            len(review_data.get('critical', [])) + len(review_data.get('warnings', []))
        ))
        
        pr_review_id = cursor.fetchone()['id']
        conn.commit()
        return pr_review_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_repo_pr_reviews(repo_full_name: str, limit: int = 50) -> list:
    """Get PR reviews for a repository"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT pr.*, r.summary, r.critical_count, r.warning_count
            FROM pr_reviews pr
            JOIN reviews r ON pr.review_id = r.id
            WHERE pr.repo_full_name = %s
            ORDER BY pr.created_at DESC
            LIMIT %s
        """, (repo_full_name, limit))
        
        return cursor.fetchall()
    
    finally:
        cursor.close()
        conn.close()
