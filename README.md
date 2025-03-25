# 💸 Price Drop Notifier

A FastAPI + Playwright backend to track item prices and send Discord notifications when prices drop. Powered by Supabase.

## 🔧 Features

- Add items to track (name, URL, current price)
- Scrapes product pages using Playwright
- Sends Discord alerts when prices drop
- Persistent storage via Supabase
- Works with Render or Railway

## 📦 Endpoints

- `GET /items` → View all tracked items
- `POST /add-item` → Add a new item
- `POST /run-check` → Check all items for price drops

## 🚀 Deployment

Deploy easily on [Render](https://render.com) or [Railway](https://railway.app).  
Don't forget to add the environment variables from `.env`.

## 🧠 Coming Soon

- Frontend dashboard (React + Tailwind)
- Price history
- Sort, filter, and chart changes
