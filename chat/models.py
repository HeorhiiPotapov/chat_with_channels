from django.db.models.signals import m2m_changed
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User, related_name='user_rooms')
    logo = models.ImageField(
        upload_to='group_logo/%Y/%m/%d', default="default/group_logo.png")
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="first_user")
    second_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name="second_user",
                                    null=True,
                                    blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chat:room", kwargs={"room_name": self.name})

    def clean(self):
        super().clean()
        if self.is_private is True and not self.second_user:
            raise ValidationError('second user not specified')

    def save(self, *args, **kwargs):
        if self.is_private is True:
            if not self.second_user:
                raise ValueError("No second user specified")
        super(ChatRoom, self).save(*args, **kwargs)


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='room_messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.id, self.sender.name)


def members_count_changed(sender, **kwargs):
    if kwargs['instance'].is_private is True and kwargs['instance'].members.count() > 2:
        raise ValidationError(
            "You can't assign more than two members to private chat room"
        )


m2m_changed.connect(members_count_changed, sender=ChatRoom.members.through)
