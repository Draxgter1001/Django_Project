# views.py
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Equipment, Reservation, UserProfile
from .forms import UserRegisterForm, ReservationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'inventory/home.html')


def profile_view(request):
    return render(request, 'inventory/profile.html')


def successful_registration(request):
    return render(request, 'registration/successfulRegistration.html')


# views.py

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Create the UserProfile instance
            UserProfile.objects.create(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                is_approved=False
            )

            return redirect('inventory:successful_registration')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def reserve_view(request):
    return render(request, 'inventory/reserve_equipment.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        print(f"User: {user}")  # Debug statement

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                print(f"User Profile: {user_profile}")  # Debug statement
                print(f"Is Approved: {user_profile.is_approved}")  # Debug statement
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

    return render(request, 'registration/login.html')

class EquipmentListView(ListView):
    model = Equipment
    context_object_name = 'equipment_list'
    template_name = 'inventory/equipment_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Example filtering by availability
        availability = self.request.GET.get('availability', '')
        if availability:
            queryset = queryset.filter(availability=availability == 'True')
        # Example searching by name
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


@method_decorator(login_required, name='dispatch')
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'inventory/reserve_equipment.html'
    success_url = reverse_lazy('inventory:home')

    # Redirect to the home page after successful reservation

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
