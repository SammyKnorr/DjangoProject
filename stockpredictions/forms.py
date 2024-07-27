from django import forms

STOCK_CHOICES = [
    ('S&P 500 SPDR ETF', 'S&P 500 SPDR ETF (SPY)'),
    ('Nasdaq Composite Invesco QQQ ETF', 'Nasdaq Composite Invesco QQQ ETF (QQQ)'),
    ('Dow Jones SPDR ETF', 'Dow Jones SPDR ETF (DIA)')
]

class StockPredictionForm(forms.Form):
    stock_symbol = forms.ChoiceField(label='Stock Symbol', choices=STOCK_CHOICES)
    date = forms.DateField(label='Prediction Date', widget=forms.TextInput(attrs={'type': 'date'}))
