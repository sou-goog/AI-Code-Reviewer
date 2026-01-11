#!/bin/bash
# Script to remove sensitive data from git history

echo "⚠️  REMOVING API KEY FROM GIT HISTORY"
echo "This will rewrite git history. Make sure you've backed up!"
echo ""

# Using git filter-repo (recommended method)
# Install: pip install git-filter-repo

git filter-repo --replace-text <(echo "AIzaSyDrdf_bTfsJ57DBsgSWzUXzcL-qfDTFPCk==>***REMOVED***")

echo "✅ API key removed from history"
echo ""
echo "NEXT STEPS:"
echo "1. Force push to GitHub: git push origin --force --all"
echo "2. Force push tags: git push origin --force --tags"
echo "3. REVOKE the old API key at https://aistudio.google.com/app/apikey"
echo "4. Generate a NEW API key"
