import logging

import recipe_factory
import translation
import message_cls
import answering

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5483232182:AAE6RnbdIkqWCm-HpMMXzZkJ4T00q3d5hb4'
START_MESSAGE_PARAHRAPHS = [
    '🤖 Привет! Я твой повар и нейросеть.',
    '🥑 Назови любое, пускай даже не существующее блюдо, а я придумаю рецепт.',
    '❓ Также ты можешь задать мне любой вопрос по кулинарии.',
    '🎨 Скоро я научусь рисовать блюда по их названиям и даже смогу сам придумать названия.',
    '🤷‍♂️ Я могу нечайно сгенерировать неполный рецепт или дать неоднозначный ответ на вопрос, но это потому что я обучался всего 3 эпохи на небольшой выборке.'
]
START_MESSAGE = '\n\n'.join(START_MESSAGE_PARAHRAPHS)  # Join parahraphs with one empty line inbetween

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    message.reply(START_MESSAGE)


@dp.message_handler()
async def on_msg(message: types.Message):
    """User message handling."""
    text = message.text
    
    # Check if message is question or a dish name
    if message_cls.isMessageQuestionCls.predict(text):
        responce = answering.answer_question(text)
        message.answer.reply_text(responce)
    else:
        message.answer.reply_text('🕓 Придумываю рецепт...')
        text_en = translation.ru_en.translate(text.lower())[0].lower()
        recipe_en = recipe_factory.recipeFactory.generate_recipe(text_en)
        recipe = translation.translate_recipe_to_russian(recipe_en)
        responce = recipe.to_message()
        message.answer.reply_text(responce)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
