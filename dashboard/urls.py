"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import home_view, login_view, logout_view, train_model_view, predict_view, load_data_view, train_sales_model_view, predict_sales_view
from myapp.dashboard import dashboard_view
from myapp.ventas import ventas_mensuales_data, ventas_por_almacen_data, compras_ultimo_mes_data, compras_por_proveedor_data, ocupacion_almacenes_data, clientes_mas_compran_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Ruta para la página de inicio
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('load-data/', load_data_view, name='load_data'),
    path('dashboard/', dashboard_view, name='dashboard'),
     path('ventas-mensuales-data/', ventas_mensuales_data, name='ventas_mensuales_data'),
    path('ventas-por-almacen-data/', ventas_por_almacen_data, name='ventas_por_almacen_data'),
    path('compras-ultimo-mes-data/', compras_ultimo_mes_data, name='compras_ultimo_mes_data'),
    path('compras-por-proveedor-data/', compras_por_proveedor_data, name='compras_por_proveedor_data'),
    path('ocupacion-almacenes-data/', ocupacion_almacenes_data, name='ocupacion_almacenes_data'),
    path('clientes-mas-compran-data/', clientes_mas_compran_data, name='clientes_mas_compran_data'),
    path('train-model/', train_model_view, name='train_model'),
    path('predict/', predict_view, name='predict'), 
    path('train-sales-model/', train_sales_model_view, name='train_sales_model'),
    path('predict-sales/', predict_sales_view, name='predict_sales'),
]  
