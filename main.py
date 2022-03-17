import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from users import UserDataBase
import help

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s() - %(message)s',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(help.full_help_admin)


def echo(update: Update, context: CallbackContext) -> None:
    """Мне не известна такая команда."""
    user_id = update.effective_user.id
    update.message.reply_text(f"Твой telegram_id: {user_id}")


def test(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    logger.debug(f'Context is: {context.args}')
    update.message.reply_text(''.join(context.args))


# Users management

def add_user(update: Update, context: CallbackContext) -> None:
    """Added users in database, for admins only"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}, len = {len(context.args)}")
        if len(context.args) == 0:
            update.message.reply_text(help.adduser)
        else:
            telegram_id: str = ''.join(context.args[0])
            group: str = ''.join(context.args[1])
            description: str = ' '.join(context.args[2:])
            update.message.reply_text(users.add_user(telegram_id, group, description))
    except Exception as err:
        logger.error(err)


def list_user(update: Update, context: CallbackContext) -> None:
    """Show users in DataBase"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}")
        find_key: str = ''.join(context.args)
        logger.debug(f"find_key is: {find_key}")
        update.message.reply_text(users.list_user(find_key))
    except Exception as err:
        logger.error(err)


def off_user(update: Update, context: CallbackContext) -> None:
    """Disable user"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}")
        telegram_id: str = ''.join(context.args)
        logger.debug(f"telegram_id is: {telegram_id}")
        update.message.reply_text(users.off_user(telegram_id))
    except Exception as err:
        logger.exception(err)


def on_user(update: Update, context: CallbackContext) -> None:
    """Enable user"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}")
        telegram_id: str = ''.join(context.args)
        logger.debug(f"telegram_id is: {telegram_id}")
        update.message.reply_text(users.on_user(telegram_id))
    except Exception as err:
        logger.exception(err)


def del_user(update: Update, context: CallbackContext) -> None:
    """Delete user"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}")
        telegram_id: str = ''.join(context.args)
        logger.debug(f"telegram_id is: {telegram_id}")
        update.message.reply_text(users.del_user(telegram_id))
    except Exception as err:
        logger.exception(err)


def mov_user(update: Update, context: CallbackContext) -> None:
    """Move user"""
    try:
        users = UserDataBase()
        logger.debug(f"context args: {context.args}")
        telegram_id: str = ''.join(context.args[0])
        logger.debug(f"telegram_id is: {telegram_id}")
        group: str = ''.join(context.args[1])
        update.message.reply_text(users.move_user_to_group(telegram_id, group))
    except Exception as err:
        logger.exception(err)

# /Users management


def main() -> None:
    """Start the bot."""
    # Users from data base
    allowed_users = UserDataBase()
    admins = allowed_users.list_user_in_group('admin')

    # Create the Updater and pass it your bot's token.
    updater = Updater("695336312:AAFM16fPwyz-JIOra7DawJ46dXQo_qvolOE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # User management command
    dispatcher.add_handler(CommandHandler("adduser", add_user, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("listuser", list_user, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("offuser", off_user, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("onuser", on_user, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("deluser", del_user, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("movuser", mov_user, Filters.user(admins)))

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("test", test, Filters.user(admins)))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
