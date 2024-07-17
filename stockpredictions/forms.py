from django import forms

class StockPredictionForm(forms.Form):
    stock_symbol = forms.CharField(label='Stock Symbol', max_length=10)
    date = forms.DateField(label='Prediction Date')
