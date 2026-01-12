"""
GitHub OAuth authentication flow.
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import os
import requests
from github_db import save_github_integration

router = APIRouter(prefix="/auth/github", tags=["GitHub Auth"])

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

@router.get("/login")
async def github_login():
    """Initiate GitHub OAuth flow"""
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")
    
    redirect_uri = f"{FRONTEND_URL}/auth/github/callback"
    state = "random_state_string"  # TODO: Generate secure state
    
    auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={GITHUB_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"scope=repo user:email&"
        f"state={state}"
    )
    
    return {"auth_url": auth_url}

@router.get("/callback")
async def github_callback(code: str = Query(...), state: str = Query(None)):
    """Handle GitHub OAuth callback"""
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")
    
    # Exchange code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        },
        headers={"Accept": "application/json"}
    )
    
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange code for token")
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="No access token in response")
    
    # Get user information
    user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
    )
    
    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")
    
    user_data = user_response.json()
    
    # Save to database
    try:
        integration_id = save_github_integration(
            github_id=user_data["id"],
            username=user_data["login"],
            access_token=access_token,
            refresh_token=token_data.get("refresh_token")
        )
        
        return {
            "success": True,
            "user": {
                "id": user_data["id"],
                "username": user_data["login"],
                "avatar_url": user_data.get("avatar_url"),
                "name": user_data.get("name")
            },
            "integration_id": integration_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save integration: {str(e)}")

@router.get("/repos")
async def get_user_repos(username: str = Query(...)):
    """Get user's GitHub repositories"""
    from github_db import get_github_integration
    
    integration = get_github_integration(username)
    if not integration:
        raise HTTPException(status_code=404, detail="GitHub integration not found")
    
    access_token = integration['access_token']
    
    # Fetch repositories
    repos_response = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        },
        params={
            "sort": "updated",
            "per_page": 100
        }
    )
    
    if repos_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch repositories")
    
    repos_data = repos_response.json()
    
    # Format response
    repos = [
        {
            "id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "private": repo["private"],
            "description": repo.get("description"),
            "url": repo["html_url"],
            "language": repo.get("language"),
            "updated_at": repo["updated_at"]
        }
        for repo in repos_data
    ]
    
    return {"repos": repos}
