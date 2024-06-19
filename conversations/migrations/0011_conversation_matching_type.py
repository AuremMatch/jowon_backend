# Generated by Django 4.2.11 on 2024-06-18 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0010_conversation_시상금_conversation_응모분야_conversation_접수기간_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='matching_type',
            field=models.CharField(choices=[('random', 'Random Matching'), ('top_two', 'Top Two Matching'), ('same', 'Same Matching')], default='random', max_length=10),
        ),
    ]
