import os
import requests
import matplotlib
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StockForm, EditSharesForm
from .models import Stock
from chatbot import settings

# Create your views here.
matplotlib.use('Agg')

def home(request):
    return render(request, "home.html")

def autocomplete_stock_tags(request):
    query = request.GET.get('q', '')
    api_key = settings.ALPHAVANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    results = []
    if 'bestMatches' in data:
        for match in data['bestMatches']:
            results.append(match['1. symbol'])

    return JsonResponse(results, safe=False)

@login_required
def your_stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_tag = form.cleaned_data.get('stock_tag')
            shares = form.cleaned_data.get('shares')
            existing_stock = Stock.objects.filter(user=request.user, stock_tag=stock_tag).first()
            if existing_stock:
                return JsonResponse({'success': False, 'errors': {'stock_tag': ["You already have this stock in your portfolio."]}})
            stock = Stock.objects.create(user=request.user, stock_tag=stock_tag, shares=shares)
            generate_stock_graph(stock_tag)
            current_worth = calculate_current_worth(stock_tag, shares)
            return JsonResponse({'success': True, 'stock_tag': stock_tag, 'stock_id': stock.id, 'shares': shares, 'current_price': current_worth / shares if shares else 0})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    form = StockForm()
    edit_form = EditSharesForm()
    stocks = Stock.objects.filter(user=request.user)
    for stock in stocks:
        stock.current_worth = calculate_current_worth(stock.stock_tag, stock.shares)
        generate_stock_graph(stock.stock_tag)  # Regenerate graph for each stock
    return render(request, 'your_stocks.html', {'stocks': stocks, 'form': form, 'edit_form': edit_form})

@login_required
def edit_shares(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id, user=request.user)
    if request.method == 'POST':
        form = EditSharesForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'shares': stock.shares, 'current_worth': calculate_current_worth(stock.stock_tag, stock.shares)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

def generate_stock_graph(stock_tag):
    api_key = settings.ALPHAVANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_tag}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    time_series = data.get('Time Series (Daily)', {})
    dates = list(time_series.keys())
    dates.sort()

    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    one_year_ago = datetime.now() - timedelta(days=365)
    filtered_dates = [date for date in dates if date > one_year_ago]

    closing_prices = [float(time_series[date.strftime('%Y-%m-%d')]['4. close']) for date in filtered_dates]

    plt.figure(figsize=(10, 5))
    plt.plot(filtered_dates, closing_prices, label='Closing Price')
    plt.title(f'Stock Trends for {stock_tag}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45)
    
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
    
    plt.legend()
    plt.tight_layout()

    media_path = settings.MEDIA_ROOT
    if not os.path.exists(media_path):
        os.makedirs(media_path)

    graph_path = os.path.join(media_path, f'{stock_tag}.png')
    plt.savefig(graph_path)
    plt.close()

    stock = Stock.objects.filter(stock_tag=stock_tag).order_by('-added_at').first()
    stock.graph_path = f'{stock_tag}.png'
    stock.save()

@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id, user=request.user)
    stock.delete()
    messages.success(request, f'Stock {stock.stock_tag} has been deleted.')
    return redirect('your_stocks')

def calculate_current_worth(stock_tag, shares):
    api_key = settings.ALPHAVANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_tag}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Global Quote' not in data:
        return 0
    current_price = float(data['Global Quote']['05. price'])
    return current_price * shares
