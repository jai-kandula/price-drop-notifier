import sys
import asyncio
from fastapi import FastAPI
from scraper import scrape_price
from supabase_client import add_item, get_all_items, update_price
from discord_notify import send_notification

# ✅ Force correct event loop on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

api = FastAPI()

@api.get("/")
def root():
    return {"status": "Price Drop Notifier is running"}

@api.post("/add-item")
def add(item: dict):
    return add_item(item["name"], item["url"], item["current_price"])

@api.get("/items")
def fetch_items():
    return get_all_items()

@api.post("/run-check")
async def run_check():
    items = get_all_items()
    updated_items = []

    for item in items:
        print(f"🧪 Checking item: {item['name']}")
        current_price = await scrape_price(item["url"])
        if current_price is None:
            continue

        if current_price < item["current_price"]:
            updated_items.append(item["name"])
            update_price(item["id"], current_price)
            send_notification(
                name=item["name"],
                url=item["url"],
                old_price=item["current_price"],
                new_price=current_price
            )

    return {"updated": updated_items}
