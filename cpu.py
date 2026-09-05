# Python script for high CPU alerts.
# Continuously samples CPU usage and sends an email each time it crosses a
# threshold.
#
# Setup:
#   pip install psutil
#
# Credentials are read from environment variables — never hardcode them here.
# In PowerShell (current session only):
#   $env:ALERT_SMTP_USER = "your_email@example.com"
#   $env:ALERT_SMTP_PASS = "your_app_password"
#
# If your email provider supports app passwords (e.g. Gmail), use one instead
# of your real account password, and rotate it if it's ever exposed.
#
# See README.md for the full list of supported environment variables.

import os
import smtplib
import sys
import time
from email.mime.text import MIMEText

import psutil

CPU_THRESHOLD = 80          # percent
CHECK_INTERVAL_SECONDS = 5  # how long to sample CPU usage over
POLL_INTERVAL_SECONDS = 60  # delay between checks, to avoid alert spam
SMTP_TIMEOUT_SECONDS = 10   # give up instead of hanging on a dead connection

SMTP_HOST = os.environ.get("ALERT_SMTP_HOST", "smtp.gmail.com")
SMTP_USER = os.environ.get("ALERT_SMTP_USER")
SMTP_PASS = os.environ.get("ALERT_SMTP_PASS")
# Falls back to SMTP_USER if ALERT_TO is unset OR set to an empty string.
ALERT_TO = os.environ.get("ALERT_TO") or SMTP_USER

try:
    SMTP_PORT = int(os.environ.get("ALERT_SMTP_PORT", "587"))
except ValueError:
    print(
        "Invalid ALERT_SMTP_PORT: must be an integer.",
        file=sys.stderr,
    )
    sys.exit(1)


def send_alert_email(cpu_percent: float) -> None:
    if not SMTP_USER or not SMTP_PASS:
        print("SMTP credentials not set (ALERT_SMTP_USER / ALERT_SMTP_PASS). Skipping email.")
        return

    recipients = [addr.strip() for addr in (ALERT_TO or "").split(",") if addr.strip()]
    if not recipients:
        print("No valid ALERT_TO recipients configured. Skipping email.")
        return

    subject = f"High CPU Alert: {cpu_percent:.1f}%"
    body = f"CPU usage is at {cpu_percent:.1f}%, which exceeds the {CPU_THRESHOLD}% threshold."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, recipients, msg.as_string())
        print(f"Alert email sent to {', '.join(recipients)}")
    except (smtplib.SMTPException, OSError) as e:
        print(f"Failed to send email: {e}", file=sys.stderr)


def check_cpu_once() -> float:
    cpu_percent = psutil.cpu_percent(interval=CHECK_INTERVAL_SECONDS)
    print(f"CPU usage: {cpu_percent:.1f}%")

    if cpu_percent >= CPU_THRESHOLD:
        print("HIGH CPU ALERT")
        send_alert_email(cpu_percent)
    else:
        print("CPU normal")

    return cpu_percent


def monitor_forever() -> None:
    while True:
        check_cpu_once()
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    monitor_forever()
