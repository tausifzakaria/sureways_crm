from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="tasks_list"),
    path("tasks/save/", views.task_save, name="task_save"),
    path("tasks/delete/<int:pk>/", views.task_delete, name="task_delete"),
    path("tasks/status_update/<int:pk>/", views.task_status_update, name="task_status_update"),
    path("tasks/counts/", views.task_dashboard_counts, name="task_dashboard_counts"),
    path("activities/", views.activities, name="activities"),
    path("activities/add/", views.activity_add, name="activity_add"),
    path("activities/<int:pk>/edit/", views.activity_edit, name="activity_edit"),
    path("activities/<int:pk>/delete/", views.activity_delete, name="activity_delete"),
]
