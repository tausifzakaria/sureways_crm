from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from .models import Task
from companies.models import Company
from contacts.models import Contact
from .forms import TaskForm
from django.utils import timezone
from django.utils.timezone import localdate
def task_list(request):
    tasks = Task.objects.all()
    contacts = Contact.objects.all()
    companies = Company.objects.all()
    today = localdate()

    for task in tasks:
        if task.due_date:
            delta = (today - task.due_date).days
            if delta > 0:
                task.overdue_days = delta
                task.due_status = f"Overdue by {delta} days"
                task.due_class = "bg-danger-subtle text-danger-emphasis"
            elif delta == 0:
                task.overdue_days = 0
                task.due_status = "Due Today"
                task.due_class = "bg-warning-subtle text-warning-emphasis"
            else:
                task.overdue_days = delta
                task.due_status = f"Due in {abs(delta)} days"
                task.due_class = "bg-success-subtle text-success-emphasis"
        else:
            task.overdue_days = None
            task.due_status = "No due date"
            task.due_class = "bg-secondary-subtle text-secondary-emphasis"

    return render(request, "tasks.html", {"tasks": tasks, "contacts": contacts, "companies": companies})


def task_dashboard_counts(request):
    total = Task.objects.count()
    pending = Task.objects.filter(status=Task.STATUS_PENDING).count()
    due_today = Task.objects.filter(due_date=timezone.localdate()).count()
    overdue = Task.objects.filter(due_date__lt=timezone.localdate(), status__in=[Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS]).count()

    return JsonResponse({
        "totalTasks": total,
        "pending": pending,
        "dueToday": due_today,
        "overdue": overdue,
    })


@require_POST
def task_save(request):
    """
    Handles both create and update.
    Expects a hidden 'id' in form for edit (same pattern as company_save).
    """
    pk = request.POST.get("id")
    if pk:
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(request.POST)

    if form.is_valid():
        task = form.save(commit=False)
        # if status moved to completed set timestamp
        if task.status == Task.STATUS_COMPLETED and task.completed_at is None:
            task.completed_at = timezone.now()
        if task.status != Task.STATUS_COMPLETED:
            task.completed_at = None
        task.save()
        messages.success(request, "Task saved.")
        return redirect("tasks_list")
    else:
        # if invalid, re-render page with errors — we'll show messages and re-open modal ideally.
        contacts = Contact.objects.all()
        companies = Company.objects.all()
        tasks = Task.objects.all()
        return render(request, "tasks.html", {
            "tasks": tasks,
            "contacts": contacts,
            "companies": companies,
            "form_errors": form.errors,
            "form_data": request.POST,
        })


@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("tasks_list")

@require_POST
def task_status_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    new_status = request.POST.get("status")
    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        if new_status == Task.STATUS_COMPLETED:
            task.completed_at = timezone.now()
        else:
            task.completed_at = None
        task.save()
        messages.success(request, "Task status updated.")
        return redirect("tasks_list")
    else:
        messages.error(request, "Invalid status.")
        return redirect("tasks_list")
    

from .models import Activity
from django.utils.timezone import now

def activities(request):
    activities = Activity.objects.all().order_by("-date_time")
    contacts = Contact.objects.all()
    companies = Company.objects.all()
    stats = {
        "total": activities.count(),
        "calls": activities.filter(type="Call").count(),
        "emails": activities.filter(type="Email").count(),
        "meetings": activities.filter(type="Meeting").count(),
    }

    return render(request, "activities.html", {
        "activities": activities,
        "contacts": contacts,
        "companies": companies,
        "stats": stats,
    })

def activity_add(request):
    if request.method == "POST":
        Activity.objects.create(
            type=request.POST["type"],
            title=request.POST["title"],
            description=request.POST.get("description", ""),
            date_time=request.POST["date_time"],
            contact=Contact.objects.get(id=request.POST["contact"]) if request.POST.get("contact") else None,
            company=Company.objects.get(id=request.POST["company"]) if request.POST.get("company") else None,
            outcome=request.POST.get("outcome", ""),
        )
    return redirect("activities")

def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.type = request.POST["type"]
        activity.title = request.POST["title"]
        activity.description = request.POST.get("description", "")
        activity.date_time = request.POST["date_time"]
        activity.contact = Contact.objects.get(id=request.POST["contact"]) if request.POST.get("contact") else None
        activity.company = Company.objects.get(id=request.POST["company"]) if request.POST.get("company") else None
        activity.outcome = request.POST.get("outcome", "")
        activity.save()
        return redirect("activities")
    return render(request, "activity_edit.html", {"activity": activity})


def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity.delete()
    return redirect("activities")