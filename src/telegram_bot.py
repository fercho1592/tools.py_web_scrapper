from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,ContextTypes, Application
from telegram.constants import ReactionEmoji
from asyncio import sleep

def BuildApp() -> Application:
    from configs.config_manager import read_telegram_bot_config
    config = read_telegram_bot_config()
    bot_token = config["bot_token"]

    app = ApplicationBuilder().token(bot_token).build()
    return app

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.effective_user)
    print(update.message.text)
    await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                           message_id=update.message.message_id,
                                           reaction=ReactionEmoji.GHOST)
    await update.message.reply_text('No respondo pendejadas')
    await sleep(2)
    await update.message.reply_text('Y menos a maricas')

if __name__ == '__main__':
    print('Starting bot...')
    app = BuildApp()

    print('Registering handlers...')
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(None, messageHandler))

    print('Running bot...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)
