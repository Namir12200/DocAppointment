# Generated by Django 5.0.6 on 2024-07-07 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorroutine',
            name='first_date',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorroutine',
            name='last_date',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]