# Generated by Django 2.0.5 on 2018-05-22 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20180327_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('created',)},
        ),
    ]