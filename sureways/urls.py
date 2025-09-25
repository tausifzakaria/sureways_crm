"""
URL configuration for sureways project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, Login, Logout, import_export_page,export_company_csv, export_contact_csv, export_task_csv, export_activity_csv , import_company_csv, import_contact_csv, import_task_csv, import_activity_csv, download_company_template, download_contact_template, download_task_template, download_activity_template
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('contacts/', include('contacts.urls')),
    path('companies/', include('companies.urls')),
    path('tasks/', include('tasks.urls')),
    path('scanner/', include('scanner.urls')),
    path("import-export/", import_export_page, name="import_export"),  # main page
        # Company
    path("export/company/", export_company_csv, name="export_company_csv"),
    path("import/company/", import_company_csv, name="import_company_csv"),
    path("template/company/", download_company_template, name="download_company_template"),
    # Contact
    path("export/contact/", export_contact_csv, name="export_contact_csv"),
    path("import/contact/", import_contact_csv, name="import_contact_csv"),
    path("template/contact/", download_contact_template, name="download_contact_template"),
    # Task
    path("export/task/", export_task_csv, name="export_task_csv"),
    path("import/task/", import_task_csv, name="import_task_csv"),
    path("template/task/", download_task_template, name="download_task_template"),
    # Activity
    path("export/activity/", export_activity_csv, name="export_activity_csv"),
    path("import/activity/", import_activity_csv, name="import_activity_csv"),
    path("template/activity/", download_activity_template, name="download_activity_template"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)