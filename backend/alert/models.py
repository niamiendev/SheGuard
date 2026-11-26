import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

from django.db import models
from account.models import Profile


class Contact(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
    
    
class Alert(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        IN_PROGRESS = "IN_PROGRESS", "En cours"
        RESOLVED = "RESOLVED", "Résolue"
        CANCELLED = "CANCELLED", "Annulée"
        CALLED = "CALLED", "Appelle"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="alerts"
    )

    operateur = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_alerts"
    )

    contacts = models.ManyToManyField(
        Contact,
        blank=True,
        related_name="alerts"
    )

    latitude = models.FloatField()
    longitude = models.FloatField()

    address = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alerte {self.id} - {self.status}"