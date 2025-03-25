import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_item(name, url, current_price):
    return supabase.table("items").insert({
        "name": name,
        "url": url,
        "current_price": current_price
    }).execute()

def get_all_items():
    res = supabase.table("items").select("*").execute()
    return res.data

def update_price(item_id, new_price):
    return supabase.table("items").update({
        "current_price": new_price
    }).eq("id", item_id).execute()
