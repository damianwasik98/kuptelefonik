# Generated by Django 3.1.7 on 2021-04-27 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_phone_observed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='shops')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('currency', models.CharField(max_length=3)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.phone')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop')),
            ],
        ),
    ]
