from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count, Avg
from .models import Company, Contact


def company_list(request):
    companies = Company.objects.all().prefetch_related("linked_contacts")
    contacts = Contact.objects.all()
    return render(request, "companies.html", {
        "companies": companies,
        "contacts": contacts,  # for select dropdown
    })


def company_dashboard_counts(request):
    total_companies = Company.objects.count()
    active = Company.objects.filter(status="Active").count()
    industries = Company.objects.values("industry").exclude(industry="").distinct().count()

    # average contacts per company
    avg_contacts = (
        Company.objects.annotate(cnt=Count("linked_contacts"))
        .aggregate(avg=Avg("cnt"))["avg"] or 0
    )

    return JsonResponse({
        "totalCompanies": total_companies,
        "active": active,
        "industries": industries,
        "avgContacts": round(avg_contacts, 2),
    })


@require_POST
def company_save(request):
    pk = request.POST.get("id")
    linked_contacts_ids = request.POST.getlist("linkedContacts")

    data = {
        "name": request.POST.get("companyName", "").strip(),
        "website": request.POST.get("website", "").strip(),
        "phone": request.POST.get("phone", "").strip(),
        "industry": request.POST.get("industry", "").strip(),
        "status": request.POST.get("status", "").strip(),
        "country": request.POST.get("country", "").strip(),
        "city": request.POST.get("city", "").strip(),
        "address": request.POST.get("address", "").strip(),
        "tags": request.POST.get("tags", "").strip(),
        "source": request.POST.get("source", "").strip(),
        "notes": request.POST.get("notes", "").strip(),
    }

    if pk:
        company = get_object_or_404(Company, pk=pk)
        for k, v in data.items():
            setattr(company, k, v)
        company.save()
    else:
        company = Company.objects.create(**data)

    # update linked contacts
    if linked_contacts_ids:
        company.linked_contacts.set(Contact.objects.filter(pk__in=linked_contacts_ids))

    return redirect("companies_management")


def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
    return redirect("companies_management")
