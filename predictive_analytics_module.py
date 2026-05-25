"""
Predictive Analytics Module - Advanced Machine Learning Models
Includes classification, regression, and neural network-like predictions
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


class PredictiveModels:
    """Multiple ML models for business prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.logistic = LogisticRegression(random_state=42)
        self.gb_regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def predict_customer_lifetime_value(self, df, features_cols, target_col):
        """Predict CLV using gradient boosting regression"""
        try:
            X = df[features_cols].fillna(df[features_cols].mean())
            y = df[target_col].fillna(df[target_col].mean())
            
            X_scaled = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            self.gb_regressor.fit(X_train, y_train)
            y_pred = self.gb_regressor.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            feature_importance = pd.DataFrame({
                'feature': features_cols,
                'importance': self.gb_regressor.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return {
                'model': self.gb_regressor,
                'predictions': y_pred,
                'actual': y_test,
                'rmse': rmse,
                'mae': mae,
                'r2_score': r2,
                'feature_importance': feature_importance,
                'model_type': 'Gradient Boosting Regressor'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_churn_risk(self, df, features_cols, target_col):
        """Predict customer churn using random forest"""
        try:
            X = df[features_cols].fillna(df[features_cols].mean())
            y = df[target_col]
            
            X_scaled = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            self.rf_classifier.fit(X_train, y_train)
            y_pred = self.rf_classifier.predict(X_test)
            y_pred_proba = self.rf_classifier.predict_proba(X_test)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            try:
                auc = roc_auc_score(y_test, y_pred_proba)
            except:
                auc = 0.0
            
            feature_importance = pd.DataFrame({
                'feature': features_cols,
                'importance': self.rf_classifier.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return {
                'model': self.rf_classifier,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'actual': y_test,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'auc_score': auc,
                'feature_importance': feature_importance,
                'model_type': 'Random Forest Classifier'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_revenue(self, df, features_cols, target_col):
        """Predict revenue using ensemble methods"""
        try:
            X = df[features_cols].fillna(df[features_cols].mean())
            y = df[target_col].fillna(df[target_col].mean())
            
            X_scaled = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            # Train both models
            self.gb_regressor.fit(X_train, y_train)
            self.rf_regressor.fit(X_train, y_train)
            
            # Get predictions
            gb_pred = self.gb_regressor.predict(X_test)
            rf_pred = self.rf_regressor.predict(X_test)
            
            # Ensemble average
            ensemble_pred = (gb_pred + rf_pred) / 2
            
            gb_r2 = r2_score(y_test, gb_pred)
            rf_r2 = r2_score(y_test, rf_pred)
            ensemble_r2 = r2_score(y_test, ensemble_pred)
            
            gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
            rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
            ensemble_rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
            
            return {
                'gb_predictions': gb_pred,
                'rf_predictions': rf_pred,
                'ensemble_predictions': ensemble_pred,
                'actual': y_test,
                'gb_r2': gb_r2,
                'rf_r2': rf_r2,
                'ensemble_r2': ensemble_r2,
                'gb_rmse': gb_rmse,
                'rf_rmse': rf_rmse,
                'ensemble_rmse': ensemble_rmse,
                'ensemble_avg_prediction': ensemble_pred.mean(),
                'model_type': 'Ensemble (Gradient Boosting + Random Forest)'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def feature_importance_analysis(self, df, features_cols, target_col):
        """Analyze which features matter most"""
        try:
            X = df[features_cols].fillna(df[features_cols].mean())
            y = df[target_col].fillna(df[target_col].mean())
            
            X_scaled = self.scaler.fit_transform(X)
            self.rf_regressor.fit(X_scaled, y)
            
            importance_df = pd.DataFrame({
                'feature': features_cols,
                'importance': self.rf_regressor.feature_importances_,
                'importance_pct': (self.rf_regressor.feature_importances_ / self.rf_regressor.feature_importances_.sum() * 100).round(2)
            }).sort_values('importance', ascending=False)
            
            return {
                'feature_importance': importance_df,
                'top_3_features': importance_df.head(3)['feature'].tolist(),
                'top_3_importance': importance_df.head(3)['importance_pct'].tolist()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_product_demand(self, df, features_cols, target_col):
        """Predict product/service demand"""
        try:
            X = df[features_cols].fillna(df[features_cols].mean())
            y = df[target_col].fillna(df[target_col].mean())
            
            X_scaled = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            self.gb_regressor.fit(X_train, y_train)
            y_pred = self.gb_regressor.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
            
            # Demand categories
            demand_high = (y_pred > np.percentile(y_pred, 66)).sum()
            demand_medium = ((y_pred > np.percentile(y_pred, 33)) & (y_pred <= np.percentile(y_pred, 66))).sum()
            demand_low = (y_pred <= np.percentile(y_pred, 33)).sum()
            
            return {
                'predictions': y_pred,
                'actual': y_test,
                'mae': mae,
                'mape': mape,
                'high_demand_count': demand_high,
                'medium_demand_count': demand_medium,
                'low_demand_count': demand_low,
                'avg_prediction': y_pred.mean(),
                'std_prediction': y_pred.std()
            }
        except Exception as e:
            return {'error': str(e)}


class TimeSeriesPrediction:
    """Advanced time series prediction methods"""
    
    def __init__(self):
        self.model = None
    
    def arima_extended(self, series, p=2, d=1, q=2, periods=12):
        """Extended ARIMA-like forecasting"""
        try:
            series = series.values if isinstance(series, pd.Series) else series
            n = len(series)
            
            # Differencing
            if d > 0:
                diff_series = np.diff(series, n=d)
            else:
                diff_series = series
            
            # AR component (p terms)
            ar_component = np.array([np.mean(diff_series[-p:]) if len(diff_series) >= p else np.mean(diff_series)])
            
            # MA component (q terms)
            ma_component = np.array([np.std(diff_series[-q:]) if len(diff_series) >= q else np.std(diff_series)])
            
            # Forecast
            forecast = []
            for _ in range(periods):
                next_val = ar_component[0] + ma_component[0] * np.random.normal(0, 1)
                forecast.append(series[-1] + next_val if len(series) > 0 else next_val)
                series = np.append(series, forecast[-1])
            
            return {
                'forecast': np.array(forecast),
                'forecast_mean': np.mean(forecast),
                'forecast_std': np.std(forecast),
                'forecast_min': np.min(forecast),
                'forecast_max': np.max(forecast)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def prophet_like_forecast(self, series, periods=12, seasonality_mode='additive'):
        """Prophet-like forecasting with seasonality"""
        try:
            series = series.values if isinstance(series, pd.Series) else series
            n = len(series)
            
            # Trend component (linear)
            x = np.arange(n)
            coeffs = np.polyfit(x, series, 2)
            trend = np.polyval(coeffs, x)
            
            # Detrended series
            detrended = series - trend
            
            # Seasonal component (periodicity)
            if len(series) >= 12:
                seasonal_period = 12
                seasonal = np.array([detrended[i::seasonal_period].mean() for i in range(seasonal_period)])
            else:
                seasonal = np.zeros(len(series))
            
            # Forecast
            forecast = []
            for i in range(periods):
                trend_val = np.polyval(coeffs, n + i)
                seasonal_val = seasonal[(n + i) % len(seasonal)] if len(seasonal) > 0 else 0
                
                if seasonality_mode == 'additive':
                    pred = trend_val + seasonal_val
                else:  # multiplicative
                    pred = trend_val * (1 + seasonal_val / 100) if trend_val != 0 else seasonal_val
                
                forecast.append(max(0, pred))
            
            return {
                'forecast': np.array(forecast),
                'trend': trend.tolist(),
                'seasonal': seasonal.tolist(),
                'forecast_mean': np.mean(forecast),
                'forecast_trend': 'increasing' if coeffs[0] > 0 else 'decreasing'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def forecast_confidence_intervals(self, series, periods=12, confidence=0.95):
        """Generate confidence intervals for forecasts"""
        try:
            series = series.values if isinstance(series, pd.Series) else series
            
            # Calculate residuals from mean
            mean_val = np.mean(series)
            residuals = series - mean_val
            std_residuals = np.std(residuals)
            
            # Simple trend forecast
            trend_forecast = np.linspace(mean_val, mean_val + std_residuals, periods)
            
            # Calculate z-score for confidence level
            from scipy import stats
            z_score = stats.norm.ppf((1 + confidence) / 2)
            
            # Margin of error increases with forecast horizon
            margins = np.linspace(std_residuals * z_score, std_residuals * z_score * 1.5, periods)
            
            upper_bound = trend_forecast + margins
            lower_bound = trend_forecast - margins
            
            return {
                'forecast': trend_forecast,
                'upper_bound': upper_bound,
                'lower_bound': lower_bound,
                'margins': margins,
                'confidence_level': confidence,
                'forecast_range': (lower_bound[0], upper_bound[-1])
            }
        except Exception as e:
            return {'error': str(e)}


class AnomalyPrediction:
    """Predict future anomalies"""
    
    def predict_anomalies(self, series, window=20, sensitivity=2.0):
        """Predict where anomalies might occur"""
        try:
            series = series.values if isinstance(series, pd.Series) else series
            
            anomalies = []
            for i in range(window, len(series)):
                window_data = series[i-window:i]
                mean_val = np.mean(window_data)
                std_val = np.std(window_data)
                
                z_score = abs((series[i] - mean_val) / (std_val + 1e-10))
                
                if z_score > sensitivity:
                    anomalies.append({
                        'index': i,
                        'value': series[i],
                        'z_score': z_score,
                        'severity': 'high' if z_score > sensitivity * 1.5 else 'medium'
                    })
            
            return {
                'anomalies': anomalies,
                'anomaly_count': len(anomalies),
                'anomaly_rate': len(anomalies) / len(series) * 100,
                'high_severity': len([a for a in anomalies if a['severity'] == 'high']),
                'predicted_next_anomaly_index': anomalies[-1]['index'] + window if anomalies else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def anomaly_impact_assessment(self, series, anomaly_indices):
        """Assess impact of anomalies"""
        try:
            series = series.values if isinstance(series, pd.Series) else series
            
            if not anomaly_indices:
                return {'impact': 0, 'severity': 'none'}
            
            normal_mean = np.mean([series[i] for i in range(len(series)) if i not in anomaly_indices])
            anomaly_values = [series[i] for i in anomaly_indices]
            
            impact = np.mean(np.abs(np.array(anomaly_values) - normal_mean)) / (normal_mean + 1e-10) * 100
            
            return {
                'total_impact_%': round(impact, 2),
                'anomaly_count': len(anomaly_indices),
                'normal_mean': normal_mean,
                'anomaly_mean': np.mean(anomaly_values),
                'deviation': np.mean(anomaly_values) - normal_mean,
                'severity_level': 'critical' if impact > 50 else 'high' if impact > 20 else 'medium'
            }
        except Exception as e:
            return {'error': str(e)}
