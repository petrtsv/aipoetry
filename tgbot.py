import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from markov import markov_generate

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

keyboard = [
    [InlineKeyboardButton("Сгенерировать заново", callback_data='generate_new'),
     InlineKeyboardButton("Сохранить", callback_data='save')],
]

keyboard_markup = InlineKeyboardMarkup(keyboard)


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Отправь мне первую строчку на русском языке и получи четверостишье, сочиненное машиной!")


def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    if query.data == 'generate_new':
        first_line = (query.message.text_markdown.split('\n')[0])[1:-1]
        query.edit_message_text(text=get_poem(first_line), reply_markup=keyboard_markup, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'save':
        query.edit_message_reply_markup(reply_markup=None)


def get_poem(first_line=None):
    words = list(first_line.split())
    words = words[-min(2, len(words)):]
    while len(words) < 2:
        words = [words[0]] + words

    gen_lines = markov_generate(words)

    return f'*{first_line}*\n{gen_lines}'


def new_poem_handler(update: Update, context: CallbackContext):
    text = get_poem(update.message.text)

    update.message.reply_text(text, reply_markup=keyboard_markup, parse_mode=ParseMode.MARKDOWN)


def main() -> None:
    token = os.environ.get("TG_TOKEN")

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], help_handler))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, new_poem_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
