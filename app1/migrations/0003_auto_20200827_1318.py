# Generated by Django 3.0.3 on 2020-08-27 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20200827_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='location',
        ),
        migrations.DeleteModel(
            name='Landmark',
        ),
    ]
