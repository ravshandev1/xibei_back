# Generated by Django 4.2 on 2023-04-24 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rate_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='rate',
        ),
    ]
