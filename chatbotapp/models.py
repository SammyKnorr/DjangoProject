from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_tag = models.CharField(max_length=10)
    shares = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    graph_path = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.stock_tag} - {self.user.username}"
