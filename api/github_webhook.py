"""
GitHub webhook handler for PR events.
"""
from fastapi import APIRouter, Request, HTTPException, Header
import hmac
import hashlib
import os
from typing import Optional
from github_client import GitHubClient, GitHubAppClient
from github_db import is_auto_review_enabled, save_pr_review
from src.llm_client import analyze_code_diff

router = APIRouter(prefix="/github", tags=["GitHub Webhooks"])

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """Handle GitHub webhook events"""
    
    # Read raw body for signature verification
    body = await request.body()
    payload = await request.json()
    
    # Verify webhook signature if secret is configured
    if WEBHOOK_SECRET and x_hub_signature_256:
        if not verify_signature(body, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Handle pull request events
    if x_github_event == "pull_request":
        return await handle_pull_request(payload)
    
    # Handle installation events
    elif x_github_event == "installation":
        return await handle_installation(payload)
    
    return {"status": "ignored", "event": x_github_event}


async def handle_pull_request(payload: dict):
    """Handle pull_request webhook events"""
    action = payload.get("action")
    
    # Only review on opened or synchronize (new commits)
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "action": action}
    
    pr = payload["pull_request"]
    repo = payload["repository"]
    repo_full_name = repo["full_name"]
    pr_number = pr["number"]
    
    # Check if auto-review is enabled for this repo
    if not is_auto_review_enabled(repo_full_name):
        return {"status": "auto_review_disabled", "repo": repo_full_name}
    
    try:
        # Get installation ID for API access
        installation_id = payload.get("installation", {}).get("id")
        
        if not installation_id:
            # Fallback: Try to use user token from database
            # For now, just return error
            raise HTTPException(
                status_code=400, 
                detail="No installation ID - GitHub App not installed"
            )
        
        # Initialize GitHub client with app token
        github_client = GitHubAppClient(installation_id)
        
        # Fetch PR diff
        diff = github_client.get_pr_diff(repo_full_name, pr_number)
        
        if not diff:
            return {"status": "no_changes", "pr": pr_number}
        
        # Get AI review
        review = analyze_code_diff(diff)
        
        # Post review comments
        commit_id = pr["head"]["sha"]
        github_client.post_review_comments(
            repo_full_name, 
            pr_number, 
            review, 
            commit_id
        )
        
        # Save to database
        save_pr_review(
            repo_full_name=repo_full_name,
            pr_number=pr_number,
            review_data=review,
            status="completed"
        )
        
        return {
            "status": "success",
            "repo": repo_full_name,
            "pr": pr_number,
            "issues_found": len(review.get("critical", [])) + len(review.get("warnings", []))
        }
    
    except Exception as e:
        # Save failed review
        save_pr_review(
            repo_full_name=repo_full_name,
            pr_number=pr_number,
            review_data={"error": str(e)},
            status="failed"
        )
        
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to review PR: {str(e)}"
        )


async def handle_installation(payload: dict):
    """Handle installation events (app installed/uninstalled)"""
    action = payload.get("action")
    installation = payload.get("installation", {})
    installation_id = installation.get("id")
    
    if action == "created":
        # App was installed - could save installation info
        return {
            "status": "installed",
            "installation_id": installation_id,
            "repos": len(installation.get("repositories", []))
        }
    
    elif action == "deleted":
        # App was uninstalled - could clean up data
        return {
            "status": "uninstalled",
            "installation_id": installation_id
        }
    
    return {"status": "ignored", "action": action}


def verify_signature(body: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    if not WEBHOOK_SECRET:
        return True  # Skip verification if no secret configured
    
    secret = WEBHOOK_SECRET.encode()
    expected = "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(expected, signature)


@router.get("/webhook/test")
async def test_webhook():
    """Test endpoint to verify webhook is accessible"""
    return {
        "status": "ok",
        "message": "Webhook endpoint is accessible",
        "secret_configured": bool(WEBHOOK_SECRET)
    }
