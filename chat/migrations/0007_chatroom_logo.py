# Generated by Django 3.1.5 on 2021-02-15 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_chatroom_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='logo',
            field=models.ImageField(default='default/group_logo.png', upload_to='group_logo/%Y/%m/%d'),
        ),
    ]