from django.urls import path
from .views import CompanyManagement
urlpatterns = [
    path('', CompanyManagement, name='companies_management'),
]