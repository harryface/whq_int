# Generated by Django 4.1 on 2022-08-07 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('amount_paid', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('hours_worked', models.FloatField()),
                ('employee_id', models.IntegerField()),
                ('job_group', models.CharField(max_length=1)),
                ('csv_file_id', models.CharField(max_length=255)),
            ],
        ),
    ]
