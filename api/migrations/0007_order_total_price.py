# Generated by Django 4.0.3 on 2022-03-12 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
