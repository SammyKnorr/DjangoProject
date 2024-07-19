from django import forms
from .models import Stock

class StockForm(forms.Form):
    stock_tag = forms.CharField(
        max_length=10,
        help_text="Enter the stock tag (e.g., AAPL for Apple Inc.)",
        widget=forms.TextInput(attrs={'id': 'id_stock_tag'})
    )
    shares = forms.IntegerField(
        min_value=1,
        help_text="Enter the number of shares owned",
        widget=forms.NumberInput(attrs={'id': 'id_shares'})
    )

    def __init__(self, valid_symbols, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_symbols = valid_symbols

    def clean_stock_tag(self):
        stock_tag = self.cleaned_data.get('stock_tag')
        if not stock_tag.isalnum():
            raise forms.ValidationError("Stock tag must be alphanumeric.")
        if stock_tag not in self.valid_symbols:
            raise forms.ValidationError("Invalid stock tag.")
        return stock_tag

class EditSharesForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['shares']
        widgets = {
            'shares': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }