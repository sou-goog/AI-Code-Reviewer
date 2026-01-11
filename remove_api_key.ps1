# PowerShell script to remove API key from git history

Write-Host "⚠️  REMOVING API KEY FROM GIT HISTORY" -ForegroundColor Red
Write-Host "This will rewrite git history. Backing up current state..." -ForegroundColor Yellow
Write-Host ""

# Backup current branch
git branch backup-before-cleanup

# Use BFG Repo-Cleaner (fastest method for Windows)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
# Or use git filter-repo

Write-Host "Creating replacement file..." -ForegroundColor Cyan
"AIzaSyDrdf_bTfsJ57DBsgSWzUXzcL-qfDTFPCk" | Out-File -FilePath "api-key-to-remove.txt" -Encoding UTF8

# Method 1: Using BFG (recommended - faster)
Write-Host "`nMethod 1: Using BFG Repo-Cleaner" -ForegroundColor Green
Write-Host "Download: https://rtyley.github.io/bfg-repo-cleaner/" -ForegroundColor Yellow
Write-Host "Run: java -jar bfg.jar --replace-text api-key-to-remove.txt ." -ForegroundColor White
Write-Host "Then: git reflog expire --expire=now --all && git gc --prune=now --aggressive" -ForegroundColor White

Write-Host "`n--- OR ---`n" -ForegroundColor Magenta

# Method 2: Using git filter-branch (slower but built-in)
Write-Host "Method 2: Using git filter-branch" -ForegroundColor Green
Write-Host "Run the following commands:" -ForegroundColor Yellow
Write-Host @"
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch --all' \
  --prune-empty --tag-name-filter cat -- --all

git filter-branch --force --tree-filter \
  'find . -type f -exec sed -i "s/AIzaSyDrdf_bTfsJ57DBsgSWzUXzcL-qfDTFPCk/***REMOVED***/g" {} \;' \
  HEAD

git reflog expire --expire=now --all
git gc --prune=now --aggressive
"@ -ForegroundColor White

Write-Host "`n✅ After cleanup, run:" -ForegroundColor Green
Write-Host "git push origin --force --all" -ForegroundColor Cyan
Write-Host "git push origin --force --tags" -ForegroundColor Cyan

Write-Host "`n🔐 CRITICAL: Revoke old API key!" -ForegroundColor Red
Write-Host "1. Go to: https://aistudio.google.com/app/apikey" -ForegroundColor Yellow
Write-Host "2. DELETE key: AIzaSyDrdf_bTfsJ57DBsgSWzUXzcL-qfDTFPCk" -ForegroundColor Yellow
Write-Host "3. Generate NEW key" -ForegroundColor Yellow
Write-Host "4. Update GitHub Secret with new key" -ForegroundColor Yellow
