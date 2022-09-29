from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from pymorphy2 import MorphAnalyzer
import string
import re
import nltk
import device


nltk.download('punkt')
morph = MorphAnalyzer()


def make_first_letter_capital(name):
  return name[0].upper() + name[1:]


def fahrengheit_to_celsius(degrees):
  return (degrees - 32) * 5 / 9


def is_fahrengheit(token):
  return token.endswith('f') and token[:-1].isdigit()


def round_degrees(deg):
  return int(round(deg / 10) * 10)


def replace_fahrengheit_with_celsius_str(steps):
  tokens = word_tokenize(steps)
  tokens = [f'{round_degrees(int(fahrengheit_to_celsius(int(token[:-1]))))} degrees celsius'\
            if is_fahrengheit(token) else token for token in tokens]
  text = ' '.join(tokens)
  text = re.sub(' ,', ',', text)
  text = re.sub(' [.]', '.', text)
  return text


class Seq2SeqGenerator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.pipe = pipeline(task='text2text-generation',
                             model=self.model,
                             tokenizer=self.tokenizer,
                             device=device.device)
    

    def __call__(self, *args, **kwd):
        return [out['generated_text'] for out in self.pipe(args[0])]


def preprocess(text):
    new_text = re.sub('[?]', '', text)  # remove question sign
    new_text = new_text.lower()
    tokens = [morph.parse(token)[0].normal_form \
            for token in word_tokenize(new_text) \
            if token not in string.punctuation]
    return ' '.join(tokens)
