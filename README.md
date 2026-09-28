# DevSecOps AppSec Lab

A hands-on DevSecOps project demonstrating how application security controls can be integrated into a CI pipeline using GitHub Actions.

The project uses a small Python Flask application and deliberately introduced security issues to demonstrate detection, pipeline enforcement, remediation, and validation.

## Project Goals

This lab demonstrates:

- Static Application Security Testing (SAST)
- Software Composition Analysis (SCA)
- Secret scanning
- CI/CD security gates
- Vulnerability remediation
- Secure coding practices
- Shift-left security

## Architecture

    Developer Push / Pull Request
                |
                v
            GitHub
                |
                v
         GitHub Actions
                |
                v
       ---------------------
       |        |          |
       v        v          v
     Semgrep  pip-audit  Gitleaks
      SAST      SCA      Secrets
       |        |          |
       ---------------------
                |
                v
           Pass / Fail
                |
                v
           Remediation
                |
                v
            Re-run CI

## Technology Stack

- Python
- Flask
- SQLite
- Git
- GitHub
- GitHub Actions
- Semgrep
- pip-audit
- Gitleaks

## Application

The lab contains a small Flask application that allows a user to search for a username stored in a SQLite database.

Application flow:

    Browser
       |
       v
    Flask Application
       |
       v
    User Input
       |
       v
    SQLite Query
       |
       v
    Search Result

## CI/CD Security Pipeline

The GitHub Actions workflow runs automatically when:

- code is pushed to `main`
- a pull request targets `main`

The pipeline performs three security checks.

### 1. SAST with Semgrep

Semgrep scans the Python source code for insecure coding patterns.

An intentionally vulnerable SQL query was introduced:

    query = f"SELECT * FROM users WHERE username = '{username}'"
    users = conn.execute(query).fetchall()

Semgrep detected the SQL injection risk and the pipeline was configured to fail when blocking findings were present.

The vulnerability was remediated using a parameterized query:

    query = "SELECT * FROM users WHERE username = ?"
    users = conn.execute(query, (username,)).fetchall()

This ensures user-controlled input is treated as data rather than SQL syntax.

Semgrep also detected Flask running with `debug=True`, which was disabled in the final implementation.

### 2. SCA with pip-audit

`pip-audit` scans Python dependencies for known vulnerabilities.

A deliberately outdated version of `urllib3` was temporarily introduced.

The scan identified known vulnerabilities associated with the package version and caused the CI pipeline to fail.

The vulnerable dependency was then upgraded or removed and the scan was run again successfully.

The final application dependency is:

    Flask==3.1.3

### 3. Secret Scanning with Gitleaks

Gitleaks scans source code for exposed credentials and secrets.

A fake lab credential was deliberately hardcoded into the application and detected using a custom Gitleaks rule.

The pipeline failed when the secret was detected.

The hardcoded value was replaced with an environment-variable based approach:

    LAB_SECRET = os.getenv("LAB_SECRET")

This demonstrates why sensitive values should not be stored directly in source code.

In a real CI/CD environment, secrets could be supplied through a mechanism such as GitHub Actions Secrets.

## Security Findings and Remediation

| Area | Deliberate Issue | Tool | Remediation |
|---|---|---|---|
| SAST | SQL injection | Semgrep | Parameterized query |
| SAST | Flask debug mode | Semgrep | Disabled debug mode |
| SCA | Vulnerable dependency | pip-audit | Dependency upgrade/removal |
| Secrets | Hardcoded lab secret | Gitleaks | Environment variable |

## Security Gate Behaviour

    Security Finding
          |
          v
    Scanner Returns Failure
          |
          v
    GitHub Actions Step Fails
          |
          v
    Pipeline Fails
          |
          v
    Developer Remediates
          |
          v
    Pipeline Re-runs
          |
          v
    Clean Pipeline Passes

The project demonstrates the difference between simply reporting security findings and enforcing security policy.

Semgrep was configured with:

    semgrep scan --config=p/python --error

The `--error` option causes blocking findings to return a non-zero exit code.

GitHub Actions interprets that non-zero exit code as a failed step.

## SAST vs SCA

### SAST

Static Application Security Testing analyses application source code for insecure coding patterns.

Example:

    User-controlled input
            |
            v
    Unsafe SQL construction
            |
            v
    Potential SQL Injection

### SCA

Software Composition Analysis analyses third-party and open-source dependencies.

Example:

    requirements.txt
           |
           v
    Dependency Version
           |
           v
    Known Vulnerability Data
           |
           v
    Vulnerable Component Identified

SAST focuses primarily on application source code, while SCA focuses on third-party components and dependency risk.

## DevSecOps Concepts Demonstrated

- Shift-left security
- Automated security testing
- CI/CD security integration
- Security gates
- Developer feedback
- Vulnerability remediation
- Dependency risk management
- Secure secret handling
- Secure coding practices

Instead of performing security testing only at the end of development, security controls execute automatically as part of the development workflow.

## Running the Application

Create a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run the application:

    python app.py

The application runs locally at:

    http://127.0.0.1:5000

## Key Learning Outcomes

Through this project I gained hands-on experience with:

- Building GitHub Actions workflows
- Understanding triggers, jobs, steps, runners and actions
- Integrating security tooling into CI
- Using exit codes to enforce security gates
- Analysing SAST findings
- Understanding source-to-sink SQL injection behaviour
- Performing dependency vulnerability scanning
- Remediating vulnerable dependencies
- Detecting hardcoded secrets
- Using environment variables for sensitive configuration
- Validating remediation through automated security scans

## Enterprise Tool Mapping

| Lab Tool | Security Concept |
|---|---|
| Semgrep | SAST / secure code analysis |
| pip-audit | SCA / dependency vulnerability management |
| Gitleaks | Secret scanning |
| GitHub Actions | CI/CD automation |

Tools such as **Checkmarx**, **Black Duck**, and **Prisma Cloud** were not used directly in this lab.

The project demonstrates hands-on experience with the underlying AppSec and DevSecOps concepts that enterprise security platforms support.

## Project Status

Core CI security pipeline implemented and validated:

- SAST integrated and validated
- SCA integrated and validated
- Secret scanning integrated and validated
- Deliberate vulnerabilities detected
- Security gates demonstrated
- Findings remediated
- Final pipeline passing
