# Generated by Django 3.0.3 on 2020-05-18 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_profile.png', null=True, upload_to=''),
        ),
    ]
