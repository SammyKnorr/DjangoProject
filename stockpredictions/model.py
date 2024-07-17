from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class StockPredictor:
    def __init__(self, model_path, tokenizer_path):
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

    def predict(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors='pt')
        outputs = self.model.generate(**inputs)
        prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return prediction

stock_predictor = StockPredictor(model_path='path/to/your/model', tokenizer_path='path/to/your/tokenizer')
