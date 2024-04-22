from openpyxl import load_workbook
from django.core.management.base import BaseCommand
from inventory.models import Equipment, Location
from django.db import transaction


class Command(BaseCommand):
    help = 'Load equipment data from Excel file using openpyxl'

    def handle(self, *args, **options):
        file_path = r'C:\Users\uthsh\PycharmProjects\djangoProjectGroup\Equiment  Inventory.xlsx'
        wb = load_workbook(filename=file_path)
        ws = wb.active

        with transaction.atomic():
            for row in ws.iter_rows(min_row=2, values_only=True):
                if len(row) < 7:  # Check if the row has less than 7 columns
                    continue  # Skip this row or handle the error as needed

                location_name = row[4]
                location, _ = Location.objects.get_or_create(
                    location_name=location_name,
                    defaults={'location_type': 'Default'}
                )

                Equipment.objects.update_or_create(
                    name=row[0],
                    defaults={
                        'type': row[1],
                        'quantity': row[2],
                        'last_audit': row[3],
                        'location': location,
                        'status': row[5] if row[5] else '',
                        'comments': row[6] if row[6] else ''
                    }
                )
        print('Data import complete')
