import os
from telegram import Update
from telegram.ext import ContextTypes
from services.browser import capture_chart_screenshot
from services.ai_vision import analyze_chart_image

async def handle_tradingview_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming TradingView URLs sent as text messages."""
    url = update.message.text
    status_msg = await update.message.reply_text("🔍 Capturing chart screenshot via Playwright...")
    
    output_filename = f"telegram_snapshot_{update.effective_user.id}.png"
    image_path = None
    
    try:
        # 1. Capture screenshot from URL
        image_path = await capture_chart_screenshot(url, output_filename)
        
        await status_msg.edit_text("🤖 Analyzing chart with OpenRouter AI...")
        
        # 2. Run AI vision analysis
        analysis = analyze_chart_image(image_path)
        
        # 3. Send back photo and analysis report
        with open(image_path, "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=analysis[:1024]  # Telegram caption limit safety
            )
            
        # If analysis is longer than Telegram's caption limit, send the rest as a text message
        if len(analysis) > 1024:
            await update.message.reply_text(analysis[1024:])
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing chart URL: {str(e)}")
    finally:
        # Clean up temp file
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        await status_msg.delete()

async def handle_photo_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles direct image uploads sent by users in the Telegram chat."""
    status_msg = await update.message.reply_text("📥 Receiving screenshot and analyzing with OpenRouter AI...")
    
    image_path = None
    try:
        # Get the largest available photo from Telegram's photo array
        photo_file = await update.message.photo[-1].get_file()
        
        os.makedirs("temp", exist_ok=True)
        image_path = f"temp/telegram_upload_{update.effective_user.id}.jpg"
        
        # Download photo locally
        await photo_file.download_to_drive(image_path)
        
        # Run AI vision analysis
        analysis = analyze_chart_image(image_path)
        
        # Send back the analysis
        await update.message.reply_text(analysis)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing uploaded image: {str(e)}")
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        await status_msg.delete()