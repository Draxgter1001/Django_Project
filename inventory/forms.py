# forms.py
from .models import UserProfile, Reservation, Equipment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['equipment', 'start_date', 'end_date', 'purpose']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
