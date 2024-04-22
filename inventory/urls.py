# App-level urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import SignUpView, home, EquipmentListView, ReservationCreateView, profile_view, successful_registration

app_name = 'inventory'  # Define the app namespace

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inventory:login'), name='logout'),
    path('register/', views.register, name='register'),  # Make sure to point to the correct register view
    path('successfulRegistration/', views.successful_registration, name='successful_registration'),
    path('home/', home, name='home'),
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('reserve/', ReservationCreateView.as_view(), name='reserve_equipment'),
    path('profile/', profile_view, name='profile'),


    # ... any other app-specific patterns
]
