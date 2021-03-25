from django import forms
from django.core import validators
from .models import ChatRoom


class ChatRoomCreateForm(forms.ModelForm):
    name = forms.CharField(min_length=5, validators=[validators.validate_slug])

    class Meta:
        model = ChatRoom
        fields = ('name',)
