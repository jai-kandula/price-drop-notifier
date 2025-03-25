import os
import requests

def send_discord_notification(message: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL not set in environment variables.")

    data = {
        "content": message
    }

    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        raise Exception(f"Failed to send Discord notification: {response.status_code}, {response.text}")
