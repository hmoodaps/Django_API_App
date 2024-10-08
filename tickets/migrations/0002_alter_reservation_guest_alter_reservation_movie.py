# Generated by Django 5.1 on 2024-08-31 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rez', to='tickets.guest'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rez', to='tickets.movie'),
        ),
    ]
