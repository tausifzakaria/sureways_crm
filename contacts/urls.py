from django.urls import path
from .views import ContactManagement
urlpatterns = [
    path('', ContactManagement, name='contacts_management'),
]