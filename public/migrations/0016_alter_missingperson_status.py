# Generated by Django 5.0.6 on 2024-08-05 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0015_reportinformation_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missingperson',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
