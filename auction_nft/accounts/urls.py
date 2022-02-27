"""auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy
app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/pass_change_form.html',success_url=reverse_lazy('accounts:password_change_done')),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/pass_change_done.html', ),name='password_change_done'),
    path('registration/', views.register_view, name='register'),
    path('ip_control/', views.ip_control_view, name='ip-control'),
    path('users/<int:id>/profile/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit')
]
