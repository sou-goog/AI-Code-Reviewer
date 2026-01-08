from typing import Optional

import git


def get_staged_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of staged changes in the given repository path.
    """
    try:
        repo = git.Repo(repo_path)
        
        if repo.head.is_valid():
             diff = repo.git.diff("--cached")
        else:
             diff = repo.git.diff("--cached")
             
        if not diff:
            return None
        return diff
    except git.InvalidGitRepositoryError:
        print("Error: Not a valid git repository.")
        return None
    except Exception as e:
        print(f"Error getting diff: {e}")
        return None

def get_uncommitted_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of all uncommitted changes (staged + unstaged).
    """
    try:
        repo = git.Repo(repo_path)
        diff = repo.git.diff("HEAD")
        
        if not diff:
            return None
        return diff
    except Exception as e:
        print(f"Error getting diff: {e}")
        return None

def get_last_commit_diff(repo_path: str = ".") -> Optional[str]:
    """
    Returns the diff of the last commit.
    """
    try:
        repo = git.Repo(repo_path)
        diff = repo.git.diff("HEAD~1", "HEAD")
        
        if not diff:
            return None
        return diff
    except Exception as e:
        print(f"Error getting diff: {e}")
        return None
