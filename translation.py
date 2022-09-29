import sacremoses
import recipe_factory
import device
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


RU_EN_MODEL_NAME = 'facebook/wmt19-ru-en'
EN_RU_MODEL_NAME = 'facebook/wmt19-en-ru'


class Translator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.pipe = pipeline(task='translation', model=self.model,
                             tokenizer=self.tokenizer, device=device.device)
    
    
    def translate(self, text):
        return [out['translation_text'] for out in self.pipe(text)]


ru_en = Translator(RU_EN_MODEL_NAME)
en_ru = Translator(EN_RU_MODEL_NAME)


def translate_recipe_to_russian(recipe: recipe_factory.Recipe):
    translator = en_ru
    return recipe_factory.Recipe(
        translator.translate(recipe.name)[0],
        translator.translate(recipe.ingredients),
        translator.translate(recipe.steps)
    )
