# Generated by Django 4.0.3 on 2022-03-12 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_pictutre_book_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='count',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='sold_count',
            new_name='sold_quantity',
        ),
    ]
