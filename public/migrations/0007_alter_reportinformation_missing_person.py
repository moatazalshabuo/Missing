# Generated by Django 5.0.6 on 2024-07-03 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0006_alter_missingperson_status_foundpersondetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportinformation',
            name='missing_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='public.missingperson'),
        ),
    ]
