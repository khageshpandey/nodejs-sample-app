# nodejs-sample-app

Minimal Express REST API used as a sandbox for local dev, CI/CD, and container/K8s testing.

## Run locally
```bash
npm install
npm run dev
```

## Run tests
```bash
npm test
```

## Build and run with Docker
```bash
docker build -t nodejs-sample-app .
docker run -p 3000:3000 nodejs-sample-app
```

## Endpoints
- `GET /` - basic status message
- `GET /health` - liveness probe
- `GET /health/ready` - readiness probe
- `GET /users` - hardcoded list of sample users

## CPU alert script (cpu.py)
Standalone utility that polls CPU usage and emails an alert when it crosses
a threshold. Not part of the Express app.

```bash
pip install psutil
python cpu.py
```

Configured entirely via environment variables — never hardcode credentials
in `cpu.py`:

| Variable | Required | Default | Description |
|---|---|---|---|
| `ALERT_SMTP_HOST` | no | `smtp.gmail.com` | SMTP server hostname |
| `ALERT_SMTP_PORT` | no | `587` | SMTP server port (must be an integer) |
| `ALERT_SMTP_USER` | yes, to send email | - | SMTP login / "From" address |
| `ALERT_SMTP_PASS` | yes, to send email | - | SMTP password or app password |
| `ALERT_TO` | no | value of `ALERT_SMTP_USER` | Comma-separated recipient address(es) |

If `ALERT_SMTP_USER`/`ALERT_SMTP_PASS` aren't set, the script still runs and
logs CPU usage, it just skips sending email.
