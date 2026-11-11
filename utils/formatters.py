def format_signal_response(url: str, analysis_text: str) -> str:
    """Formats the final text message delivered to Telegram."""
    header = "📊 **TradingView Chart Analysis**\n"
    source = f"🔗 **Source**: [View Original Chart]({url})\n\n"
    disclaimer = "\n\n⚠️ *Disclaimer: Not financial advice. For educational and analytical purposes only.*"
    return f"{header}{source}{analysis_text}{disclaimer}"