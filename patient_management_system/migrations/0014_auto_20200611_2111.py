# Generated by Django 3.0.5 on 2020-06-11 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management_system', '0013_auto_20200611_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors_database',
            name='date_of_joining',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
