# Generated by Django 4.2.11 on 2024-05-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
