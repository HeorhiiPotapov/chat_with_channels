from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .tokens import account_activation_token
from .models import Profile

User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:waiting_for_activation')
    template_name = 'users/registration.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('users/activation/message.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return super().form_valid(form)


class ActivationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            print(e)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('chat:index')
        else:
            return redirect('users:activation_failed')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.pk)
        profile = Profile.objects.get(user=user)

        return render(request, 'users/profile.html', {
            'user': user,
            'profile': profile})
