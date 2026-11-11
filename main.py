import os
import asyncio
import threading
import shutil
from fastapi import FastAPI, Request, Form, Response, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import settings
from handlers.commands import start_command, help_command
from handlers.messages import handle_tradingview_url, handle_photo_upload
from services.browser import capture_chart_screenshot
from services.ai_vision import analyze_chart_image

app = FastAPI(title="TradingView Bot Control Center")
templates = Jinja2Templates(directory="templates")

# Global Background Thread Controllers for Telegram Bot
bot_thread = None
is_bot_running = False
stop_event = threading.Event()

def run_telegram_bot():
    """Runs the Telegram bot using built-in run_polling to handle async loops safely."""
    global is_bot_running
    try:
        # Build the application
        telegram_app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Register handlers from your modular files
        telegram_app.add_handler(CommandHandler("start", start_command))
        telegram_app.add_handler(CommandHandler("help", help_command))
        
        # 1. Listen for TradingView URLs in text messages
        telegram_app.add_handler(
            MessageHandler(
                filters.TEXT & (~filters.COMMAND) & filters.Regex(r"tradingview\.com/chart/"),
                handle_tradingview_url
            )
        )
        
        # 2. Listen for direct photo/screenshot uploads in Telegram chat
        telegram_app.add_handler(
            MessageHandler(
                filters.PHOTO & (~filters.COMMAND),
                handle_photo_upload
            )
        )
        
        is_bot_running = True
        print("🤖 Telegram Bot polling started successfully.")
        
        # run_polling() manages the async event loop and updates cleanly
        telegram_app.run_polling(stop_signals=None)
        
    except Exception as e:
        print(f"❌ Telegram Bot error: {e}")
    finally:
        is_bot_running = False
        print("🛑 Telegram Bot stopped.")

# --- Web Routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, auth_token: str = Cookie(default=None)):
    if auth_token != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/login", status_code=303)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login", response_class=HTMLResponse)
async def login_action(request: Request, password: str = Form(...)):
    if password == settings.ADMIN_PASSWORD:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="auth_token", value=settings.ADMIN_PASSWORD, httponly=True)
        return response
    return templates.TemplateResponse(request, "login.html", {"error": "Invalid Password"})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="auth_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, auth_token: str = Cookie(default=None), analysis_result: str = None):
    if auth_token != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(request, "dashboard.html", {
        "is_running": is_bot_running,
        "analysis_result": analysis_result
    })

@app.post("/toggle-bot")
async def toggle_bot(auth_token: str = Cookie(default=None)):
    global bot_thread, is_bot_running, stop_event
    if auth_token != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/login", status_code=303)
    
    if is_bot_running:
        stop_event.set()
        if bot_thread:
            bot_thread.join(timeout=5)
        is_bot_running = False
    else:
        stop_event.clear()
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()
        
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_chart_web(
    request: Request, 
    chart_url: str = Form(None), 
    chart_file: UploadFile = File(None), 
    auth_token: str = Cookie(default=None)
):
    if auth_token != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/login", status_code=303)
    
    image_path = None
    try:
        os.makedirs("temp", exist_ok=True)
        
        # Scenario A: User uploaded an image file directly via web dashboard
        if chart_file and chart_file.filename:
            image_path = os.path.join("temp", f"upload_{chart_file.filename}")
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(chart_file.file, buffer)
            source_info = f"Uploaded File: {chart_file.filename}"
            
        # Scenario B: User provided a TradingView URL via web dashboard
        elif chart_url:
            image_path = await capture_chart_screenshot(chart_url, "web_snapshot.png")
            source_info = f"URL: {chart_url}"
        else:
            raise ValueError("Please provide either a TradingView URL or upload an image file.")
        
        # Run AI Vision Analysis (via OpenRouter)
        analysis = analyze_chart_image(image_path)
        
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            
        result_text = f"Source - {source_info}\n\n{analysis}"
    except Exception as e:
        result_text = f"Error analyzing chart: {str(e)}"
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        
    return templates.TemplateResponse(request, "dashboard.html", {
        "is_running": is_bot_running,
        "analysis_result": result_text
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)