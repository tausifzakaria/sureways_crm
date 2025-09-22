from django.db import models
from contacts.models import Contact
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='active')
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="e.g Supplier, Customer, Forwarder")
    source = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    linked_contacts = models.ManyToManyField(Contact, related_name="companies", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def contact_count(self):
        return self.linked_contacts.count()

    def __str__(self):
        return self.name