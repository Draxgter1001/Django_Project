# Tafshi Uthshow Hoque & Rafael Rojas Luppichini
# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Equipment
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    # def clean_date_of_birth(self):
    #     date_of_birth = self.cleaned_data.get('date_of_birth')
    #     today = datetime.date.today()
    #     age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    #     if age < 18:
    #         raise ValidationError("You must be at least 18 years old to register.")
    #     return date_of_birth


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}))

    class Meta:
        model = Reservation
        fields = ['equipment', 'start_date', 'purpose', 'quantity']

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < timezone.now().date():
            raise forms.ValidationError("The start date must be today or in the future.")

        return start_date


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
