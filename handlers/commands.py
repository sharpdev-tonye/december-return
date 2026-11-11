from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    welcome_text = (
        "👋 Welcome to TradingView Signal Bot!\n\n"
        "Send me a TradingView chart link (e.g., https://www.tradingview.com/chart/8opR1NZM/), "
        "and I will capture the rendered chart and generate an AI-powered technical setup for you!"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    help_text = (
        "💡 How to use:\n"
        "1. Open any chart on TradingView.\n"
        "2. Copy the URL from your browser address bar.\n"
        "3. Paste the URL directly into this chat.\n\n"
        "The bot will take a screenshot, read the technical setup, and output trade levels."
    )
    await update.message.reply_text(help_text)