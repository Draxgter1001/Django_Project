# admin.py
from django.contrib import admin
from .models import UserProfile, Equipment, Reservation, Location


# Custom ModelAdmin classes
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity', 'availability', 'onsite_only', 'status', 'comments')
    list_filter = ('type', 'availability', 'onsite_only')
    search_fields = ('name',)


# Register models with their respective ModelAdmin classes
admin.site.register(UserProfile)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Reservation)
admin.site.register(Location)

