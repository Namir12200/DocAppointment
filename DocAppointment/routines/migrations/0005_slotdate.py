# Generated by Django 5.0.6 on 2024-07-10 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0004_alter_doctorroutine_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('nextDate', models.IntegerField(null=True)),
                ('total_patients', models.IntegerField()),
                ('slot', models.IntegerField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routines.doctorroutine')),
            ],
        ),
    ]