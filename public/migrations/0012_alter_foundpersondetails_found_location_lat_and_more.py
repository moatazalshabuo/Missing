# Generated by Django 5.0.6 on 2024-07-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_foundpersondetails_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundpersondetails',
            name='found_location_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='خط العرض لمكان العثور'),
        ),
        migrations.AlterField(
            model_name='foundpersondetails',
            name='found_location_lng',
            field=models.FloatField(blank=True, null=True, verbose_name='خط الطول لمكان العثور'),
        ),
    ]
