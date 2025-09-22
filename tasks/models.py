from django.db import models
from django.utils import timezone
from contacts.models import Contact
from companies.models import Company

class Task(models.Model):
    TYPE_FOLLOW_UP = "Follow-up Call"
    TYPE_SEND_QUOTE = "Send Quote"
    TYPE_MEETING = "Meeting"
    TYPE_EMAIL = "Email"
    TYPE_RESEARCH = "Research"
    TYPE_OTHER = "Other"

    TYPE_CHOICES = [
        (TYPE_FOLLOW_UP, "Follow-up Call"),
        (TYPE_SEND_QUOTE, "Send Quote"),
        (TYPE_MEETING, "Meeting"),
        (TYPE_EMAIL, "Email"),
        (TYPE_RESEARCH, "Research"),
        (TYPE_OTHER, "Other"),
    ]

    PRIORITY_LOW = "Low"
    PRIORITY_MEDIUM = "Medium"
    PRIORITY_HIGH = "High"
    PRIORITY_URGENT = "Urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    STATUS_PENDING = "Pending"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True, related_name="tasks"
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True, related_name="tasks"
    )
    due_date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TYPE_OTHER)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-due_date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class Activity(models.Model):
    TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('WhatsApp', 'WhatsApp'),
        ('SMS', 'SMS'),
        ('Note', 'Note'),
    ]
    OUTCOME_CHOICES = [
        ('Positive', 'Positive'),
        ('Neutral', 'Neutral'),
        ('Negative', 'Negative'),
        ('Follow-up Required', 'Follow-up Required'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    outcome = models.CharField(max_length=50, choices=OUTCOME_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
