# Generated by Django 5.0.6 on 2024-07-01 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missingperson',
            name='status',
            field=models.CharField(choices=[('0', 'في انتظار'), ('1', 'مفقود'), ('2', 'تم العثور'), ('3', 'رفض')], default=1, max_length=10),
        ),
        migrations.CreateModel(
            name='FoundPersonDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('found_date', models.DateField(verbose_name='تاريخ العثور')),
                ('found_location_lat', models.FloatField(verbose_name='خط العرض لمكان العثور')),
                ('found_location_lng', models.FloatField(verbose_name='خط الطول لمكان العثور')),
                ('current_health_status', models.TextField(verbose_name='الحالة الصحية الحالية')),
                ('other_detiles', models.TextField(verbose_name='تفاصيل اخرى')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='found_person_details', to='public.missingperson')),
            ],
        ),
    ]
