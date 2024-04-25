# views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .forms import UserRegisterForm, ReservationForm
from .models import Equipment, Reservation, UserProfile, Location, EquipmentUsageHistory


# Authentication and Registration Views

@login_required
def home(request):
    return render(request, 'inventory/home.html')


@login_required
def edit_account(request):
    return render(request, "registration/editAccount.html")


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('inventory:successful_registration')

    def form_valid(self, form):
        user = form.save()
        UserProfile.objects.update_or_create(user=user, defaults={'is_approved': False})
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


# Equipment Views

class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    context_object_name = 'equipment_list'
    template_name = 'inventory/equipment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_types'] = Equipment.objects.values_list('type', flat=True).distinct()
        context['equipment_locations'] = Location.objects.values_list('location_name', flat=True).distinct()
        return context


# Reservation Views

@login_required
def booking_view(request):
    reservations = (Reservation.objects.filter(user=request.user).select_related('equipment', 'equipment__location')
                    .order_by('-start_date'))
    return render(request, 'inventory/bookingList.html', {'reservations': reservations})


@login_required
def cancel_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk, user=request.user)
        if reservation.status not in [Reservation.ReservationStatus.APPROVED, Reservation.ReservationStatus.PENDING]:
            messages.error(request, "Cannot cancel a reservation that is not pending or approved.")
        else:
            equipment = reservation.equipment
            equipment.quantity += reservation.quantity  # Restore the equipment quantity
            equipment.save()
            reservation.delete()
            messages.success(request, "Reservation cancelled successfully.")
    except Reservation.DoesNotExist:
        messages.error(request, "Reservation not found.")
    return HttpResponseRedirect(reverse('inventory:booking_view'))


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('inventory:booking_view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        reservation = form.save(commit=False)
        equipment = reservation.equipment

        if equipment.quantity >= reservation.quantity:
            equipment.quantity -= reservation.quantity
            equipment.save()
            messages.success(self.request, "Reservation successfully created.")
            return super().form_valid(form)
        else:
            form.add_error('quantity', 'Insufficient quantity available.')
            return self.form_invalid(form)


# Miscellaneous Views

def successful_registration(request):
    return render(request, 'registration/successfulRegistration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.is_approved:
                    login(request, user)
                    return redirect('inventory:home')
                else:
                    messages.error(request, 'Your account is pending approval.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


@login_required
@staff_member_required  # Replace this with the actual permission check for admins
def download_report(request, pk):
    equipment_usage_history = EquipmentUsageHistory.objects.get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="{equipment_usage_history.equipment.name}_usage_report.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF.
    p.drawString(100, 800, f"Usage Report for: {equipment_usage_history.equipment.name}")
    p.drawString(100, 780, f"Times Reserved: {equipment_usage_history.times_reserved}")
    if equipment_usage_history.last_reserved:
        p.drawString(100, 760, f"Last Reserved On: {equipment_usage_history.last_reserved.strftime('%Y-%m-%d')}")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()
    return response


@login_required
@staff_member_required
def download_inventory_report(request):
    equipment_list = Equipment.objects.all().select_related('location')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Starting Y position near the top of the page
    y_position = height - inch * 1
    line_height = 0.2 * inch  # Define the space needed for each line, including some space between lines

    # Define columns positions based on the page width
    column_1_x = inch * 0.5
    column_2_x = width / 4
    column_3_x = width / 2
    column_4_x = width * 3 / 4

    # Print header
    p.setFont("Helvetica-Bold", 14)
    p.drawString(column_1_x, y_position, "Inventory Report")
    y_position -= inch / 2

    p.setFont("Helvetica", 7)

    # Iterate through the equipment list and write to the PDF
    for equipment in equipment_list:
        # Check if we need to start a new page
        if y_position < inch:
            p.showPage()
            y_position = height - inch * 1  # Reset y_position for the new page
            p.setFont("Helvetica", 7)

        p.drawString(column_1_x, y_position, f"{equipment.name}")
        p.drawString(column_2_x, y_position, f"{equipment.type}")
        p.drawString(column_3_x, y_position, f"{equipment.quantity}")
        p.drawString(column_4_x, y_position, f"{equipment.location}")

        y_position -= line_height  # Decrement the y_position for the next line

    p.showPage()
    p.save()
    return response
