import logging
import os

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Отправь мне первую строчку на русском языке и получи четверостишье, сочиненное машиной!")


def main() -> None:
    token = os.environ.get("TG_TOKEN")

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start, help'], help_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
