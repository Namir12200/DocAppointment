# Generated by Django 5.0.6 on 2024-07-13 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientRecord', '0002_alter_patienthistory_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patienthistory',
            name='visit_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
