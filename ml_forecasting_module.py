"""
ML-Powered Time Series Forecasting Module
Advanced forecasting using multiple algorithms: ARIMA-like, Exponential Smoothing, Linear Regression
"""

import numpy as np
import pandas as pd
from scipy import signal
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class MLForecaster:
    """Advanced machine learning-based time series forecasting"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.forecasts = {}
    
    def arima_like_forecast(self, series, periods=12, order=(1, 1, 1)):
        """
        ARIMA-like forecasting using differencing and autoregression
        
        Args:
            series: Time series data
            periods: Number of periods to forecast
            order: (p, d, q) - autoregressive, differencing, moving average
        
        Returns:
            Forecast values
        """
        p, d, q = order
        data = np.array(series).flatten()
        
        # Apply differencing
        diff_data = data.copy()
        for _ in range(d):
            diff_data = np.diff(diff_data)
        
        # Autoregressive component
        if len(diff_data) > p:
            X = np.array([diff_data[i-p:i] for i in range(p, len(diff_data))])
            y = diff_data[p:]
            
            model = LinearRegression()
            model.fit(X, y)
            self.models['arima'] = model
            
            # Forecast
            forecast = []
            last_values = diff_data[-p:].tolist()
            
            for _ in range(periods):
                next_val = model.predict([last_values])[0]
                forecast.append(next_val)
                last_values = (last_values + [next_val])[-p:]
            
            # Reverse differencing
            forecast = np.array(forecast)
            last_original = data[-1]
            for _ in range(d):
                forecast = np.cumsum(np.concatenate([[last_original], forecast]))[1:]
                last_original = forecast[-1]
            
            return forecast
        
        return np.full(periods, np.mean(data))
    
    def exponential_smoothing_ml(self, series, periods=12, alpha=0.3, beta=0.2, gamma=0.1):
        """
        Advanced exponential smoothing with trend and seasonality
        
        Args:
            series: Time series data
            periods: Forecast periods
            alpha: Level smoothing parameter
            beta: Trend smoothing parameter
            gamma: Seasonality smoothing parameter
        
        Returns:
            Forecast values
        """
        data = np.array(series).flatten()
        n = len(data)
        seasonal_period = 12  # Assume 12-period seasonality
        
        # Initialize components
        level = data[0]
        trend = (data[seasonal_period] - data[0]) / seasonal_period if n > seasonal_period else 0
        seasonality = np.ones(seasonal_period)
        
        if n >= seasonal_period:
            for i in range(seasonal_period):
                seasonality[i] = data[i] / np.mean(data[:seasonal_period])
        
        # Smoothing
        smoothed_data = []
        for i in range(n):
            season_idx = i % seasonal_period
            
            if i > 0:
                prev_level = level
                level = alpha * (data[i] / seasonality[season_idx]) + (1 - alpha) * (prev_level + trend)
                trend = beta * (level - prev_level) + (1 - beta) * trend
                seasonality[season_idx] = gamma * (data[i] / level) + (1 - gamma) * seasonality[season_idx]
            
            smoothed_data.append(level * seasonality[season_idx])
        
        # Forecast
        forecast = []
        for i in range(periods):
            season_idx = (n + i) % seasonal_period
            forecast_val = (level + (i + 1) * trend) * seasonality[season_idx]
            forecast.append(forecast_val)
        
        return np.array(forecast)
    
    def ml_regression_forecast(self, series, periods=12, degree=2):
        """
        Polynomial regression forecasting
        
        Args:
            series: Time series data
            periods: Forecast periods
            degree: Polynomial degree
        
        Returns:
            Forecast values
        """
        data = np.array(series).flatten()
        X = np.arange(len(data)).reshape(-1, 1)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Add polynomial features
        X_poly = np.hstack([X_scaled ** i for i in range(1, degree + 1)])
        
        # Fit model
        model = LinearRegression()
        model.fit(X_poly, data)
        self.models['regression'] = (model, scaler, degree)
        
        # Forecast
        X_future = np.arange(len(data), len(data) + periods).reshape(-1, 1)
        X_future_scaled = scaler.transform(X_future)
        X_future_poly = np.hstack([X_future_scaled ** i for i in range(1, degree + 1)])
        
        forecast = model.predict(X_future_poly)
        return np.maximum(forecast, 0)  # Ensure non-negative
    
    def ensemble_forecast(self, series, periods=12):
        """
        Ensemble forecasting combining multiple algorithms
        
        Args:
            series: Time series data
            periods: Forecast periods
        
        Returns:
            Dictionary with individual and ensemble forecasts
        """
        arima_forecast = self.arima_like_forecast(series, periods)
        exp_smooth_forecast = self.exponential_smoothing_ml(series, periods)
        ml_forecast = self.ml_regression_forecast(series, periods)
        
        # Weighted ensemble (can adjust weights)
        ensemble = (arima_forecast * 0.3 + exp_smooth_forecast * 0.4 + ml_forecast * 0.3)
        
        return {
            'arima': arima_forecast,
            'exponential_smoothing': exp_smooth_forecast,
            'regression': ml_forecast,
            'ensemble': ensemble,
            'ensemble_mean': np.mean(ensemble),
            'ensemble_std': np.std(ensemble),
            'confidence_interval_95': (
                ensemble - 1.96 * np.std(ensemble),
                ensemble + 1.96 * np.std(ensemble)
            )
        }
    
    def forecast_accuracy_metrics(self, actual, predicted):
        """
        Calculate forecast accuracy metrics
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            Dictionary with accuracy metrics
        """
        actual = np.array(actual).flatten()
        predicted = np.array(predicted).flatten()
        
        # Ensure same length
        min_len = min(len(actual), len(predicted))
        actual = actual[:min_len]
        predicted = predicted[:min_len]
        
        # Calculate metrics
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        mape = np.mean(np.abs((actual - predicted) / (np.abs(actual) + 1e-8))) * 100
        
        # Direction accuracy (if trend is correct)
        actual_diff = np.diff(actual)
        pred_diff = np.diff(predicted)
        direction_accuracy = np.mean((actual_diff * pred_diff) > 0) * 100
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'Direction_Accuracy': direction_accuracy,
            'Mean_Actual': np.mean(actual),
            'Mean_Predicted': np.mean(predicted)
        }
    
    def multi_step_forecast(self, data_dict, periods=12):
        """
        Forecast multiple metrics simultaneously
        
        Args:
            data_dict: Dictionary of {metric_name: series}
            periods: Forecast periods
        
        Returns:
            Dictionary with forecasts for each metric
        """
        results = {}
        
        for metric_name, series in data_dict.items():
            if len(series) > 3:
                forecast = self.ensemble_forecast(series, periods)
                results[metric_name] = forecast
        
        return results


class TimeSeriesAnalyzer:
    """Advanced time series analysis"""
    
    @staticmethod
    def decompose_series(series, period=12):
        """
        Decompose time series into trend, seasonal, residual
        
        Args:
            series: Time series data
            period: Seasonal period
        
        Returns:
            Dictionary with components
        """
        data = np.array(series).flatten()
        n = len(data)
        
        if n < 2 * period:
            return {'trend': data, 'seasonal': np.zeros_like(data), 'residual': np.zeros_like(data)}
        
        # Moving average for trend
        trend = np.convolve(data, np.ones(period) / period, mode='same')
        
        # Detrended data
        detrended = data - trend
        
        # Seasonal component
        seasonal = np.zeros_like(data)
        for i in range(period):
            indices = np.arange(i, n, period)
            if len(indices) > 0:
                seasonal[indices] = np.mean(detrended[indices])
        
        # Residual
        residual = data - trend - seasonal
        
        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'trend_strength': 1 - (np.var(residual) / np.var(trend + residual + 1e-8)),
            'seasonal_strength': 1 - (np.var(residual) / np.var(seasonal + residual + 1e-8))
        }
    
    @staticmethod
    def stationarity_test(series):
        """
        Test if series is stationary using multiple methods
        
        Args:
            series: Time series data
        
        Returns:
            Stationarity assessment
        """
        data = np.array(series).flatten()
        
        # Mean and variance stability (rolling window)
        window = max(3, len(data) // 4)
        first_half_mean = np.mean(data[:len(data)//2])
        second_half_mean = np.mean(data[len(data)//2:])
        
        mean_stable = abs(first_half_mean - second_half_mean) / (first_half_mean + 1e-8) < 0.2
        
        first_half_var = np.var(data[:len(data)//2])
        second_half_var = np.var(data[len(data)//2:])
        
        var_stable = abs(first_half_var - second_half_var) / (first_half_var + 1e-8) < 0.2
        
        # ACF-based check
        autocorr = np.correlate(data - np.mean(data), data - np.mean(data), mode='full')[len(data)-1:len(data)+10]
        autocorr = autocorr / autocorr[0]
        high_autocorr = np.mean(np.abs(autocorr[1:5])) > 0.5
        
        return {
            'mean_stable': mean_stable,
            'variance_stable': var_stable,
            'likely_stationary': mean_stable and var_stable,
            'high_autocorrelation': high_autocorr,
            'recommendation': 'Differencing recommended' if not (mean_stable and var_stable) else 'Data is stationary'
        }
    
    @staticmethod
    def forecast_confidence_bands(forecast, residuals, confidence=0.95):
        """
        Calculate confidence bands for forecasts
        
        Args:
            forecast: Point forecast
            residuals: Model residuals
            confidence: Confidence level
        
        Returns:
            Lower and upper confidence bands
        """
        std_error = np.std(residuals)
        z_score = 1.96 if confidence == 0.95 else 2.576
        
        margin = z_score * std_error
        lower = forecast - margin
        upper = forecast + margin
        
        return lower, upper
