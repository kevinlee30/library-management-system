# Generated by Django 4.0 on 2022-12-28 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('title', models.CharField(max_length=200, verbose_name='Highlight Title')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.book')),
                ('imgUrl', models.CharField(max_length=200, verbose_name='Image URL')),
            ],
        ),
    ]