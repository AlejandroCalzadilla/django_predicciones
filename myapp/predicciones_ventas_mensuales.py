from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import NotaVenta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np

def fetch_sales_data():
    ventas = NotaVenta.objects.annotate(
        mes_anio=TruncMonth('fecha')
    ).values(
        'mes_anio'
    ).annotate(
        total_ventas=Sum('monto_total')
    ).order_by('mes_anio')

    return pd.DataFrame(list(ventas))

def preprocess_data(df_ventas):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_ventas['total_ventas_scaled'] = scaler.fit_transform(df_ventas[['total_ventas']])

    n_steps = 12
    data = df_ventas['total_ventas_scaled'].values
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i + n_steps])
        y.append(data[i + n_steps])

    return scaler, pd.DataFrame(X), pd.Series(y)

def train_sales_model(X, y, model_path='modelo_ventas_mensuales.h5'):
    """
    Entrena un modelo LSTM con los datos proporcionados y guarda el modelo.
    """
    X_train, y_train = X.values, y.values

    # Remodelar para la entrada de LSTM
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    # Crear el modelo
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entrenar
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Guardar el modelo
    model.save(model_path)

    return model

def predict_future_sales(model, last_sequence, scaler, n_predictions=12):
    """
    Predice las ventas futuras basándose en el modelo entrenado.
    """
    predictions = []
    current_sequence = last_sequence
    for _ in range(n_predictions):
        prediction = model.predict(current_sequence)
        predictions.append(prediction[0, 0])
        current_sequence = np.append(current_sequence[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()

def save_model(model, path):
    model.save(path)

def load_model(path):
    return load_model(path)