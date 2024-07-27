from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import StockAddView

urlpatterns = [
    path("", views.home, name="home"),
    path("your_stocks/", views.your_stocks, name="your_stocks"),
    path("delete_stock/<int:stock_id>/", views.delete_stock, name="delete_stock"),
    path("edit_shares/<int:stock_id>/", views.edit_shares, name="edit_shares"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/add-stock/', StockAddView.as_view(), name='add-stock'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
