# admin.py
from django.contrib import admin
from .models import UserProfile, Equipment, Reservation, Location


# Custom ModelAdmin classes
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity', 'availability', 'onsite_only', 'status', 'comments')
    list_filter = ('type', 'availability', 'onsite_only')
    search_fields = ('name',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'start_date', 'end_date', 'status', 'purpose', 'quantity')
    list_filter = ('user', 'equipment', 'start_date', 'end_date')


# Register models with their respective ModelAdmin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Location)
