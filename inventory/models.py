# Tafshi Uthshow Hoque, Rafael Rojas Vivanc & Rishabh Kabawala

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # date_of_birth = models.DateField(null=True, blank=False) Notice in development that the DOB is not needed.
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


# Done
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

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.availability = False
        else:
            self.availability = True

        super(Equipment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Reservation(models.Model):
    class ReservationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        APPROVED = 'Approved', _('Approved')
        REJECTED = 'Rejected', _('Rejected')
        CANCELED = 'Canceled', _('Canceled')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    purpose = models.TextField()
    quantity = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        # Check if the status has been changed to 'Canceled'
        if (self.pk and self.status == self.ReservationStatus.CANCELED and self.__original_status !=
                self.ReservationStatus.CANCELED):
            # Increment the equipment's quantity by the canceled reservation's quantity
            self.equipment.quantity += self.quantity
            self.equipment.save()

        super().save(*args, **kwargs)
        self.__original_status = self.status  # Update the original status after saving

    def __str__(self):
        return f'{self.user.username} - {self.equipment.name}'


class EquipmentUsageHistory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    times_reserved = models.IntegerField(default=0)
    last_reserved = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipment.name} usage history"


# Update the Reservation model's safe method to increment the times_reserved
@receiver(post_save, sender=Reservation)
def update_usage_history(sender, instance, created, **kwargs):
    if created:
        history, _ = EquipmentUsageHistory.objects.get_or_create(equipment=instance.equipment)
        history.times_reserved += 1
        history.last_reserved = instance.start_date
        history.save()


@receiver(post_delete, sender=Reservation)
def decrement_usage_history(sender, instance, **kwargs):
    history = EquipmentUsageHistory.objects.filter(equipment=instance.equipment).first()
    if history:
        history.times_reserved -= 1
        history.save()
