"""
URL configuration for hoos_around project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import reverse
import map.views


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name="index.html"), name='login'),
#     path('accounts/', include('allauth.urls'), name='accounts'),
#     # path('logout', LogoutView.as_view(), name='logout'),
# ]
from django.contrib.auth import views as auth_views
from users import views

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


# Title: Signals
# URL: https://docs.djangoproject.com/en/4.2/topics/signals/
# Used to check if the user currently logging in is an admin

@receiver(post_save, sender=User)
def add_user_to_admin_group(sender, instance, **kwargs):
    # print(f'Signal triggered: Email: {instance.email}')
    # List of email addresses that should be considered as admin emails
    admin_emails = ['tmt5zv@virginia.edu', 'reidfarmer62@gmail.com']

    if instance.email in admin_emails:
        group, _ = Group.objects.get_or_create(name='Admins')
        permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(User))
        group.permissions.add(*permissions)
        instance.groups.add(group)

urlpatterns = [
    # path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin_login'),
    # path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
    path('superAccess/', admin.site.urls),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('', views.Login.as_view(), name='directLogin'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),  # Social authentication URLs
    path('home/', include("map.urls"), name="home"),
    # path('events/', views.CreateView.as_view(), name='createEvent'),
]
