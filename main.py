import logging

import recipe_factory
import translation
import message_cls
import answering
import config

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(config.START_MESSAGE)


@dp.message_handler()
async def on_msg(message: types.Message):
    """User message handling."""
    text = message.text
    
    # Check if message is question or a dish name
    if message_cls.isMessageQuestionCls.predict(text):
        responce = answering.answer_question(text)
        await bot.send_message(message.from_user.id, responce)
    else:
        await bot.send_message(message.from_user.id, config.RECIPE_WAIT_MESSAGE)
        text_en = translation.ru_en.translate(text.lower())[0].lower()
        recipe_en = recipe_factory.recipeFactory.generate_recipe(text_en)
        recipe = translation.translate_recipe_to_russian(recipe_en)
        responce = recipe.to_message()
        await bot.send_message(message.from_user.id, responce)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
