import logging
from typing import Optional

import git

logger = logging.getLogger(__name__)


def get_staged_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of staged changes in the given repository path.
    
    Args:
        repo_path: Path to git repository (default: current directory)
        
    Returns:
        Git diff string or None if no changes or error
    """
    try:
        repo = git.Repo(repo_path)
        
        if repo.head.is_valid():
            diff = repo.git.diff("--cached")
        else:
            # For new repos without commits, return empty diff
            diff = repo.git.diff("--cached")
             
        if not diff:
            logger.debug("No staged changes found")
            return None
        return diff
    except git.InvalidGitRepositoryError:
        logger.error(f"Not a valid git repository: {repo_path}")
        return None
    except Exception as e:
        logger.error(f"Error getting staged diff: {e}", exc_info=True)
        return None

def get_uncommitted_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of all uncommitted changes (staged + unstaged).
    
    Args:
        repo_path: Path to git repository (default: current directory)
        
    Returns:
        Git diff string or None if no changes or error
    """
    try:
        repo = git.Repo(repo_path)
        diff = repo.git.diff("HEAD")
        
        if not diff:
            logger.debug("No uncommitted changes found")
            return None
        return diff
    except git.InvalidGitRepositoryError:
        logger.error(f"Not a valid git repository: {repo_path}")
        return None
    except Exception as e:
        logger.error(f"Error getting uncommitted diff: {e}", exc_info=True)
        return None

def get_last_commit_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of the last commit.
    
    Args:
        repo_path: Path to git repository (default: current directory)
        
    Returns:
        Git diff string or None if no commits or error
    """
    try:
        repo = git.Repo(repo_path)
        
        # Check if there are any commits
        if len(list(repo.iter_commits())) == 0:
            logger.debug("No commits found in repository")
            return None
            
        diff = repo.git.diff("HEAD~1", "HEAD")
        
        if not diff:
            logger.debug("Last commit has no changes")
            return None
        return diff
    except git.InvalidGitRepositoryError:
        logger.error(f"Not a valid git repository: {repo_path}")
        return None
    except Exception as e:
        logger.error(f"Error getting last commit diff: {e}", exc_info=True)
        return None
