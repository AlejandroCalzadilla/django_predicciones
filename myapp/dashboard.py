# myapp/views.py
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from .models import NotaVenta, NotaCompra, Almacen

from django.shortcuts import render, redirect

def dashboard_view(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')
    
    return render(request, 'dashboard.html')