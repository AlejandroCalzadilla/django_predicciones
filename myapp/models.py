# myapp/models.py
from django.db import models

class Almacen(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    nombre = models.CharField(max_length=255)
    capacidad = models.IntegerField()

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    nombre = models.CharField(max_length=255)

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    nombre = models.CharField(max_length=255)

class Parabrisas(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    descripcion = models.CharField(max_length=255)
    categoria_id = models.IntegerField(default=0)
    posicion_id = models.IntegerField(default=0)
    vehiculo_id = models.IntegerField(default=0)
    observacion = models.CharField(max_length=255, default='sirve')

class NotaCompra(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    fecha = models.DateField()
    cantidad = models.IntegerField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    parabrisa_id = models.ForeignKey(Parabrisas, on_delete=models.CASCADE, db_column='parabrisa_id')
    proveedor_id = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='proveedor_id')
    almacen_id = models.ForeignKey(Almacen, on_delete=models.CASCADE, db_column='almacen_id')

class NotaVenta(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    fecha = models.DateField()
    user_id = models.IntegerField(default=0)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cliente_id')
    almacen_id = models.ForeignKey(Almacen, on_delete=models.CASCADE, db_column='almacen_id')
    #factura_id = models.IntegerField(default=0, db_column='factura_id')


class AlmacenParabrisa(models.Model):
    id = models.AutoField(primary_key=True)  # Permitir que el ID sea proporcionado
    almacen_id = models.ForeignKey(Almacen, on_delete=models.CASCADE, db_column='almacen_id')
    parabrisa_id = models.ForeignKey(Parabrisas, on_delete=models.CASCADE, db_column='parabrisa_id')
    stock = models.IntegerField()



class NotaVentaParabrisa(models.Model):
    id = models.AutoField(primary_key=True)
    nota_venta_id = models.ForeignKey(NotaVenta, on_delete=models.CASCADE,db_column='nota_venta_id')
    parabrisa_id = models.ForeignKey(Parabrisas, on_delete=models.CASCADE,db_column='parabrisa_id')
    cantidad = models.IntegerField()



