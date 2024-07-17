from django import forms

class StockForm(forms.Form):
    stock_tag = forms.CharField(max_length=10, help_text="Enter the stock tag (e.g., AAPL for Apple Inc.)")

    def clean_stock_tag(self):
        stock_tag = self.cleaned_data.get('stock_tag')
        # Add your validation for stock tags here, e.g., checking against a list of valid stock tags
        # For simplicity, we assume any non-empty value is valid.
        if not stock_tag.isalnum():
            raise forms.ValidationError("Stock tag must be alphanumeric.")
        return stock_tag