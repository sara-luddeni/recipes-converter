import logging
import os
import re
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from recipes_bot.downloaders.tiktok import TikTokDownloader
from recipes_bot.extractors.recipe import extract_recipe_from_video
from recipes_bot.extractors.models import Recipe

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TIKTOK_URL_PATTERN = re.compile(
    r'https?://(?:www\.|vm\.)?tiktok\.com/[^\s]+'
)


def extract_tiktok_url(text: str) -> str | None:
    match = TIKTOK_URL_PATTERN.search(text)
    return match.group(0) if match else None


def format_recipe_telegram(recipe: Recipe) -> str:
    lines = [
        f"*{recipe.title}*",
        "",
        "*Ingredients:*"
    ]
    
    for ingredient in recipe.ingredients:
        escaped = ingredient.replace("_", "\\_").replace("*", "\\*")
        lines.append(f"• {escaped}")
    
    lines.extend(["", "*Instructions:*"])
    
    for i, instruction in enumerate(recipe.instructions, start=1):
        escaped = instruction.replace("_", "\\_").replace("*", "\\*")
        lines.append(f"{i}. {escaped}")
    
    return "\n".join(lines)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info("User %s (id=%s) started the bot", user.username, user.id)
    welcome_message = (
        "Welcome to the Recipe Bot!\n\n"
        "Send me a TikTok video link containing a recipe, "
        "and I'll extract the recipe for you.\n\n"
        "Just paste the link and I'll do the rest!"
    )
    await update.message.reply_text(welcome_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    
    user = update.effective_user
    url = extract_tiktok_url(update.message.text)
    if not url:
        logger.debug("User %s sent non-TikTok message", user.id)
        await update.message.reply_text(
            "Please send a valid TikTok video link.\n"
            "Example: https://www.tiktok.com/@user/video/1234567890"
        )
        return
    
    logger.info("User %s (id=%s) requested recipe from: %s", user.username, user.id, url)
    status_message = await update.message.reply_text(
        "Processing your video... This may take a minute."
    )
    
    temp_video_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_video_path = temp_file.name
        
        logger.info("Downloading video from %s", url)
        await status_message.edit_text("Downloading video...")
        TikTokDownloader.download(url, temp_video_path)
        
        logger.info("Transcribing and extracting recipe from %s", temp_video_path)
        await status_message.edit_text("Transcribing and extracting recipe...")
        recipe = extract_recipe_from_video(temp_video_path, "/dev/null")
        
        logger.info("Successfully extracted recipe: %s", recipe.title)
        formatted_recipe = format_recipe_telegram(recipe)
        await status_message.edit_text(formatted_recipe, parse_mode="Markdown")
        
    except FileNotFoundError as e:
        logger.exception("File not found error for url %s", url)
        await status_message.edit_text(f"Error: Could not process the video. {e}")
    except ValueError as e:
        logger.exception("Value error processing url %s", url)
        await status_message.edit_text(f"Error: {e}")
    except RuntimeError as e:
        logger.exception("Runtime error processing url %s", url)
        await status_message.edit_text(f"Error processing recipe: {e}")
    except Exception:
        logger.exception("Unexpected error processing url %s", url)
        await status_message.edit_text(
            "Sorry, something went wrong while processing your video. "
            "Please try again later."
        )
    finally:
        if temp_video_path:
            try:
                Path(temp_video_path).unlink(missing_ok=True)
                logger.debug("Cleaned up temp file %s", temp_video_path)
            except OSError:
                logger.warning("Failed to clean up temp file %s", temp_video_path)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN environment variable is required. "
            "Please set it with your Telegram bot token."
        )
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
