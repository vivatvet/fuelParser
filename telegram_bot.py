import telegram
from telegram import Update
import env
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
from orm import Orm

t_bot = telegram.Bot(token=env.bot_token)


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    orm = Orm()
    if not orm.find_user(user_id=user_id):
        orm.add_user(user_id=user_id)


def start_bot():
    updater = Updater(token=env.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()


def send_msg(msg: str):
    orm = Orm()
    users = orm.get_users()
    for user in users:
        user_id: int = user[0]
        try:
            t_bot.send_message(chat_id=user_id, text=msg)
        except telegram.error.BadRequest as e:
            print("telegram error", e)
