from django.db.models import Sum
from django.db.models.functions import TruncMonth
import pandas as pd
from .models import NotaVentaParabrisa
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense


def fetch_sales_data():
    parabrisas_mas_vendidos = NotaVentaParabrisa.objects.values(
        'parabrisa_id'
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:10]

    parabrisas_ids = [item['parabrisa_id'] for item in parabrisas_mas_vendidos]

    ventas = NotaVentaParabrisa.objects.filter(
        parabrisa_id__in=parabrisas_ids
    ).annotate(
        mes_anio=TruncMonth('nota_venta_id__fecha')
    ).values(
        'parabrisa_id', 'mes_anio'
    ).annotate(
        cantidad_vendida=Sum('cantidad')
    ).order_by('parabrisa_id', 'mes_anio')

    return pd.DataFrame(list(ventas))

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def scale_data(self, data):
        return self.scaler.fit_transform(data)

    def create_sequences(self, data, n_steps):
        X, y = [], []
        for i in range(len(data) - n_steps):
            X.append(data[i:i + n_steps])
            y.append(data[i + n_steps])
        return np.array(X), np.array(y)

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data)

class SalesPredictor:
    def __init__(self, n_steps=12):
        self.model = Sequential()
        self.n_steps = n_steps

    def build_model(self, input_shape):
        self.model.add(LSTM(50, activation='relu', input_shape=input_shape))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, X_train, y_train, X_test, y_test, epochs=50, batch_size=32):
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size)

    def predict_future(self, last_sequence, n_predictions):
        predictions = []
        current_sequence = last_sequence
        for _ in range(n_predictions):
            prediction = self.model.predict(current_sequence[np.newaxis, :, :])
            predictions.append(prediction[0, 0])
            current_sequence = np.append(current_sequence[1:], prediction, axis=0)
        return predictions

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = load_model(path)
