from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils import timezone
from .models import NotaVenta, NotaCompra, Almacen
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.timezone import now

def ventas_mensuales_data(request):
    current_year = now().year  # Obtiene el año actual

    ventas_mensuales = NotaVenta.objects.annotate(
        mes=ExtractMonth('fecha'),
        anio=ExtractYear('fecha')
    ).filter(
        anio=current_year  # Filtra solo registros del año actual
    ).values('mes').annotate(
        total=Sum('monto_total')
    ).order_by('mes')

    data = {
        "categories": [item['mes'] for item in ventas_mensuales],
        "values": [item['total'] for item in ventas_mensuales]
    }
    print(data, "ventas_mensuales_data")
    return JsonResponse(data)

def ventas_por_almacen_data(request): 
    current_year = now().year  # Obtiene el año actual
    
    # Filtrar las ventas solo para el año actual
    ventas_por_almacen = NotaVenta.objects.filter(
        fecha__year=current_year  # Filtra solo registros del año actual
    ).values(
        'almacen_id__nombre'
    ).annotate(
        total=Sum('monto_total')
    ).order_by('almacen_id__nombre')

    data = {
        "categories": [item['almacen_id__nombre'] for item in ventas_por_almacen],
        "values": [item['total'] for item in ventas_por_almacen]
    }
    #print(data, "ventas_por_almacen_data")
    return JsonResponse(data)


def compras_ultimo_mes_data(request):
    # Agrupa las compras por mes del año actual y suma el importe total
    compras_mensuales = NotaCompra.objects.filter(
        fecha__year=timezone.now().year
    ).annotate(
        mes=ExtractMonth('fecha')  # Extrae el mes de la fecha
    ).values(
        'mes'
    ).annotate(
        total_gasto=Sum('importe_total')  # Suma del importe total por mes
    ).order_by('mes')

    # Prepara los datos para el gráfico
    data = {
        "categories": [item['mes'] for item in compras_mensuales],
        "values": [item['total_gasto'] for item in compras_mensuales]
    }

    #print(data, "compras_mensuales_data")  # Para depuración
    return JsonResponse(data)




def compras_por_proveedor_data(request):
    compras_por_proveedor = NotaCompra.objects.filter(
        fecha__year=timezone.now().year
    ).values(
        'proveedor_id__nombre'
    ).annotate(
        total=Sum('importe_total')
    ).order_by('-total')

    data = {
        "categories": [item['proveedor_id__nombre'] for item in compras_por_proveedor],
        "values": [item['total'] for item in compras_por_proveedor]
    }
    #print(data,"compras_por_proveedor_data")
    return JsonResponse(data)

def ocupacion_almacenes_data(request):
    ocupacion_almacenes = Almacen.objects.annotate(
        ocupado=Sum('almacenparabrisa__stock')
    ).values('nombre', 'capacidad', 'ocupado')

    data = {
        "categories": [item['nombre'] for item in ocupacion_almacenes],
        "stock": [item['ocupado'] for item in ocupacion_almacenes],
        "capacity": [item['capacidad'] for item in ocupacion_almacenes]
    }
    #print(data, "ocupacion_almacenes_data")
    return JsonResponse(data)

def clientes_mas_compran_data(request):
    clientes_mas_compran = NotaVenta.objects.filter(
        fecha__year=timezone.now().year
    ).values(
        'cliente_id__nombre'
    ).annotate(
        total=Sum('monto_total')
    ).order_by('-total')[:10]
    

    data = {
        "categories": [item['cliente_id__nombre'] for item in clientes_mas_compran],
        "values": [item['total'] for item in clientes_mas_compran]
    }
    #print(data,"clientes_mas_compran_data")
    return JsonResponse(data)