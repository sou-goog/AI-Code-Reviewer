"""
GitHub API client for repository and PR operations.
"""
import os
from github import Github, GithubIntegration
from typing import List, Dict, Optional

class GitHubClient:
    """GitHub API client wrapper"""
    
    def __init__(self, access_token: str):
        """Initialize with user access token"""
        self.client = Github(access_token)
    
    def get_pr_diff(self, repo_full_name: str, pr_number: int) -> str:
        """Get PR diff/changes"""
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            # Get all files changed in PR
            files = pr.get_files()
            
            # Combine diffs
            full_diff = ""
            for file in files:
                full_diff += f"\n--- {file.filename} ---\n"
                if file.patch:
                    full_diff += file.patch + "\n"
            
            return full_diff
        
        except Exception as e:
            raise Exception(f"Failed to fetch PR diff: {str(e)}")
    
    def get_pr_files(self, repo_full_name: str, pr_number: int) -> List[Dict]:
        """Get list of files changed in PR"""
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            files = pr.get_files()
            
            return [
                {
                    "filename": f.filename,
                    "status": f.status,
                    "additions": f.additions,
                    "deletions": f.deletions,
                    "changes": f.changes,
                    "patch": f.patch
                }
                for f in files
            ]
        
        except Exception as e:
            raise Exception(f"Failed to fetch PR files: {str(e)}")
    
    def post_pr_comment(self, repo_full_name: str, pr_number: int, body: str):
        """Post a comment on PR"""
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(body)
        
        except Exception as e:
            raise Exception(f"Failed to post comment: {str(e)}")
    
    def post_review_comments(self, repo_full_name: str, pr_number: int, 
                            review_data: Dict, commit_id: str):
        """Post inline review comments on PR"""
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            # Create review summary comment
            summary = self._format_review_summary(review_data)
            
            # For now, just post a summary comment
            # TODO: Add inline comments when we can map issues to line numbers
            pr.create_issue_comment(summary)
            
            return True
        
        except Exception as e:
            raise Exception(f"Failed to post review: {str(e)}")
    
    def _format_review_summary(self, review_data: Dict) -> str:
        """Format review data as markdown comment"""
        critical = review_data.get('critical', [])
        warnings = review_data.get('warnings', [])
        suggestions = review_data.get('suggestions', [])
        positive = review_data.get('positive', [])
        summary = review_data.get('summary', '')
        
        comment = "## 🤖 AI Code Review\n\n"
        
        # Summary
        if summary:
            comment += f"**Summary:** {summary}\n\n"
        
        # Stats
        comment += "### 📊 Review Stats\n\n"
        comment += f"- 🚨 Critical Issues: **{len(critical)}**\n"
        comment += f"- ⚠️ Warnings: **{len(warnings)}**\n"
        comment += f"- 💡 Suggestions: **{len(suggestions)}**\n"
        comment += f"- ✅ Positive Notes: **{len(positive)}**\n\n"
        
        # Critical issues
        if critical:
            comment += "### 🚨 Critical Issues\n\n"
            for i, issue in enumerate(critical, 1):
                comment += f"{i}. {issue}\n\n"
        
        # Warnings
        if warnings:
            comment += "### ⚠️ Warnings\n\n"
            for i, issue in enumerate(warnings, 1):
                comment += f"{i}. {issue}\n\n"
        
        # Suggestions
        if suggestions:
            comment += "### 💡 Suggestions\n\n"
            for i, issue in enumerate(suggestions, 1):
                comment += f"{i}. {issue}\n\n"
        
        # Positive feedback
        if positive:
            comment += "### ✅ Positive Notes\n\n"
            for i, note in enumerate(positive, 1):
                comment += f"{i}. {note}\n\n"
        
        comment += "\n---\n*Powered by AI Code Reviewer - Free & Open Source*"
        
        return comment
    
    def get_user_repos(self) -> List[Dict]:
        """Get authenticated user's repositories"""
        try:
            repos = self.client.get_user().get_repos(sort='updated')
            
            return [
                {
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "description": repo.description,
                    "url": repo.html_url,
                    "language": repo.language,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None
                }
                for repo in repos[:100]  # Limit to 100
            ]
        
        except Exception as e:
            raise Exception(f"Failed to fetch repos: {str(e)}")


class GitHubAppClient:
    """GitHub App client for installation-based access"""
    
    def __init__(self, installation_id: int):
        """Initialize with GitHub App installation ID"""
        app_id = os.getenv("GITHUB_APP_ID")
        private_key = os.getenv("GITHUB_PRIVATE_KEY")
        
        if not app_id or not private_key:
            raise ValueError("GitHub App credentials not configured")
        
        integration = GithubIntegration(int(app_id), private_key)
        self.token = integration.get_access_token(installation_id).token
        self.client = Github(self.token)
    
    def get_pr_diff(self, repo_full_name: str, pr_number: int) -> str:
        """Get PR diff using app token"""
        client = GitHubClient(self.token)
        return client.get_pr_diff(repo_full_name, pr_number)
    
    def post_review_comments(self, repo_full_name: str, pr_number: int, 
                            review_data: Dict, commit_id: str):
        """Post review comments using app token"""
        client = GitHubClient(self.token)
        return client.post_review_comments(repo_full_name, pr_number, review_data, commit_id)
