from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("your_stocks/", views.your_stocks, name="your_stocks"),
    path("delete_stock/<int:stock_id>/", views.delete_stock, name="delete_stock"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
