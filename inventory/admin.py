# admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import UserProfile, Equipment, Reservation, Location, EquipmentUsageHistory


# Custom ModelAdmin classes
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity', 'availability', 'onsite_only', 'status', 'comments',
                    'inventory_report_link')
    list_filter = ('type', 'availability', 'onsite_only')
    search_fields = ('name',)

    def inventory_report_link(self, obj):
        url = reverse('inventory:download_inventory_report')
        return format_html('<a href="{}">Download Inventory Report</a>', url)

    inventory_report_link.short_description = 'Inventory Report'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'start_date', 'end_date', 'status', 'purpose', 'quantity')
    list_filter = ('user', 'equipment', 'start_date', 'end_date')


class EquipmentUsageHistoryAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'times_reserved', 'last_reserved', 'download_report_link']

    def download_report_link(self, obj):
        return format_html('<a href="{}">Download PDF</a>', reverse('download_report', args=[obj.pk]))

    download_report_link.short_description = 'Download Report'


# Register models with their respective ModelAdmin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Location)
admin.site.register(EquipmentUsageHistory, EquipmentUsageHistoryAdmin)
