from django.shortcuts import render
from .forms import StockPredictionForm
import requests
import json

def predict_stock(request):
    if request.method == 'POST':
        form = StockPredictionForm(request.POST)
        if form.is_valid():
            stock_symbol = form.cleaned_data['stock_symbol']
            date = form.cleaned_data['date']
            url='https://ptoar7b9u5.execute-api.us-east-2.amazonaws.com/prod'
            myobj = json.dumps({"inputs":f"predict the closing value on {date} for {stock_symbol}"})
            x= requests.post(url, data=myobj, headers={'content-type':'application/json','x-api-key':''})
            return render(request, 'predictions/result.html', {'prediction': json.loads(x.text)[0]["generated_text"]})
    else:
        form = StockPredictionForm()
    return render(request, 'predictions/predict.html', {'form': form})
