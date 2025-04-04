# Generated by Django 2.2.28 on 2025-03-22 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoeats', '0008_auto_20250322_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True),
        ),
    ]
