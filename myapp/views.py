from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .api_client import login, logout, main
from .predicciones_parabrisas import fetch_sales_data as fetch_parabrisas_sales_data, DataPreprocessor, SalesPredictor
from .predicciones_ventas_mensuales import fetch_sales_data as fetch_ventas_sales_data, preprocess_data, train_sales_model, predict_future_sales, save_model, load_model
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from .models import Parabrisas
import os
import numpy as np

def home_view(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        response = login(email, password)
        
        if response:
            token = response.get('access_token')
            user = response.get('user')
            if token and user:
                request.session['token'] = token
                request.session['user_name'] = user['name']
                request.session['profile_photo_url'] = user['profile_photo_url']
                return redirect('dashboard')
            else:
                return HttpResponse('Error en el login')
    return render(request, 'login.html')

def logout_view(request):
    token = request.session.get('token')
    if token:
        logout(token)
        request.session.flush()
    return redirect('login')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def train_model_view(request):
    df_ventas = fetch_parabrisas_sales_data()
    productos_unicos = df_ventas['parabrisa_id'].unique()
    preprocessor = DataPreprocessor()

    for producto_id in productos_unicos:
        df_producto = df_ventas[df_ventas['parabrisa_id'] == producto_id]

        if len(df_producto) >= 12:
            ventas_scaled = preprocessor.scale_data(df_producto[['cantidad_vendida']])
            X, y = preprocessor.create_sequences(ventas_scaled, n_steps=12)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            predictor = SalesPredictor()
            predictor.build_model(input_shape=(X_train.shape[1], 1))
            predictor.train_model(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
            predictor.save_model(f'modelo_parabrisa_{producto_id}.h5')

    return JsonResponse({'status': 'Model trained successfully'})

def predict_view(request):
    df_ventas = fetch_parabrisas_sales_data()
    productos_unicos = df_ventas['parabrisa_id'].unique()
    preprocessor = DataPreprocessor()
    df_predicciones_totales = pd.DataFrame()

    posiciones = {
        1: "parabrisas delantero",
        2: "parabrisas trasero",
        3: "derecho delantero",
        4: "derecho trasero",
        5: "izquierdo delantero",
        6: "izquierdo trasero"
    }

    for producto_id in productos_unicos:
        df_producto = df_ventas[df_ventas['parabrisa_id'] == producto_id]

        if len(df_producto) >= 12:
            ventas_scaled = preprocessor.scale_data(df_producto[['cantidad_vendida']])
            last_sequence = ventas_scaled[-12:]

            predictor = SalesPredictor()
            model_path = f'modelo_parabrisa_{producto_id}.h5'
            if os.path.exists(model_path):
                predictor.load_model(model_path)
                predicciones_scaled = predictor.predict_future(last_sequence, n_predictions=12)
                predicciones = preprocessor.inverse_transform(np.array(predicciones_scaled).reshape(-1, 1))

                meses_prediccion = pd.date_range(start=pd.to_datetime(df_producto['mes_anio'].max()) + pd.DateOffset(months=1), periods=12, freq='M').strftime('%Y-%m')
                
                # Obtener la información de la posición y el vehiculo_id
                parabrisas = Parabrisas.objects.get(id=producto_id)
                posicion_nombre = posiciones.get(parabrisas.posicion_id, "parabrisas delantero")
                descripcion_producto = f"{posicion_nombre} {parabrisas.vehiculo_id}"
                
                # Redondear las predicciones a 2 decimales
                predicciones_redondeadas = np.round(predicciones.flatten(), 2)
                
                df_predicciones = pd.DataFrame({'mes': meses_prediccion, 'descripcion_producto': descripcion_producto, 'ventas_predichas': predicciones_redondeadas})
                df_predicciones_totales = pd.concat([df_predicciones_totales, df_predicciones])

    return JsonResponse(df_predicciones_totales.to_dict(orient='records'), safe=False)



def train_sales_model_view(request):
    df_ventas = fetch_ventas_sales_data()
    scaler, X, y = preprocess_data(df_ventas)
    model = train_sales_model(X, y)
    save_model(model, 'modelo_ventas_mensuales.h5')
    return JsonResponse({'status': 'Sales model trained successfully'})

def predict_sales_view(request):
    df_ventas = fetch_ventas_sales_data()
    scaler, X, y = preprocess_data(df_ventas)
    model = load_model('modelo_ventas_mensuales.h5')
    last_sequence = X.iloc[-1].values.reshape((1, -1, 1))
    predicciones = predict_future_sales(model, last_sequence, scaler, n_predictions=12)
    meses_prediccion = pd.date_range(start=pd.to_datetime(df_ventas['mes_anio'].max()) + pd.DateOffset(months=1), periods=12, freq='M').strftime('%Y-%m')
    df_predicciones = pd.DataFrame({'mes': meses_prediccion, 'ventas_predichas': predicciones})
    return JsonResponse(df_predicciones.to_dict(orient='records'), safe=False)


    
def load_data_view(request):
    token = request.session.get('token')
    if token:
        main(token)
        return JsonResponse({'status': 'Data loaded successfully'})
    else:
        return JsonResponse({'error': 'No token found'}, status=400)