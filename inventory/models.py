# models.py
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class Location(models.Model):
    class LocationList(models.TextChoices):
        OTHER = 'Other', _('Other')
        XRLab_Blue_Cabinet = 'XRLab Blue Cabinet', _('XRLab Blue')
        XRLab_Blue_Cabinet_Large = 'XRLab Blue Cabinet Large', _('XRLab Blue Cabinet Large')
        XRLab_Medium_Wooden_Cabinet = 'XRLab Medium Wooden Cabinet', _('XRLab Medium Wooden Cabinet')

    location_name = models.CharField(max_length=255, null=True, blank=True, default="Default Location")
    location_type = models.CharField(max_length=50, choices=LocationList.choices, default="")

    def __str__(self):
        return f'{self.location_name}'


class Equipment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True)
    last_audit = models.DateField(null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    onsite_only = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Reservation(models.Model):
    class ReservationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        APPROVED = 'Approved', _('Approved')
        REJECTED = 'Rejected', _('Rejected')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    purpose = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.equipment.name}'
