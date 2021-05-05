import logging
import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler

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


def new_poem_handler(update: Update, context: CallbackContext):
    user_line = update.message.text

    gen_lines = "\n".join([str(uuid.uuid4()) for i in range(3)])

    update.message.reply_text(
        f'*{user_line}*\n{gen_lines}',
        parse_mode=ParseMode.MARKDOWN
    )


def main() -> None:
    token = os.environ.get("TG_TOKEN")

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], help_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
