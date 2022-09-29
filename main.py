import logging

import recipe_factory
import translation
import message_cls
import answering

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '5483232182:AAE6RnbdIkqWCm-HpMMXzZkJ4T00q3d5hb4'
START_MESSAGE_PARAHRAPHS = [
    '🤖 Привет! Я твой повар и нейросеть.',
    '🥑 Назови любое, пускай даже не существующее блюдо, а я придумаю рецепт.',
    '❓ Также ты можешь задать мне любой вопрос по кулинарии.',
    '🎨 Скоро я научусь рисовать блюда по их названиям и даже смогу сам придумать названия.',
    '🤷‍♂️ Я могу нечайно сгенерировать неполный рецепт или дать неоднозначный ответ на вопрос, но это потому что я обучался всего 3 эпохи на небольшой выборке.'
]
START_MESSAGE = '\n\n'.join(START_MESSAGE_PARAHRAPHS)  # Join parahraphs with one empty line inbetween

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(START_MESSAGE)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(START_MESSAGE)


def on_text(update: Update, context: CallbackContext) -> None:
    """User message handling."""
    text = update.message.text
    
    # Check if message is question or a dish name
    if message_cls.isMessageQuestionCls.predict(text):
        responce = answering.answer_question(text)
        update.message.reply_text(responce)
    else:
        update.message.reply_text('🕓 Придумываю рецепт...')
        text_en = translation.ru_en.translate(text.lower())[0].lower()
        recipe_en = recipe_factory.recipeFactory.generate_recipe(text_en)
        recipe = translation.translate_recipe_to_russian(recipe_en)
        responce = recipe.to_message()
        update.message.reply_text(responce)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, on_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
