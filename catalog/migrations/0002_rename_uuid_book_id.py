# Generated by Django 4.0 on 2022-12-20 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='uuid',
            new_name='id',
        ),
    ]