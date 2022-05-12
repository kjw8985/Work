# Generated by Django 4.0.4 on 2022-05-12 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('location', models.TextField()),
                ('scale', models.CharField(max_length=20)),
                ('inquiry', models.TextField()),
                ('tel', models.IntegerField(null=True)),
                ('Announcement_date', models.DateField()),
                ('receipt_date', models.DateField()),
                ('release_date', models.DateField()),
                ('contract_date', models.DateField()),
                ('local', models.DateField()),
                ('etc', models.DateField()),
                ('Reception_place', models.CharField(max_length=10)),
                ('division', models.CharField(max_length=10)),
                ('acreage', models.CharField(max_length=10, null=True)),
                ('supply_area', models.DecimalField(decimal_places=2, max_digits=3)),
                ('supply_normal', models.IntegerField()),
                ('supply_special', models.IntegerField()),
                ('supply_total', models.IntegerField()),
                ('price', models.CharField(max_length=20, null=True)),
                ('views', models.IntegerField()),
                ('date_start', models.DateField()),
                ('date_finish', models.DateField()),
                ('size_one', models.DecimalField(decimal_places=4, max_digits=8)),
                ('size_two', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('price_one', models.CharField(max_length=20)),
                ('price_two', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
