# Generated by Django 5.1.3 on 2024-11-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_notaventa_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parabrisas',
            name='categoria',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='notaventa',
            name='factura',
        ),
        migrations.AlterField(
            model_name='parabrisas',
            name='posicion',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='parabrisas',
            name='vehiculo',
            field=models.IntegerField(default=0),
        ),
        migrations.RenameField(
            model_name='almacenparabrisa',
            old_name='almacen',
            new_name='almacen_id',
        ),
        migrations.RenameField(
            model_name='almacenparabrisa',
            old_name='parabrisa',
            new_name='parabrisa_id',
        ),
        migrations.RenameField(
            model_name='notacompra',
            old_name='almacen',
            new_name='almacen_id',
        ),
        migrations.RenameField(
            model_name='notacompra',
            old_name='parabrisa',
            new_name='parabrisa_id',
        ),
        migrations.RenameField(
            model_name='notacompra',
            old_name='proveedor',
            new_name='proveedor_id',
        ),
        migrations.RenameField(
            model_name='notaventa',
            old_name='almacen',
            new_name='almacen_id',
        ),
        migrations.RenameField(
            model_name='notaventa',
            old_name='cliente',
            new_name='cliente_id',
        ),
        migrations.AddField(
            model_name='notaventa',
            name='factura_id',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.DeleteModel(
            name='Factura',
        ),
        migrations.DeleteModel(
            name='Posicion',
        ),
        migrations.DeleteModel(
            name='Vehiculo',
        ),
    ]
