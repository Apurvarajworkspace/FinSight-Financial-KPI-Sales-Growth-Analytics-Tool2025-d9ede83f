"""
ML Model Management & Version Control Module
Manage ML models, versioning, deployment, and monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json


class ModelRegistry:
    """Central registry for ML models"""
    
    def __init__(self):
        self.models = {}
        self.model_versions = {}
        self.deployment_history = []
    
    def register_model(self, model_name, model_type, framework, description):
        """Register a new ML model"""
        model_id = f"{model_name}_{int(datetime.now().timestamp())}"
        self.models[model_id] = {
            'name': model_name,
            'type': model_type,  # classification, regression, clustering
            'framework': framework,  # sklearn, tensorflow, xgboost
            'description': description,
            'registered_at': datetime.now().isoformat(),
            'status': 'registered',
            'current_version': None
        }
        return {'status': 'registered', 'model_id': model_id}
    
    def create_model_version(self, model_id, version, parameters, metrics):
        """Create a version of a model"""
        if model_id not in self.models:
            return {'status': 'error', 'message': 'Model not found'}
        
        version_id = f"{model_id}_v{version}"
        self.model_versions[version_id] = {
            'model_id': model_id,
            'version': version,
            'parameters': parameters,
            'metrics': metrics,
            'created_at': datetime.now().isoformat(),
            'status': 'development'
        }
        
        self.models[model_id]['current_version'] = version_id
        return {'status': 'created', 'version_id': version_id}
    
    def get_model_history(self, model_id):
        """Get version history of a model"""
        versions = [v for v in self.model_versions.values() if v['model_id'] == model_id]
        return sorted(versions, key=lambda x: x['version'])
    
    def list_registered_models(self):
        """List all registered models"""
        return {
            'total_models': len(self.models),
            'models': list(self.models.keys())
        }


class ModelValidator:
    """Validate ML model performance"""
    
    def __init__(self):
        self.validation_results = []
        self.test_datasets = {}
    
    def register_test_dataset(self, dataset_id, name, size, split='train'):
        """Register a test dataset"""
        self.test_datasets[dataset_id] = {
            'name': name,
            'size': size,
            'split': split,
            'registered_at': datetime.now().isoformat()
        }
        return {'status': 'registered', 'dataset_id': dataset_id}
    
    def validate_model(self, model_id, dataset_id, metrics_dict):
        """Validate model on test dataset"""
        if model_id not in self.test_datasets and dataset_id not in self.test_datasets:
            return None
        
        validation = {
            'model_id': model_id,
            'dataset_id': dataset_id,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics_dict,
            'status': self._determine_validation_status(metrics_dict)
        }
        self.validation_results.append(validation)
        return validation
    
    def _determine_validation_status(self, metrics):
        """Determine validation status based on metrics"""
        if metrics.get('accuracy', 0) > 0.90:
            return 'passed'
        elif metrics.get('accuracy', 0) > 0.80:
            return 'warning'
        else:
            return 'failed'
    
    def get_validation_report(self):
        """Get validation summary"""
        if not self.validation_results:
            return {}
        
        passed = sum(1 for v in self.validation_results if v['status'] == 'passed')
        return {
            'total_validations': len(self.validation_results),
            'passed': passed,
            'pass_rate': (passed / len(self.validation_results) * 100),
            'datasets_used': len(self.test_datasets)
        }


class ModelDeployer:
    """Deploy and manage ML model deployments"""
    
    def __init__(self):
        self.deployments = {}
        self.deployment_log = []
        self.active_deployments = {}
    
    def deploy_model(self, model_id, environment, version=None):
        """Deploy a model to environment"""
        deployment_id = f"deploy_{model_id}_{int(datetime.now().timestamp())}"
        deployment = {
            'deployment_id': deployment_id,
            'model_id': model_id,
            'environment': environment,  # development, staging, production
            'version': version,
            'deployed_at': datetime.now().isoformat(),
            'status': 'active',
            'requests_served': 0,
            'errors': 0
        }
        
        self.deployments[deployment_id] = deployment
        self.active_deployments[environment] = deployment_id
        self.deployment_log.append(deployment)
        
        return {'status': 'deployed', 'deployment_id': deployment_id, 'environment': environment}
    
    def get_deployment_status(self, deployment_id):
        """Get status of a deployment"""
        if deployment_id not in self.deployments:
            return None
        
        deployment = self.deployments[deployment_id]
        return {
            'deployment_id': deployment_id,
            'status': deployment['status'],
            'environment': deployment['environment'],
            'deployed_at': deployment['deployed_at'],
            'requests_served': deployment['requests_served'],
            'error_rate': (deployment['errors'] / max(deployment['requests_served'], 1) * 100)
        }
    
    def record_prediction(self, deployment_id, success=True):
        """Record a model prediction/inference"""
        if deployment_id in self.deployments:
            self.deployments[deployment_id]['requests_served'] += 1
            if not success:
                self.deployments[deployment_id]['errors'] += 1
    
    def rollback_deployment(self, deployment_id, previous_version):
        """Rollback to previous model version"""
        if deployment_id not in self.deployments:
            return None
        
        deployment = self.deployments[deployment_id]
        old_version = deployment['version']
        deployment['version'] = previous_version
        
        rollback_record = {
            'timestamp': datetime.now().isoformat(),
            'deployment_id': deployment_id,
            'from_version': old_version,
            'to_version': previous_version,
            'reason': 'rollback'
        }
        self.deployment_log.append(rollback_record)
        
        return rollback_record
    
    def get_active_deployments(self):
        """Get all active deployments"""
        active = [d for d in self.deployments.values() if d['status'] == 'active']
        return {
            'total_active': len(active),
            'deployments': active
        }


class ModelMonitoring:
    """Monitor deployed models for data drift and performance degradation"""
    
    def __init__(self):
        self.performance_metrics = {}
        self.data_drift_alerts = []
        self.monitoring_data = []
    
    def record_model_metrics(self, model_id, timestamp, accuracy, latency, data_drift_score):
        """Record model performance metrics over time"""
        metric_record = {
            'model_id': model_id,
            'timestamp': timestamp,
            'accuracy': accuracy,
            'latency_ms': latency,
            'data_drift_score': data_drift_score
        }
        self.monitoring_data.append(metric_record)
        
        # Check for alerts
        if data_drift_score > 0.3:  # Threshold for data drift
            self._generate_data_drift_alert(model_id, data_drift_score)
        
        if accuracy < 0.85:  # Performance degradation
            self._generate_performance_alert(model_id, accuracy)
        
        return metric_record
    
    def _generate_data_drift_alert(self, model_id, drift_score):
        """Generate data drift alert"""
        alert = {
            'alert_type': 'data_drift',
            'model_id': model_id,
            'drift_score': drift_score,
            'timestamp': datetime.now().isoformat(),
            'severity': 'critical' if drift_score > 0.5 else 'warning'
        }
        self.data_drift_alerts.append(alert)
        return alert
    
    def _generate_performance_alert(self, model_id, accuracy):
        """Generate performance degradation alert"""
        alert = {
            'alert_type': 'performance_degradation',
            'model_id': model_id,
            'accuracy': accuracy,
            'timestamp': datetime.now().isoformat(),
            'severity': 'critical' if accuracy < 0.80 else 'warning'
        }
        self.data_drift_alerts.append(alert)
        return alert
    
    def get_monitoring_dashboard(self):
        """Get monitoring dashboard"""
        if not self.monitoring_data:
            return {}
        
        recent_data = self.monitoring_data[-10:]  # Last 10 records
        avg_accuracy = np.mean([d['accuracy'] for d in recent_data])
        avg_latency = np.mean([d['latency_ms'] for d in recent_data])
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(self.monitoring_data),
            'avg_accuracy': avg_accuracy,
            'avg_latency_ms': avg_latency,
            'active_alerts': len(self.data_drift_alerts),
            'data_drift_alerts': len([a for a in self.data_drift_alerts if a['alert_type'] == 'data_drift'])
        }


def run_ml_management_demo():
    """Demo function for ML model management"""
    print("\n" + "="*70)
    print("ML MODEL MANAGEMENT & VERSION CONTROL DEMO")
    print("="*70)
    
    # Initialize ML management systems
    registry = ModelRegistry()
    validator = ModelValidator()
    deployer = ModelDeployer()
    monitor = ModelMonitoring()
    
    # 1. Model registration
    print("\n[1] Model Registration...")
    print("-" * 70)
    model1 = registry.register_model('revenue_predictor', 'regression', 'sklearn', 'Predicts revenue')
    model2 = registry.register_model('churn_classifier', 'classification', 'xgboost', 'Predicts churn')
    models = registry.list_registered_models()
    print(f"[DONE] Models Registered: {models['total_models']}")
    
    # 2. Model versioning
    print("\n[2] Model Versioning...")
    print("-" * 70)
    model_id_1 = models['models'][0]
    registry.create_model_version(model_id_1, 1.0, {'max_depth': 5, 'learning_rate': 0.1}, 
                                 {'accuracy': 0.85, 'rmse': 1000})
    registry.create_model_version(model_id_1, 1.1, {'max_depth': 7, 'learning_rate': 0.05}, 
                                 {'accuracy': 0.88, 'rmse': 950})
    history = registry.get_model_history(model_id_1)
    print(f"[DONE] Versions Created: {len(history)}")
    print(f"[DONE] Current Version: {history[-1]['version']}")
    
    # 3. Model validation
    print("\n[3] Model Validation...")
    print("-" * 70)
    validator.register_test_dataset('test_2024', 'Q1 2024 Data', 5000, 'test')
    validator.validate_model(model_id_1, 'test_2024', {'accuracy': 0.89, 'precision': 0.91, 'recall': 0.87})
    validator.validate_model(model_id_1, 'test_2024', {'accuracy': 0.88, 'precision': 0.90, 'recall': 0.86})
    val_report = validator.get_validation_report()
    print(f"[DONE] Validations Run: {val_report['total_validations']}")
    print(f"[DONE] Pass Rate: {val_report['pass_rate']:.1f}%")
    
    # 4. Model deployment
    print("\n[4] Model Deployment...")
    print("-" * 70)
    deployer.deploy_model(model_id_1, 'development', '1.0')
    deployer.deploy_model(model_id_1, 'staging', '1.1')
    deployer.deploy_model(model_id_1, 'production', '1.0')
    active = deployer.get_active_deployments()
    print(f"[DONE] Active Deployments: {active['total_active']}")
    print(f"[DONE] Environments: development, staging, production")
    
    # 5. Model monitoring
    print("\n[5] Model Performance Monitoring...")
    print("-" * 70)
    for i in range(10):
        monitor.record_model_metrics(model_id_1, datetime.now().isoformat(),
                                    accuracy=np.random.normal(0.88, 0.02),
                                    latency=np.random.normal(50, 10),
                                    data_drift_score=np.random.normal(0.2, 0.05))
    
    dashboard = monitor.get_monitoring_dashboard()
    print(f"[DONE] Metrics Records: {dashboard['total_records']}")
    print(f"[DONE] Avg Accuracy: {dashboard['avg_accuracy']:.3f}")
    print(f"[DONE] Avg Latency: {dashboard['avg_latency_ms']:.1f}ms")
    print(f"[DONE] Active Alerts: {dashboard['active_alerts']}")
    
    print("\n" + "="*70)
    print("[DONE] ML MODEL MANAGEMENT DEMO COMPLETED")
    print("="*70)
