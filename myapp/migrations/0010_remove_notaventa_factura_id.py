# Generated by Django 5.1.3 on 2024-11-24 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_notaventa_factura_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notaventa',
            name='factura_id',
        ),
    ]
