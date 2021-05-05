import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from markov import markov_generate

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Отправь мне первую строчку на русском языке и получи четверостишье, сочиненное машиной!")


def get_keyboard_markup():
    keyboard = [
        [InlineKeyboardButton("Сгенерировать заново", callback_data='generate_new')],
    ]

    return InlineKeyboardMarkup(keyboard)


N_LINES = 4
USE_USER_TEXT = False


def get_poem(first_line=None):
    gen_lines = markov_generate()

    if first_line is None:
        return gen_lines
    else:
        return f'*{first_line}*\n{gen_lines}'


def new_poem_handler(update: Update, context: CallbackContext):
    text = get_poem(update.message.text if USE_USER_TEXT else None)

    update.message.reply_text(text)


def main() -> None:
    token = os.environ.get("TG_TOKEN")

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], help_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, new_poem_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
