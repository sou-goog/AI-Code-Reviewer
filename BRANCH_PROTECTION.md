# 🔒 Branch Protection Guide

## Overview
Protecting your `main` branch is a critical security practice that prevents accidental force pushes, deletions, and ensures code quality through required status checks before merging.

## Why Protect the Main Branch?

✅ **Prevents accidental force pushes** that could overwrite history  
✅ **Requires pull requests** for all changes (no direct pushes)  
✅ **Enforces code review** before merging  
✅ **Requires status checks** (tests, linting) to pass  
✅ **Prevents branch deletion** by unauthorized users  

## Step-by-Step Setup

### 1. Navigate to Branch Protection Settings

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/AI-Code-Reviewer`
2. Click **Settings** (top menu)
3. Click **Branches** (left sidebar)
4. Under **Branch protection rules**, click **Add rule** or **Edit** if a rule exists

### 2. Configure Branch Protection Rule

#### Basic Protection (Recommended Minimum)

1. **Branch name pattern**: Enter `main` (or `master` if that's your default branch)

2. **Protect matching branches**: Check these options:

   ✅ **Require a pull request before merging**
      - ✅ Require approvals: `1` (or more for team projects)
      - ✅ Dismiss stale pull request approvals when new commits are pushed
      - ✅ Require review from Code Owners (if you have a CODEOWNERS file)

   ✅ **Require status checks to pass before merging**
      - ✅ Require branches to be up to date before merging
      - Add required status checks:
        - `test` (if you have a test workflow)
        - `lint` (if you have a linting workflow)
        - `code-review` (your AI review workflow - optional but recommended)

   ✅ **Require conversation resolution before merging**
      - Ensures all PR comments are addressed

   ✅ **Do not allow bypassing the above settings**
      - Prevents even admins from bypassing (recommended for production)

   ✅ **Restrict who can push to matching branches**
      - Leave empty to allow all collaborators, or specify teams/users

   ✅ **Allow force pushes**
      - ❌ **UNCHECK THIS** - Prevents dangerous force pushes

   ✅ **Allow deletions**
      - ❌ **UNCHECK THIS** - Prevents accidental branch deletion

#### Advanced Options (Optional)

- **Require linear history**: Ensures a clean, linear git history
- **Include administrators**: Apply rules to admins too (recommended)
- **Allow specified actors to bypass**: Only if you need exceptions

### 3. Save the Rule

Click **Create** or **Save changes** at the bottom of the page.

## Recommended Configuration for This Project

For the AI Code Reviewer project, here's the recommended setup:

```
Branch: main

✅ Require a pull request before merging
   - Required approvals: 1
   - ✅ Dismiss stale approvals
   - ✅ Require review from Code Owners

✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date
   - Required checks:
     - test (pytest)
     - code-review (AI review workflow)

✅ Require conversation resolution before merging

✅ Do not allow bypassing the above settings

✅ Restrict pushes that create files larger than 100 MB

❌ Allow force pushes
❌ Allow deletions

✅ Include administrators
```

## Verification

After setting up branch protection:

1. Try to push directly to main:
   ```bash
   git checkout main
   echo "test" >> test.txt
   git add test.txt
   git commit -m "Test direct push"
   git push origin main
   ```
   
   **Expected**: Push should be rejected with message about branch protection

2. Create a pull request instead:
   ```bash
   git checkout -b test-branch
   echo "test" >> test.txt
   git add test.txt
   git commit -m "Test PR"
   git push origin test-branch
   ```
   
   Then create a PR on GitHub - it should require review and status checks.

## Status Checks Setup

To require your test suite to pass before merging:

1. Go to **Settings** → **Branches**
2. In your branch protection rule, under **Require status checks**
3. Click **Search for status checks**
4. Select:
   - `test` (if you have a test workflow)
   - `code-review` (your AI review workflow)

### Creating Status Check Workflows

If you don't have status checks yet, create `.github/workflows/test.yml`:

```yaml
name: Test

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting

### "Branch is protected" error when pushing
✅ **This is correct!** You must use pull requests now.

### Status checks not showing up
- Ensure workflows are in `.github/workflows/`
- Check that workflows run on `pull_request` events
- Verify workflow files are valid YAML

### Can't merge PR even after approval
- Check that all required status checks have passed
- Ensure branch is up to date with main
- Verify conversation resolution is enabled and all comments are resolved

### Need to bypass protection (emergency only)
- Only possible if "Include administrators" is unchecked
- Or if you're in the bypass list
- **Not recommended** - use hotfix branches instead

## Best Practices

1. **Always use feature branches** for changes
2. **Require at least 1 approval** for code review
3. **Keep status checks fast** (< 5 minutes)
4. **Use CODEOWNERS file** for automatic reviewer assignment
5. **Enable "Require up to date"** to prevent merge conflicts
6. **Include administrators** to prevent accidental bypasses

## Additional Resources

- [GitHub Docs: About Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Requiring Status Checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)

---

**⚠️ Important**: Once branch protection is enabled, you **cannot** directly push to main. All changes must go through pull requests. This is a security best practice!
