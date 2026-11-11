# import base64
# import logging
# from openai import OpenAI
# from config import settings

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=settings.GEMINI_API_KEY,
# )

# def analyze_chart_image(image_path: str) -> str:
#     """Sends the chart image to OpenRouter for technical analysis with error handling."""
#     try:
#         with open(image_path, "rb") as image_file:
#             encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

#         prompt = (
#             "You are an expert quantitative trader and market analyst. "
#             "Analyze this TradingView chart screenshot carefully.\n\n"
#             "Provide a concise summary with the following sections:\n"
#             "1. **Asset & Timeframe**: Identify ticker and timeframe.\n"
#             "2. **Market Structure**: Overall trend (Bullish/Bearish/Ranging).\n"
#             "3. **Technical Indicators**: Key observations from visible indicators (RSI, Moving Averages, MACD, Volume, etc.).\n"
#             "4. **Trade Setup**:\n"
#             "   - Bias (Long/Short/Neutral)\n"
#             "   - Suggested Entry Zone\n"
#             "   - Stop Loss (SL)\n"
#             "   - Take Profit 1 (TP1) & Take Profit 2 (TP2)\n"
#             "   - Risk-to-Reward Ratio (Target minimum 1:2)\n"
#             "5. **Risk Assessment**: Potential traps, major news risks, or market conditions to watch.\n\n"
#             "Keep the output clean, structured, and formatted in valid Markdown."
#         )

#         response = client.chat.completions.create(
#             model="google/gemini-2.5-flash",  # Active OpenRouter model route
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/png;base64,{encoded_image}"
#                             }
#                         }
#                     ]
#                 }
#             ],
#             max_tokens=1500
#         )
        
#         if response.choices and response.choices[0].message.content:
#             return response.choices[0].message.content
#         else:
#             return "Error: OpenRouter returned an empty response content."
            
#     except Exception as e:
#         logging.error(f"AI Vision Analysis Failed: {str(e)}")
#         return f"Error communicating with OpenRouter API: {str(e)}"
    
    
    
    
    
    
# this is my own

import base64
import logging
from openai import OpenAI
from config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.GEMINI_API_KEY,
)

def analyze_chart_image(image_path: str) -> str:
    """Sends the chart image to OpenRouter for structured, pro-tier trade feedback."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        prompt = (
            "You are an elite institutional trading desk analyst. Analyze this chart for a 1-week swing setup "
            "using pure price action, market structure, and liquidity zones only. Do not mention technical indicators.\n\n"
            "Format your output cleanly to look like a professional data-driven terminal report using this exact layout:\n\n"
            "📊 **MARKET THESIS**\n"
            "[1-2 sharp sentences explaining the current structural narrative, e.g., higher lows printing with expanding momentum into major overhead liquidity.]\n\n"
            "📈 **KEY LEVELS & TRADE PLAN**\n"
            "```text\n"
            "• Target 1    : [Price] (+X%)\n"
            "• Resistance  : [Price] (+X%)\n"
            "• Entry Zone  : [Price]\n"
            "• Support     : [Price] (-X%)\n"
            "• Stop Loss   : [Price] (-X%)\n"
            "```\n"
            "* **Risk/Reward Profile:** [e.g., 1:3.2 Risk-to-Reward (Risking 1.5% to make 5.0%)]\n\n"
            "⚖️ **SCENARIO PROBABILITIES**\n"
            "• **Bullish Continuation:** [XX%] — [Brief condition]\n"
            "• **Range Rejection:** [XX%] — [Brief condition]\n"
            "• **Bearish Breakdown:** [XX%] — [Brief condition]\n\n"
            "⚡ **EXECUTION CONDITIONAL**\n"
            "[1 punchy sentence telling the trader exactly what confirmation or candle close validates or invalidates the setup.]"
        )

        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=900
        )
        
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "Error: OpenRouter returned an empty response content."
            
    except Exception as e:
        logging.error(f"AI Vision Analysis Failed: {str(e)}")
        return f"Error communicating with OpenRouter API: {str(e)}"