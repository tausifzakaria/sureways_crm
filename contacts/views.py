from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Contact
from django.http import JsonResponse
from django.db.models import Count

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts.html", {"contacts": contacts})

def dashboard_counts(request):
    # Count Active Clients
    active_clients = Contact.objects.filter(status="Active").count()

    # Count Prospects
    prospects = Contact.objects.filter(is_prospect=True).count()

    # Unique countries
    countries = Contact.objects.values("country").exclude(country="").distinct().count()

    return JsonResponse({
        "activeClients": active_clients,
        "prospects": prospects,
        "countries": countries,
    })

@require_POST
def contact_save(request):
    # If "id" present -> update, else create
    pk = request.POST.get("id")
    data = {
        "full_name": request.POST.get("full_name", "").strip(),
        "job_title": request.POST.get("job_title", "").strip(),
        "department": request.POST.get("department", "").strip(),
        "speciality": request.POST.get("speciality", "").strip(),
        "email_primary": request.POST.get("email_primary", "").strip(),
        "email_secondary": request.POST.get("email_secondary", "").strip(),
        "mobile": request.POST.get("mobile", "").strip(),
        "whatsapp": request.POST.get("whatsapp", "").strip(),
        "country": request.POST.get("country", "").strip(),
        "city": request.POST.get("city", "").strip(),
        "tags": request.POST.get("tags", "").strip(),
        "source": request.POST.get("source", "").strip(),
        "notes": request.POST.get("notes", "").strip(),
        "status": request.POST.get("status", "").strip(),
        "is_prospect": request.POST.get("is_prospect") == "on",
    }

    if pk:
        contact = get_object_or_404(Contact, pk=pk)
        for k, v in data.items():
            setattr(contact, k, v)
        contact.save()
    else:
        Contact.objects.create(**data)

    return redirect("contacts_management")


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
    return redirect("contacts_management")
