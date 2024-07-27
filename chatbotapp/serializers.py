from rest_framework import serializers

class StockSerializer(serializers.Serializer):
    stock_tag = serializers.CharField(max_length=10)
    shares = serializers.IntegerField(min_value=0)

    def __init__(self, valid_symbols, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_symbols = valid_symbols

    def validate_stock_tag(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Stock tag must be alphanumeric.")
        if value not in self.valid_symbols:
            raise serializers.ValidationError("Invalid stock tag.")
        return value