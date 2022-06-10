import telegram
from telegram import Update
import env
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from orm import Orm
from site_parser import MyHTMLParser

t_bot = telegram.Bot(token=env.bot_token)


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    orm = Orm()
    if not orm.find_user(user_id=user_id):
        orm.add_user(user_id=user_id)
    update.message.pin(disable_notification=True)
    update.message.reply_text("Enter number of azs")


def list_azs(update: Update, context: CallbackContext):
    orm = Orm()
    user_id = update.effective_user.id
    azs = orm.get_subscribed_azs(user_id=user_id)
    for a in azs:
        update.message.reply_text(f'{a[2]}\n{a[1]}\n')


def message_handler(update: Update, context: CallbackContext):
    cmd = context.bot.get_chat(update.effective_chat.id).pinned_message
    if not cmd:
        update.message.reply_text("Use cmd add or del")
        return
    else:
        cmd = cmd.text
    update.effective_chat.unpin_all_messages()
    if cmd == "/add" or cmd == "/start":
        add_azs(update=update, context=context)
    elif cmd == "/del":
        del_azs(update=update, context=context)


def start_bot():
    updater = Updater(token=env.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', start))
    dispatcher.add_handler(CommandHandler('del', start))
    dispatcher.add_handler(CommandHandler('list', list_azs))
    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.start_polling()


def send_msg(user_id: int, msg: str):
    try:
        t_bot.send_message(chat_id=user_id, text=msg)
    except telegram.error.BadRequest as e:
        print("telegram error", e)


def add_azs(update: Update, context: CallbackContext):
    user_id: int = update.effective_user.id
    number: str = update.message.text.strip()
    orm = Orm()
    azs_list = MyHTMLParser().get_azs()
    for azs in azs_list["data"]:
        n_azs = azs['FullName'].split("№")[1].split(" ")[0]
        if number == n_azs:
            full_name: str = azs['FullName']
            address: str = azs['Address']
            azs_id: int = azs['id']
            added_azs = orm.get_subscribed_azs(user_id=user_id)
            for add_azs_f in added_azs:
                if add_azs_f[0] == azs_id:
                    update.message.reply_text("AZS already added")
                    return True
            orm.subscribe(user_id=user_id, full_name=full_name, address=address, azs_id=azs_id)
            update.message.reply_text("AZS was added.")
            return True
    update.message.reply_text("Azs not found")
    return True


def del_azs(update: Update, context: CallbackContext):
    user_id: int = update.effective_user.id
    number: str = update.message.text.strip()
    orm = Orm()
    azs_list = MyHTMLParser().get_azs()
    for azs in azs_list["data"]:
        n_azs = azs['FullName'].split("№")[1].split(" ")[0]
        if number == n_azs:
            azs_id: int = azs['id']
            added_azs = orm.get_subscribed_azs(user_id=user_id)
            for add_azs_f in added_azs:
                if add_azs_f[0] == azs_id:
                    orm.unsubscribe(user_id=user_id, azs_id=azs_id)
                    update.message.reply_text("AZS was deleted.")
                    return True
    update.message.reply_text("AZS not fount in subscribe.")
    return True
