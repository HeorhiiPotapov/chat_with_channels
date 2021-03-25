from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ActivationView, ProfileView
from django.views.generic import TemplateView


app_name = 'users'
urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name="logout"),
    path('waiting-for-activation/', TemplateView.as_view(
        template_name="users/activation/wait.html"),
        name="waiting_for_activation"),
    path('activation-fialed/', TemplateView.as_view(
        template_name="users/activation/fail.html"),
        name="activation_failed"),
    path('activate/<uidb64>/<token>/',
         ActivationView.as_view(), name='activate'),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),
]
