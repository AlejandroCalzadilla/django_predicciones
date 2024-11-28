# myapp/api_client.py
import os
import django
import requests
from django.conf import settings
from .models import NotaCompra, NotaVenta, Parabrisas, Cliente, Proveedor, Almacen, AlmacenParabrisa,NotaVentaParabrisa

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

BASE_URL = 'http://localhost:8000/api'

def login(email, password):
    url = f'{BASE_URL}/login'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
    
        return response.json()  # Devuelve toda la respuesta JSON
    else:
        print('Error en el login:', response.json())
        return None

def logout(token):
    url = f'{BASE_URL}/logout'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print('Logout exitoso')
    else:
        print('Error en el logout:', response.json())

def get_data_from_api(endpoint, token):
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error al obtener los datos de {endpoint}:', response.json())
        return None

def save_data_to_db(data, model):
    for item in data:
        #print(f'Guardando item: {item}')  # Imprimir los datos recibidos
        filtered_item = {k: v for k, v in item.items() if k in [f.name for f in model._meta.fields]}
        
        print(filtered_item,"esta cargando o ni siq uiera entra")
        # Convertir valores de claves foráneas a instancias de modelos
        try:
            if model == NotaVentaParabrisa:
                filtered_item['nota_venta_id'] = NotaVenta.objects.get(id=filtered_item['nota_venta_id'])
                filtered_item['parabrisa_id'] = Parabrisas.objects.get(id=filtered_item['parabrisa_id'])
            elif model == NotaCompra:
                filtered_item['parabrisa_id'] = Parabrisas.objects.get(id=filtered_item['parabrisa_id'])
                filtered_item['proveedor_id'] = Proveedor.objects.get(id=filtered_item['proveedor_id'])
                filtered_item['almacen_id'] = Almacen.objects.get(id=filtered_item['almacen_id'])
            elif model == NotaVenta:
                filtered_item['cliente_id'] = Cliente.objects.get(id=filtered_item['cliente_id'])
                filtered_item['almacen_id'] = Almacen.objects.get(id=filtered_item['almacen_id'])
            elif model == AlmacenParabrisa:
                filtered_item['almacen_id'] = Almacen.objects.get(id=filtered_item['almacen_id'])
                filtered_item['parabrisa_id'] = Parabrisas.objects.get(id=filtered_item['parabrisa_id'])
            elif model == Parabrisas:
                pass  # No hay relaciones que resolver para Parabrisas
            elif model == Cliente:
                pass  # No hay relaciones que resolver para Cliente
            elif model == Proveedor:
                pass  # No hay relaciones que resolver para Proveedor
            elif model == Almacen:
                pass 
        except Exception as e:
            print(f'Error al guardar el item: {e}')
        
        record = model(**filtered_item)
        record.save()
        

def main(token):
    endpoints = {
        
        'todos-los-parabrisas': Parabrisas,
        'todos-los-clientes': Cliente,
        'todos-los-proveedores': Proveedor,
        'todos-los-almacenes': Almacen,
        'todas-las-ventas': NotaVenta,
        'todas-las-compras': NotaCompra,
        'almacenparabrisa': AlmacenParabrisa,
        'detalle-nota-venta': NotaVentaParabrisa
    }

    for endpoint, model in endpoints.items():
        data = get_data_from_api(endpoint, token)
        if data:
            save_data_to_db(data, model)

if __name__ == '__main__':
    email = 'tu-email@example.com'
    password = 'tu-contraseña'
    token = login(email, password)
    if token:
        main(token)
        logout(token)