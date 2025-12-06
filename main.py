import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import asyncio

# Set your tokens here
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'
OPENAI_API_KEY = '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'

# Warning: NEVER commit real API keys to GitHub or public places!
# Use environment variables in production

openai.api_key = OPENAI_API_KEY

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your friendly chatbot. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly assistant."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        bot_reply = "Sorry, something went wrong with the AI. Try again later!"

    await update.message.reply_text(bot_reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == '__main__':
    main()
