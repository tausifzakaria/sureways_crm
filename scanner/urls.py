from django.urls import path
from .views import Scanner, scan_business_card
urlpatterns = [
    path('', Scanner, name='scanner'),
    path("scan-card/", scan_business_card, name="scan_business_card"),
]