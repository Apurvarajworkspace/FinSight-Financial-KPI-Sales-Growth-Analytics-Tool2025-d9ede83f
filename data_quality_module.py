"""
Data Quality & Validation Module
Comprehensive data quality checks and validation rules
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter


class DataValidator:
    """Validate data quality"""
    
    def __init__(self):
        self.validation_rules = {}
        self.validation_results = {}
    
    def add_rule(self, rule_name, rule_func):
        """Add validation rule"""
        self.validation_rules[rule_name] = rule_func
        return {'status': 'added', 'rule': rule_name}
    
    def validate_data(self, data):
        """Validate data against rules"""
        results = {}
        errors = []
        
        for rule_name, rule_func in self.validation_rules.items():
            try:
                is_valid = rule_func(data)
                results[rule_name] = is_valid
                if not is_valid:
                    errors.append(f"Validation failed: {rule_name}")
            except Exception as e:
                errors.append(str(e))
        
        return {'rules_passed': sum(1 for v in results.values() if v), 'total_rules': len(results), 'errors': errors}
    
    def validate_schema(self, data_dict, schema):
        """Validate data schema"""
        issues = []
        
        for field, field_type in schema.items():
            if field not in data_dict:
                issues.append(f"Missing field: {field}")
            elif not isinstance(data_dict[field], field_type):
                issues.append(f"Type mismatch: {field} - expected {field_type.__name__}")
        
        return {'valid': len(issues) == 0, 'issues': issues}


class QualityMetrics:
    """Calculate data quality metrics"""
    
    def __init__(self):
        self.quality_scores = {}
    
    def calculate_completeness(self, data):
        """Calculate data completeness"""
        if not data:
            return 0
        
        total_fields = len(data)
        non_empty = sum(1 for v in data.values() if v is not None and v != '')
        
        return round((non_empty / total_fields * 100), 2) if total_fields > 0 else 0
    
    def calculate_accuracy(self, original, reference):
        """Calculate accuracy percentage"""
        matches = sum(1 for k in original if k in reference and original[k] == reference[k])
        total = len(original)
        return round((matches / total * 100), 2) if total > 0 else 0
    
    def calculate_consistency(self, data_list):
        """Calculate data consistency"""
        if not data_list:
            return 100
        
        counter = Counter(data_list)
        most_common_count = counter.most_common(1)[0][1]
        
        return round((most_common_count / len(data_list) * 100), 2)
    
    def calculate_uniqueness(self, data_list):
        """Calculate uniqueness percentage"""
        if not data_list:
            return 0
        
        unique_count = len(set(data_list))
        return round((unique_count / len(data_list) * 100), 2)


class AnomalyDetector:
    """Detect data anomalies"""
    
    def __init__(self):
        self.anomalies = {}
    
    def detect_outliers(self, values, threshold=2):
        """Detect outliers using standard deviation"""
        if len(values) < 3:
            return []
        
        mean = np.mean(values)
        std = np.std(values)
        outliers = []
        
        for i, val in enumerate(values):
            if abs(val - mean) > threshold * std:
                outliers.append({'index': i, 'value': val, 'deviation': abs(val - mean)})
        
        return outliers
    
    def detect_missing_values(self, data):
        """Detect missing values"""
        missing = {}
        
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None or value == '':
                    missing[key] = 'missing'
        elif isinstance(data, list):
            missing = sum(1 for x in data if x is None or x == '')
        
        return missing
    
    def detect_duplicates(self, data_list):
        """Detect duplicate records"""
        counter = Counter(data_list)
        duplicates = {item: count for item, count in counter.items() if count > 1}
        return duplicates


class DataCleaner:
    """Clean and preprocess data"""
    
    def __init__(self):
        self.cleaning_history = []
    
    def remove_nulls(self, data):
        """Remove null values"""
        if isinstance(data, dict):
            cleaned = {k: v for k, v in data.items() if v is not None}
        else:
            cleaned = [x for x in data if x is not None]
        
        self.cleaning_history.append({'action': 'remove_nulls', 'timestamp': datetime.now().isoformat()})
        return cleaned
    
    def normalize_values(self, data):
        """Normalize numeric values to 0-100 range"""
        if not data or len(data) == 0:
            return data
        
        values = list(data.values()) if isinstance(data, dict) else data
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        normalized = {k: round(((v - min_val) / range_val) * 100, 2) for k, v in data.items()} if isinstance(data, dict) else [round(((v - min_val) / range_val) * 100, 2) for v in data]
        
        return normalized
    
    def standardize_format(self, data):
        """Standardize data format"""
        standardized = {}
        
        if isinstance(data, dict):
            for key, value in data.items():
                standardized[key] = str(value).strip().lower()
        
        self.cleaning_history.append({'action': 'standardize_format', 'timestamp': datetime.now().isoformat()})
        return standardized


def run_data_quality_demo():
    """Demo function for data quality"""
    print("\n" + "="*70)
    print("DATA QUALITY & VALIDATION DEMO")
    print("="*70)
    
    validator = DataValidator()
    quality_metrics = QualityMetrics()
    anomaly_detector = AnomalyDetector()
    cleaner = DataCleaner()
    
    # 1. Validation rules
    print("\n[1] Setting Up Validation Rules...")
    print("-" * 70)
    validator.add_rule('non_empty', lambda d: len(d) > 0)
    validator.add_rule('has_revenue', lambda d: 'revenue' in d)
    validator.add_rule('positive_values', lambda d: all(v > 0 for v in d.values() if isinstance(v, (int, float))))
    print("[DONE] Validation Rules: 3")
    
    # 2. Quality metrics
    print("\n[2] Calculating Quality Metrics...")
    print("-" * 70)
    data = {'revenue': 100000, 'cost': 60000, 'profit': 40000}
    completeness = quality_metrics.calculate_completeness(data)
    print(f"[DONE] Completeness: {completeness}%")
    
    # 3. Anomaly detection
    print("\n[3] Anomaly Detection...")
    print("-" * 70)
    values = [100, 105, 102, 98, 500, 99, 101]
    outliers = anomaly_detector.detect_outliers(values)
    print(f"[DONE] Data Points: {len(values)}")
    print(f"[DONE] Outliers Detected: {len(outliers)}")
    
    # 4. Data cleaning
    print("\n[4] Data Cleaning...")
    print("-" * 70)
    dirty_data = {'name': 'JOHN DOE', 'status': 'ACTIVE', 'category': 'PREMIUM'}
    standardized = cleaner.standardize_format(dirty_data)
    print(f"[DONE] Records Standardized: {len(standardized)}")
    print(f"[DONE] Cleaning History: {len(cleaner.cleaning_history)}")
    
    # 5. Data validation
    print("\n[5] Running Validation...")
    print("-" * 70)
    validation_result = validator.validate_data(data)
    print(f"[DONE] Rules Checked: {validation_result['total_rules']}")
    print(f"[DONE] Rules Passed: {validation_result['rules_passed']}")
    
    print("\n" + "="*70)
    print("[DONE] DATA QUALITY DEMO COMPLETED")
    print("="*70)
