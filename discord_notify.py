import os
import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_notification(name, url, old_price, new_price):
    message = {
        "content": f"💸 **Price Drop Detected!**\n**{name}** just dropped from **${old_price}** to **${new_price}**.\n🔗 {url}"
    }
    response = requests.post(WEBHOOK_URL, json=message)
    print("📩 Discord notification sent." if response.ok else f"❌ Discord error: {response.text}")
