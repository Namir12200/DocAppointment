# Generated by Django 5.0.6 on 2024-07-07 13:41

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_profile_is_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorRoutine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=255)),
                ('visiting_cost', models.IntegerField()),
                ('new_customer_cost', models.IntegerField()),
                ('patients_per_day', models.PositiveSmallIntegerField()),
                ('days', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('SUN', 'Sunday'), ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')], max_length=3), size=7, unique=True)),
                ('first_date', models.IntegerField(null=True)),
                ('last_date', models.IntegerField(null=True)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
