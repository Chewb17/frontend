from django.urls import path
from .views import CustomAuthToken, SaleListView, RegisterView, SaleDetailView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('sales/', SaleListView.as_view(), name='api_sales'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='api_sales_detail'),  # Corrigir para usar SaleDetailView
    path('register/', RegisterView.as_view(), name='api_register'),
]