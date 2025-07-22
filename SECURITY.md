# Security

## CodeQL Analysis

This repository uses GitHub's CodeQL to perform static analysis for security vulnerabilities and code quality issues in our Python backend and React frontend.

### What is CodeQL?

CodeQL is GitHub's semantic code analysis engine that:
- Analyzes code as data
- Finds security vulnerabilities and code smells
- Supports Python, JavaScript, TypeScript, and many other languages
- Provides detailed explanations and fix suggestions

### Setup

The CodeQL analysis is automatically configured and runs:
- On every push to the `development` branch
- On every pull request to the `development` branch
- Weekly on Mondays at 15:00 UTC

### Configuration

The CodeQL analysis is configured in:
- `.github/workflows/codeql.yml` - GitHub Actions workflow
- `.github/codeql/codeql-config.yml` - Analysis configuration
- `.github/codeql/custom-queries/` - Custom security queries

### What CodeQL Checks For

#### Security Vulnerabilities
- **Prompt Injection** - AI model input vulnerabilities (TestMind-specific)
- **Cross-Site Scripting (XSS)** - API response vulnerabilities
- **Command Injection** - System call vulnerabilities
- **Path Traversal** - File access vulnerabilities
- **Authentication Bypass** - Authentication vulnerabilities
- **Authorization Issues** - Permission vulnerabilities
- **Data Exposure** - Sensitive data leaks
- **Insecure Deserialization** - Object deserialization vulnerabilities
- **CSRF** - Cross-Site Request Forgery
- **Open Redirect** - Redirect vulnerabilities
- **Information Disclosure** - Error message leaks
- **Hardcoded Credentials** - Embedded secrets
- **Weak Cryptography** - Insecure algorithms

> **Note:** SQL Injection checks are **excluded** from CodeQL analysis because this project does not use a database. See `.github/codeql/codeql-config.yml` for details.

#### Code Quality Issues
- Unused variables and imports
- Dead code
- Inconsistent coding patterns
- Potential null pointer exceptions
- Resource leaks

### Viewing Results

1. **GitHub Security Tab**: Go to your repository's Security tab to view all CodeQL alerts
2. **Pull Request Comments**: CodeQL will comment on PRs with any new issues found
3. **Security Dashboard**: View trends and manage security alerts

### Custom Queries

We've created custom queries specific to TestMind:
- **AI model input validation** - Prompt injection detection
- **API endpoint security** - Backend security analysis
- **Data handling security** - Sensitive data protection
- **Authentication/Authorization** - Access control validation

### Integration with Existing CI/CD

CodeQL runs alongside your existing `backend.yaml` CI/CD pipeline:
- **Parallel execution** - Doesn't block your existing tests
- **Separate reporting** - Security alerts in Security tab
- **Complementary analysis** - Focuses on security while CI/CD handles functionality

### Fixing Issues

When CodeQL finds an issue:
1. Review the detailed explanation provided
2. Check the suggested fix
3. Implement the fix following security best practices
4. Test your changes thoroughly
5. Update the PR with the fix

### Security Best Practices

#### For Python Backend (FastAPI)
- Always validate and sanitize user inputs using Pydantic models
- Use parameterized queries for database operations (not applicable here, but best practice)
- Implement proper authentication and authorization
- Log security events but avoid logging sensitive data
- Keep dependencies updated
- Use environment variables for secrets
- Implement rate limiting for AI endpoints

#### For React Frontend
- Sanitize user inputs before rendering
- Use React's built-in XSS protection
- Implement proper CORS policies
- Validate API responses
- Use HTTPS for all communications
- Avoid storing sensitive data in localStorage

#### For AI/ML Components (TestMind-specific)
- Validate and sanitize AI model inputs
- Implement rate limiting for AI endpoints
- Monitor for prompt injection attempts
- Secure API keys and credentials
- Implement proper error handling
- Validate AI model outputs

### Reporting Security Issues

If you find a security vulnerability:
1. **DO NOT** create a public issue
2. Email security@testmind.ai (if available) or contact the maintainers privately
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed before public disclosure

### Dependencies

Keep your dependencies updated:
```bash
# Python backend
cd backend
pip list --outdated
pip install -r requirements.txt --upgrade

# React frontend
cd frontend
npm audit
npm update
```

### Continuous Monitoring

- CodeQL runs automatically on all code changes to `development` branch
- Security alerts are reviewed regularly
- Dependencies are monitored for known vulnerabilities
- Security best practices are enforced through code review
- Integration with existing CI/CD pipeline

### Branch Strategy

- **Development Branch**: CodeQL analysis runs here
- **Feature Branches**: Analysis runs on PRs to development
- **Master Branch**: Protected by development branch analysis
