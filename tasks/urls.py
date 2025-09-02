from django.urls import path
from .views import TaskManagement
urlpatterns = [
    path('', TaskManagement, name='tasks_management'),
]