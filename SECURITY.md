# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please email the maintainers directly instead of opening a public issue.

**Please include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We take all security vulnerabilities seriously and will respond within 48 hours.

## Security Best Practices

When using this tool:
- **Never commit API keys to version control** - Always use environment variables or GitHub Secrets
- **If an API key is exposed**: Immediately revoke it and generate a new one
- Use environment variables or secrets management (GitHub Secrets for Actions)
- Review the code before deploying to production
- Keep dependencies updated
- Use HTTPS for all external connections
- Add `.env` files to `.gitignore` (already included)
- Never hardcode credentials in documentation or code

### If Your API Key Was Exposed

1. **Immediately revoke the exposed key**:
   - Go to https://aistudio.google.com/app/apikey
   - Delete the compromised key

2. **Generate a new API key**:
   - Create a new key at https://aistudio.google.com/app/apikey
   - Update it in your environment variables or GitHub Secrets

3. **Remove from Git History** (if committed):
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner to remove from history
   # Or consider the key compromised and just revoke it
   ```

4. **Update all services** using the old key
