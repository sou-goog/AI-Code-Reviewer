"""
Repository settings and management endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from github_db import save_repo_settings, get_github_integration, is_auto_review_enabled, get_repo_pr_reviews

router = APIRouter(prefix="/repos", tags=["Repository Management"])


class RepoSettingsUpdate(BaseModel):
    repo_full_name: str
    auto_review_enabled: bool
    review_config: Optional[dict] = None


@router.post("/settings")
async def update_repo_settings(settings: RepoSettingsUpdate):
    """Update repository settings"""
    try:
        # Get integration ID from username (simplified for now)
        # TODO: Get from session/auth token
        integration_id = 1  # Placeholder
        
        save_repo_settings(
            integration_id=integration_id,
            repo_full_name=settings.repo_full_name,
            auto_review_enabled=settings.auto_review_enabled,
            review_config=settings.review_config
        )
        
        return {
            "success": True,
            "repo": settings.repo_full_name,
            "auto_review": settings.auto_review_enabled
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings/{repo_full_name:path}")
async def get_repo_settings(repo_full_name: str):
    """Get repository settings"""
    try:
        enabled = is_auto_review_enabled(repo_full_name)
        
        return {
            "repo": repo_full_name,
            "auto_review_enabled": enabled
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{repo_full_name:path}/reviews")
async def get_repo_reviews(repo_full_name: str, limit: int = Query(50, le=100)):
    """Get PR reviews for a repository"""
    try:
        reviews = get_repo_pr_reviews(repo_full_name, limit)
        
        return {
            "repo": repo_full_name,
            "reviews": reviews,
            "count": len(reviews)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
