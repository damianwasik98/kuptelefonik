# Generated by Django 3.1.7 on 2021-04-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='color',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
