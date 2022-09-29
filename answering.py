import utils


qa = utils.Seq2SeqGenerator('FlightBlaze/food-qa')


def answer_question(text):
    preprocessed_text = utils.preprocess(text)
    return qa(preprocessed_text)[0]
