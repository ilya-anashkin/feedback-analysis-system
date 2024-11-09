from transformers import pipeline


class Analyzer:
    def __init__(self, model_name: str = "seara/rubert-tiny2-russian-sentiment"):
        self.model = pipeline(model=model_name)

    def predict(self, text: str) -> str:
        return self.model(text)[0]["label"]
