# Generated by Django 5.0.7 on 2024-07-17 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbotapp', '0003_delete_todoitem_stock_graph_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='shares',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
