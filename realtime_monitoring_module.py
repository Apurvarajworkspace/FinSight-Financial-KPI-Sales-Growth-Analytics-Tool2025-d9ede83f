"""
Real-time Monitoring & Alerting System
Provides continuous metric monitoring, anomaly detection, and threshold-based alerts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import json


class MetricsMonitor:
    """Real-time metric monitoring with historical tracking"""
    
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.metrics = {}
        self.history = {}
        self.timestamps = deque(maxlen=window_size)
        
    def record_metric(self, metric_name, value, threshold=None):
        """Record a metric value and check thresholds"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
            self.history[metric_name] = []
        
        timestamp = datetime.now()
        self.metrics[metric_name].append(value)
        self.history[metric_name].append({'value': value, 'timestamp': timestamp.isoformat()})
        self.timestamps.append(timestamp)
        
        return {
            'metric': metric_name,
            'value': value,
            'timestamp': timestamp.isoformat(),
            'is_anomaly': False
        }
    
    def get_metric_stats(self, metric_name):
        """Get real-time statistics for a metric"""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return None
        
        values = np.array(self.metrics[metric_name])
        return {
            'metric': metric_name,
            'current': values[-1],
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'count': len(values),
            'trend': 'up' if len(values) > 1 and values[-1] > values[-2] else 'down'
        }
    
    def get_all_metrics_snapshot(self):
        """Get current state of all metrics"""
        snapshot = {}
        for metric_name in self.metrics:
            snapshot[metric_name] = self.get_metric_stats(metric_name)
        return snapshot


class AlertingSystem:
    """Threshold and anomaly-based alerting"""
    
    def __init__(self):
        self.alerts = []
        self.alert_history = []
        self.thresholds = {}
        self.severity_levels = {'info': 1, 'warning': 2, 'critical': 3, 'emergency': 4}
    
    def set_threshold(self, metric_name, min_threshold=None, max_threshold=None):
        """Configure alert thresholds for a metric"""
        self.thresholds[metric_name] = {
            'min': min_threshold,
            'max': max_threshold,
            'last_alert': None
        }
        return {'status': 'configured', 'metric': metric_name, 'min': min_threshold, 'max': max_threshold}
    
    def check_alert(self, metric_name, value, severity='warning'):
        """Check if a metric value triggers an alert"""
        if metric_name not in self.thresholds:
            return None
        
        threshold = self.thresholds[metric_name]
        alert_triggered = False
        alert_type = None
        
        if threshold['min'] is not None and value < threshold['min']:
            alert_triggered = True
            alert_type = 'below_minimum'
        elif threshold['max'] is not None and value > threshold['max']:
            alert_triggered = True
            alert_type = 'above_maximum'
        
        if alert_triggered:
            alert = {
                'metric': metric_name,
                'value': value,
                'type': alert_type,
                'severity': severity,
                'timestamp': datetime.now().isoformat(),
                'threshold': threshold
            }
            self.alerts.append(alert)
            self.alert_history.append(alert)
            threshold['last_alert'] = datetime.now()
            return alert
        
        return None
    
    def get_active_alerts(self):
        """Get all currently active alerts"""
        return {
            'total_alerts': len(self.alerts),
            'alerts': self.alerts,
            'by_severity': self._group_by_severity()
        }
    
    def _group_by_severity(self):
        """Group alerts by severity level"""
        grouped = {'info': 0, 'warning': 0, 'critical': 0, 'emergency': 0}
        for alert in self.alerts:
            grouped[alert['severity']] += 1
        return grouped
    
    def acknowledge_alert(self, alert_index):
        """Mark an alert as acknowledged"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]['acknowledged'] = True
            return {'status': 'acknowledged', 'alert_index': alert_index}
        return None
    
    def clear_alerts(self):
        """Clear all active alerts"""
        count = len(self.alerts)
        self.alerts = []
        return {'status': 'cleared', 'alerts_cleared': count}


class PerformanceDashboard:
    """Dashboard for monitoring key performance indicators"""
    
    def __init__(self, monitor, alerting):
        self.monitor = monitor
        self.alerting = alerting
        self.kpi_definitions = {}
        self.dashboard_data = {}
    
    def define_kpi(self, kpi_name, formula, dependencies):
        """Define a KPI with calculation formula"""
        self.kpi_definitions[kpi_name] = {
            'formula': formula,
            'dependencies': dependencies,
            'created_at': datetime.now().isoformat()
        }
        return {'status': 'defined', 'kpi': kpi_name}
    
    def calculate_kpi(self, kpi_name):
        """Calculate a KPI based on current metrics"""
        if kpi_name not in self.kpi_definitions:
            return None
        
        kpi_def = self.kpi_definitions[kpi_name]
        try:
            values = {}
            for dep in kpi_def['dependencies']:
                stats = self.monitor.get_metric_stats(dep)
                if stats:
                    values[dep] = stats['current']
            
            # Execute formula with metric values
            result = eval(kpi_def['formula'], {"__builtins__": {}}, values)
            
            return {
                'kpi': kpi_name,
                'value': result,
                'timestamp': datetime.now().isoformat(),
                'status': 'ok'
            }
        except Exception as e:
            return {'kpi': kpi_name, 'error': str(e), 'status': 'error'}
    
    def get_dashboard_snapshot(self):
        """Get complete dashboard snapshot"""
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.monitor.get_all_metrics_snapshot(),
            'alerts': self.alerting.get_active_alerts(),
            'kpis': {kpi: self.calculate_kpi(kpi) for kpi in self.kpi_definitions}
        }


class HealthCheck:
    """System health monitoring and diagnostics"""
    
    def __init__(self):
        self.health_status = {}
        self.check_history = []
    
    def run_system_check(self, metrics_dict):
        """Run comprehensive system health check"""
        checks = {
            'data_quality': self._check_data_quality(metrics_dict),
            'performance': self._check_performance(metrics_dict),
            'integrity': self._check_integrity(metrics_dict)
        }
        
        overall_health = 'healthy' if all(c['status'] == 'ok' for c in checks.values()) else 'warning'
        
        check_result = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': overall_health,
            'checks': checks,
            'recommendations': self._generate_recommendations(checks)
        }
        
        self.check_history.append(check_result)
        return check_result
    
    def _check_data_quality(self, metrics_dict):
        """Check data quality metrics"""
        missing_count = sum(1 for v in metrics_dict.values() if v is None)
        data_quality_score = 100 - (missing_count / len(metrics_dict) * 100) if metrics_dict else 100
        return {
            'status': 'ok' if data_quality_score > 95 else 'warning',
            'score': data_quality_score,
            'missing_metrics': missing_count
        }
    
    def _check_performance(self, metrics_dict):
        """Check system performance"""
        response_times = [v for v in metrics_dict.values() if isinstance(v, (int, float))]
        avg_response = np.mean(response_times) if response_times else 0
        return {
            'status': 'ok' if avg_response < 1000 else 'warning',
            'avg_response_ms': float(avg_response),
            'metric_count': len(metrics_dict)
        }
    
    def _check_integrity(self, metrics_dict):
        """Check data integrity"""
        integrity_checks = []
        for metric, value in metrics_dict.items():
            if isinstance(value, (int, float)):
                if not np.isnan(value) and not np.isinf(value):
                    integrity_checks.append(True)
        
        integrity_score = (len(integrity_checks) / len(metrics_dict) * 100) if metrics_dict else 100
        return {
            'status': 'ok' if integrity_score > 98 else 'warning',
            'integrity_score': integrity_score
        }
    
    def _generate_recommendations(self, checks):
        """Generate recommendations based on health checks"""
        recommendations = []
        for check_name, check_data in checks.items():
            if check_data['status'] != 'ok':
                recommendations.append(f"Review {check_name}: {check_data}")
        return recommendations


def run_realtime_monitoring_demo():
    """Demo function for real-time monitoring capabilities"""
    print("\n" + "="*70)
    print("REAL-TIME MONITORING & ALERTING DEMO")
    print("="*70)
    
    # Initialize systems
    monitor = MetricsMonitor()
    alerting = AlertingSystem()
    dashboard = PerformanceDashboard(monitor, alerting)
    health = HealthCheck()
    
    # 1. Record metrics
    print("\n[1] Recording Real-Time Metrics...")
    print("-" * 70)
    for i in range(20):
        monitor.record_metric('revenue', np.random.normal(50000, 5000))
        monitor.record_metric('response_time', np.random.normal(150, 30))
        monitor.record_metric('cpu_usage', np.random.normal(45, 10))
    print("[DONE] Recorded 60 metric values")
    print(f"[DONE] Metrics tracked: revenue, response_time, cpu_usage")
    
    # 2. Set thresholds and alerts
    print("\n[2] Configuring Alert Thresholds...")
    print("-" * 70)
    alerting.set_threshold('revenue', min_threshold=30000, max_threshold=70000)
    alerting.set_threshold('response_time', min_threshold=0, max_threshold=300)
    alerting.set_threshold('cpu_usage', min_threshold=0, max_threshold=80)
    print("[DONE] Thresholds configured: 3 metrics")
    print("[DONE] Alert severity levels: info, warning, critical, emergency")
    
    # 3. Check for violations
    print("\n[3] Checking Alert Conditions...")
    print("-" * 70)
    alert_count = 0
    for metric_name in ['revenue', 'response_time', 'cpu_usage']:
        stats = monitor.get_metric_stats(metric_name)
        if stats:
            alert = alerting.check_alert(metric_name, stats['max'], severity='warning')
            if alert:
                alert_count += 1
    print(f"[DONE] Alerts triggered: {alert_count}")
    active = alerting.get_active_alerts()
    print(f"[DONE] Active alerts: {active['total_alerts']}")
    
    # 4. Dashboard snapshot
    print("\n[4] Dashboard Snapshot...")
    print("-" * 70)
    dashboard.define_kpi('revenue_efficiency', 'revenue / response_time', ['revenue', 'response_time'])
    snapshot = dashboard.get_dashboard_snapshot()
    print(f"[DONE] Metrics monitored: {len(snapshot['metrics'])}")
    print(f"[DONE] KPIs calculated: {len(snapshot['kpis'])}")
    print(f"[DONE] Active alerts: {snapshot['alerts']['total_alerts']}")
    
    # 5. Health check
    print("\n[5] System Health Check...")
    print("-" * 70)
    metrics_dict = {m: monitor.get_metric_stats(m)['current'] if monitor.get_metric_stats(m) else None 
                   for m in ['revenue', 'response_time', 'cpu_usage']}
    health_result = health.run_system_check(metrics_dict)
    print(f"[DONE] Overall Health: {health_result['overall_health'].upper()}")
    print(f"[DONE] Data Quality: {health_result['checks']['data_quality']['score']:.2f}%")
    print(f"[DONE] Performance Status: {health_result['checks']['performance']['status']}")
    
    print("\n" + "="*70)
    print("[DONE] REAL-TIME MONITORING DEMO COMPLETED")
    print("="*70)
