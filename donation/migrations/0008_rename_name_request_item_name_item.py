# Generated by Django 4.0.6 on 2022-08-16 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0007_remove_request_name_remove_request_office_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request_item',
            old_name='name',
            new_name='name_item',
        ),
    ]
