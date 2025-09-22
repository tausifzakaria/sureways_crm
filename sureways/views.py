from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def Home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'home.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authentication/login.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from  contacts.models import Contact
from companies.models import Company
from tasks.models import Task, Activity
from django.utils.dateparse import parse_datetime, parse_date

def import_export_page(request):
    return render(request, "import_export.html")
# ------- EXPORT -------
def export_company_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=companies.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "name", "website", "phone", "industry", "status", "country", "city", "address", "tags", "source", "notes"])
    for c in Company.objects.all():
        writer.writerow([c.id, c.name, c.website, c.phone, c.industry, c.status, c.country, c.city, c.address, c.tags, c.source, c.notes])
    return response

def export_contact_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "full_name", "job_title", "department", "speciality", "email_primary", "email_secondary", "mobile", "whatsapp", "country", "city", "tags", "source", "notes", "status", "is_prospect"])
    for c in Contact.objects.all():
        writer.writerow([c.id, c.full_name, c.job_title, c.department, c.speciality, c.email_primary, c.email_secondary, c.mobile, c.whatsapp, c.country, c.city, c.tags, c.source, c.notes, c.status, c.is_prospect])
    return response

def export_task_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tasks.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "title", "description", "contact_id", "company_id", "due_date", "type", "priority", "status", "completed_at"])
    for t in Task.objects.all():
        writer.writerow([t.id, t.title, t.description, t.contact_id, t.company_id, t.due_date, t.type, t.priority, t.status, t.completed_at])
    return response

def export_activity_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=activities.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "type", "title", "description", "date_time", "contact_id", "company_id", "outcome"])
    for a in Activity.objects.all():
        writer.writerow([a.id, a.type, a.title, a.description, a.date_time, a.contact_id, a.company_id, a.outcome])
    return response

# ------- IMPORT -------
def import_company_csv(request):
    if request.method == "POST":
        file = request.FILES["file"]
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())
        for row in reader:
            Company.objects.update_or_create(id=row.get("id") or None, defaults=row)
        messages.success(request, "Companies imported successfully!")
    return redirect("import_export")

def import_contact_csv(request):
    if request.method == "POST":
        file = request.FILES["file"]
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())
        for row in reader:
            Contact.objects.update_or_create(id=row.get("id") or None, defaults=row)
        messages.success(request, "Contacts imported successfully!")
    return redirect("import_export")

def import_task_csv(request):
    if request.method == "POST":
        file = request.FILES["file"]
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())
        for row in reader:
            Task.objects.update_or_create(id=row.get("id") or None, defaults=row)
        messages.success(request, "Tasks imported successfully!")
    return redirect("import_export")

def import_activity_csv(request):
    if request.method == "POST":
        file = request.FILES["file"]
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())
        for row in reader:
            Activity.objects.update_or_create(id=row.get("id") or None, defaults=row)
        messages.success(request, "Activities imported successfully!")
    return redirect("import_export")

# ------- CSV Templates -------
def download_company_template(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=company_template.csv'
    writer = csv.writer(response)
    writer.writerow(["id","name","website","phone","industry","status","country","city","address","tags","source","notes"])
    return response

def download_contact_template(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=contact_template.csv'
    writer = csv.writer(response)
    writer.writerow(["id","full_name","job_title","department","speciality","email_primary","email_secondary","mobile","whatsapp","country","city","tags","source","notes","status","is_prospect"])
    return response

def download_task_template(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=task_template.csv'
    writer = csv.writer(response)
    writer.writerow(["id","title","description","contact_id","company_id","due_date","type","priority","status","completed_at"])
    return response

def download_activity_template(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=activity_template.csv'
    writer = csv.writer(response)
    writer.writerow(["id","type","title","description","date_time","contact_id","company_id","outcome"])
    return response