# Tafshi Uthshow Hoque, Rafael Rojas Vivanc & Rishabh Kabawala
# App-level urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import download_report, download_inventory_report

app_name = 'inventory'  # Define the app namespace

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inventory:login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('successful-registration/', views.successful_registration, name='successful_registration'),

    path('successfulRegistration/', views.successful_registration, name='successful_registration'),

    path('home/', views.home, name='home'),
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('reserve/', views.ReservationCreateView.as_view(), name='reserve_equipment'),
    path('booking/', views.booking_view, name='booking_view'),

    path('cancel-reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('report/download/<int:pk>/', download_report, name='download_report'),
    path('report/download-inventory/', download_inventory_report, name='download_inventory_report'),


    path('edit-account/', views.edit_account, name='edit_account'),

    # Add other patterns as needed
]
