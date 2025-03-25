from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
from scraper import scrape_price
from discord_notify import send_discord_notification
import os

app = FastAPI()

# Enable CORS (optional, but good practice for APIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Price Drop Notifier is running"}

@app.post("/items")
async def add_item(item: dict):
    try:
        response = supabase.table("items").insert(item).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/items")
async def get_items():
    try:
        response = supabase.table("items").select("*").execute()
        return {"items": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/run-check")
async def run_check():
    try:
        response = supabase.table("items").select("*").execute()
        items = response.data

        updated_items = []

        for item in items:
            print(f"🟢 Checking item: {item['name']}")
            try:
                current = await scrape_price(item["url"])
                if current < item["current_price"]:
                    print(f"💸 Price drop detected for {item['name']}!")
                    updated_items.append(item["name"])
                    # Notify via Discord
                    await send_discord_notification(item["name"], item["url"], current)

                    # Update Supabase record
                    supabase.table("items").update({"current_price": current}).eq("id", item["id"]).execute()
            except Exception as e:
                print("❌ General scraping error:", e)

        return {"updated": updated_items}
    except Exception as e:
        return {"status": "error", "message": str(e)}
