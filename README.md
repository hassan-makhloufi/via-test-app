# via-test-app

⚠️ **Intentionally vulnerable application — for security-scanner testing only. Never deploy it.**

Test target for the Vulnerability Intelligence Agent. It contains on purpose:

| Category | Where | Detected by |
|----------|-------|-------------|
| Vulnerable Python dependencies | `requirements.txt` | Snyk, Trivy |
| Vulnerable npm dependencies | `package.json`, `package-lock.json` | Snyk, Trivy |
| SQL injection | `app.py` → `/user` | Semgrep, Snyk Code |
| OS command injection | `app.py` → `/ping` | Semgrep, Snyk Code |
| Unsafe YAML deserialization | `app.py` → `/import` | Semgrep |
| Hard-coded secrets (fake values) | `app.py`, `config.yaml` | Semgrep, Trivy |
| Flask debug mode | `app.py` | Semgrep |
| Insecure container | `Dockerfile` (old base image, runs as root) | Trivy, Semgrep |

All credentials in this repository are fake.

## Branch `fix/all` — remediated version

| Issue | Fix |
|-------|-----|
| Vulnerable dependencies (incl. Log4Shell / Spring4Shell, CISA KEV) | Upgraded to current releases |
| SQL injection | Parameterized query (`?`) |
| Command injection | IP validation + `subprocess` with an argument list, no shell |
| Unsafe YAML | `yaml.safe_load` |
| Hard-coded secrets | Read from environment variables |
| Debug mode | Disabled, bound to `127.0.0.1` |
| Insecure container | `python:3.13-slim`, non-root user, explicit `COPY` |

Merge `fix/all` into `main`, then **Re-scan**: the security gate goes from FAIL to PASS.
