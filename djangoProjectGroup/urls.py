# Project-level urls.py
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', RedirectView.as_view(pattern_name='inventory:login', permanent=False)),
    path('inventory/', include('inventory.urls')),  # Include the 'inventory' app URLconf
    # ... any other project-level URL patterns
]