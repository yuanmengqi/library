# Generated by Django 5.0.6 on 2024-06-15 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_managerment', '0007_alter_lmsuser_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow',
            name='renew_date',
        ),
    ]
