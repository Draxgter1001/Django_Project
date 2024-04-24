# views.py
import json
from datetime import date

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView
from .forms import UserRegisterForm, ReservationForm
from .models import Equipment, Reservation, UserProfile, Location


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
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'inventory/bookingList.html', {'reservations': reservations})


@method_decorator(login_required, name='dispatch')
class ReservationCreateView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        equipment_id = data.get('equipment_id')
        quantity = data.get('quantity')

        try:
            equipment = Equipment.objects.get(pk=equipment_id)
            if equipment.quantity < int(quantity):
                return JsonResponse({'error': 'Requested quantity exceeds available quantity.'}, status=400)

            reservation = Reservation.objects.create(
                user=request.user,
                equipment=equipment,
                start_date=date.today(),
                end_date=date.today(),  # Set end_date as needed
                purpose='',  # Set purpose as needed
                quantity=int(quantity),  # Add the quantity field
            )
            equipment.quantity -= int(quantity)
            equipment.save()

            return JsonResponse({'message': 'Reservation created successfully.'}, status=200)
        except Equipment.DoesNotExist:
            return JsonResponse({'error': 'Equipment not found.'}, status=404)


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
