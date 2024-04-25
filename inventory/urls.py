# App-level urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'inventory'  # Define the app namespace

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inventory:login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('successful-registration/', views.successful_registration, name='successful_registration'),
    path('home/', views.home, name='home'),
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('reserve/', views.ReservationCreateView.as_view(), name='reserve_equipment'),
    path('booking/', views.booking_view, name='booking_view'),
    path('cancel-reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('edit-account/', views.edit_account, name='edit_account'),
    # Add other patterns as needed
]
