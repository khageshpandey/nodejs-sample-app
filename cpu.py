# Python script for high CPU alerts.
# Sends an email when CPU usage crosses a threshold.
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

import os
import smtplib
import sys
import time
from email.mime.text import MIMEText

import psutil

CPU_THRESHOLD = 80          # percent
CHECK_INTERVAL_SECONDS = 5  # how long to sample CPU usage over

SMTP_HOST = os.environ.get("ALERT_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("ALERT_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("ALERT_SMTP_USER")
SMTP_PASS = os.environ.get("ALERT_SMTP_PASS")
ALERT_TO = os.environ.get("ALERT_TO", SMTP_USER)


def send_alert_email(cpu_percent: float) -> None:
    if not SMTP_USER or not SMTP_PASS:
        print("SMTP credentials not set (ALERT_SMTP_USER / ALERT_SMTP_PASS). Skipping email.")
        return

    subject = f"High CPU Alert: {cpu_percent:.1f}%"
    body = f"CPU usage is at {cpu_percent:.1f}%, which exceeds the {CPU_THRESHOLD}% threshold."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_TO

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [ALERT_TO], msg.as_string())
        print(f"Alert email sent to {ALERT_TO}")
    except smtplib.SMTPException as e:
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


if __name__ == "__main__":
    check_cpu_once()
