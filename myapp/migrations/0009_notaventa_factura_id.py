# Generated by Django 5.1.3 on 2024-11-24 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_notaventa_factura_id_notaventaparabrisa'),
    ]

    operations = [
        migrations.AddField(
            model_name='notaventa',
            name='factura_id',
            field=models.IntegerField(db_column='factura_id', default=0),
        ),
    ]
