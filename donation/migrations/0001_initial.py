# Generated by Django 4.0.6 on 2022-08-03 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('office_count', models.IntegerField(null=True)),
                ('capacity', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('state', models.CharField(choices=[('Available', 'Available'), ('Requested', 'Requested'), ('Booked', 'Booked'), ('Shipped', 'Shipped')], default='Available', max_length=100)),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donation.office')),
            ],
        ),
    ]
