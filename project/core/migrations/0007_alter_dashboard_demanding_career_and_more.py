# Generated by Django 4.1.6 on 2023-05-29 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_dashboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='demanding_career',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='recruiting_companies',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='trending_skill',
            field=models.JSONField(),
        ),
    ]