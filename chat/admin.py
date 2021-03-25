
from django.contrib import admin
from .models import ChatRoom, Message


admin.site.register(ChatRoom)


class MessageAdmin(admin.ModelAdmin):
    list_filter = ('room', 'sender')


admin.site.register(Message, MessageAdmin)
