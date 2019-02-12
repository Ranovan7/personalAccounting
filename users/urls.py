from django.urls import path
from .views import WalletInfo

urlpatterns = [
    path('', WalletInfo.as_view(), name='wallet-info')
]
