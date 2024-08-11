from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name = 'logout.html'),
         name='logout'),
    path ('logout/confirm/', TemplateView.as_view(template_name = 'logout_confirm.html'), name = 'logout_confirm'),
]