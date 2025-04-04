# Generated by Django 2.2.28 on 2025-03-22 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoeats', '0006_auto_20250322_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='latitude',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='longitude',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=30),
        ),
    ]
