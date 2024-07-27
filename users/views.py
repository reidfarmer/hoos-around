from django.shortcuts import render
from django.views import generic
from .models import User
from django.conf import settings


class Login(generic.TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_page = self.request.GET.get('next')
        context['user'] = self.request.user
        context['is_admin'] = self.is_admin()
        context['next'] = next_page
        return context

    def get_queryset(self):
        return User.objects.all()

    def is_admin(self):
        return self.request.user.groups.filter(name='Admins').exists()

    def get_success_url(self):
        return "map/home.html"
