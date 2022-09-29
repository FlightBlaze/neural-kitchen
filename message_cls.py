import joblib
import utils


class IsMessageQuestionClassifier:
    def __init__(self):
        self.vectorizer = joblib.load('data/models/is_question_vectorizer.joblib')  # Count vectorizer
        self.lr = joblib.load('data/models/is_question_lr.joblib')  # Logistic regression model


    def predict(self, text):
        return self.lr.predict(
            self.vectorizer.transform(
                [utils.preprocess(text)]
            )
        )[0] != 0.0


isMessageQuestionCls = IsMessageQuestionClassifier()
