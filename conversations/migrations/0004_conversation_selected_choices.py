# Generated by Django 4.2.11 on 2024-05-24 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0003_alter_message_conversation'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='selected_choices',
            field=models.JSONField(blank=True, default=list),
        ),
    ]