from django.shortcuts import render
from .forms import StockPredictionForm
from .model import stock_predictor

def predict_stock(request):
    if request.method == 'POST':
        form = StockPredictionForm(request.POST)
        if form.is_valid():
            stock_symbol = form.cleaned_data['stock_symbol']
            date = form.cleaned_data['date']
            prediction_input = f"{stock_symbol} {date}"
            prediction = stock_predictor.predict(prediction_input)
            return render(request, 'stockpredictions/result.html', {'prediction': prediction})
    else:
        form = StockPredictionForm()
    return render(request, 'stockpredictions/predict.html', {'form': form})
