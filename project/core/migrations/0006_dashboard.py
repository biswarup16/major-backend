# Generated by Django 4.1.6 on 2023-05-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_profile_address_profile_bio_profile_cover_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demanding_career', models.TextField()),
                ('trending_skill', models.TextField()),
                ('recruiting_companies', models.TextField()),
            ],
        ),
    ]
