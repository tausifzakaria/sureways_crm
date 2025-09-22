from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_list, name="companies_management"),
    path("companies/save/", views.company_save, name="company_save"),
    path("companies/delete/<int:pk>/", views.company_delete, name="company_delete"),
    path("companies/dashboard-counts/", views.company_dashboard_counts, name="company_dashboard_counts"),
]
