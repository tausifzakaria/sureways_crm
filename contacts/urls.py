from django.urls import path
from . import views

urlpatterns = [
    path("contacts_management/", views.contact_list, name="contacts_management"),
    path("save/", views.contact_save, name="contact_save"),   # <- new
    path("delete/<int:pk>/", views.contact_delete, name="contact_delete"),
    path("dashboard-counts/", views.dashboard_counts, name="dashboard_counts"),
]
