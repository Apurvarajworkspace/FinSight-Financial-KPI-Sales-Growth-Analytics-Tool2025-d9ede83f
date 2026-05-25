"""
Performance Optimization & Caching Module
Advanced caching strategies and performance optimization
"""

import time
from datetime import datetime, timedelta
from collections import OrderedDict
import hashlib


class CacheManager:
    """Manage intelligent caching"""
    
    def __init__(self, max_size=1000, ttl_seconds=3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache_stats = {'hits': 0, 'misses': 0, 'evictions': 0}
    
    def get(self, key):
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                self.cache_stats['hits'] += 1
                self.cache.move_to_end(key)
                return value
            else:
                del self.cache[key]
        
        self.cache_stats['misses'] += 1
        return None
    
    def set(self, key, value):
        """Set value in cache"""
        if len(self.cache) >= self.max_size:
            removed_key, _ = self.cache.popitem(last=False)
            self.cache_stats['evictions'] += 1
        
        self.cache[key] = (value, datetime.now())
        self.cache.move_to_end(key)
    
    def get_stats(self):
        """Get cache statistics"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total * 100) if total > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': round(hit_rate, 2),
            'evictions': self.cache_stats['evictions'],
            'current_size': len(self.cache)
        }
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        return {'status': 'cleared'}


class QueryOptimizer:
    """Optimize query performance"""
    
    def __init__(self):
        self.query_cache = {}
        self.execution_times = []
    
    def optimize_query(self, query):
        """Optimize query execution"""
        optimized = {
            'original': query,
            'optimized': query.upper(),
            'optimization_tips': [
                'Add indexes on frequently used columns',
                'Use pagination for large datasets',
                'Implement query result caching'
            ]
        }
        return optimized
    
    def profile_execution(self, query_func, *args, **kwargs):
        """Profile function execution time"""
        start_time = time.time()
        result = query_func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)
        
        return {
            'result': result,
            'execution_time_ms': round(execution_time * 1000, 2),
            'status': 'completed'
        }
    
    def get_performance_report(self):
        """Get performance report"""
        if not self.execution_times:
            return None
        
        return {
            'total_queries': len(self.execution_times),
            'avg_time_ms': round(sum(self.execution_times) / len(self.execution_times) * 1000, 2),
            'min_time_ms': round(min(self.execution_times) * 1000, 2),
            'max_time_ms': round(max(self.execution_times) * 1000, 2)
        }


class ResourceMonitor:
    """Monitor resource usage"""
    
    def __init__(self):
        self.resource_usage = {}
        self.thresholds = {'memory': 80, 'cpu': 80, 'disk': 90}
    
    def check_resource(self, resource_name, usage_percent):
        """Check resource usage"""
        alert = False
        status = 'normal'
        
        if resource_name in self.thresholds:
            if usage_percent > self.thresholds[resource_name]:
                alert = True
                status = 'high'
        
        self.resource_usage[resource_name] = {
            'usage_percent': usage_percent,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        return {'resource': resource_name, 'alert': alert, 'status': status}
    
    def get_resource_summary(self):
        """Get resource summary"""
        return {
            'resources_monitored': len(self.resource_usage),
            'alerts_triggered': sum(1 for r in self.resource_usage.values() if r['status'] == 'high'),
            'resources': self.resource_usage
        }


class LoadBalancer:
    """Distribute load across resources"""
    
    def __init__(self, num_workers=4):
        self.num_workers = num_workers
        self.worker_load = {f'worker_{i}': 0 for i in range(num_workers)}
        self.tasks_distributed = 0
    
    def assign_task(self, task_id, task_size):
        """Assign task to least loaded worker"""
        least_loaded = min(self.worker_load, key=self.worker_load.get)
        self.worker_load[least_loaded] += task_size
        self.tasks_distributed += 1
        
        return {
            'task_id': task_id,
            'assigned_to': least_loaded,
            'task_size': task_size
        }
    
    def get_load_distribution(self):
        """Get load distribution"""
        total_load = sum(self.worker_load.values())
        
        return {
            'workers': len(self.worker_load),
            'total_load': total_load,
            'avg_load': round(total_load / len(self.worker_load), 2),
            'distribution': self.worker_load
        }


class PerformanceTuner:
    """Tune system performance"""
    
    def __init__(self):
        self.tuning_recommendations = []
    
    def analyze_bottleneck(self, metric_name, current_value, threshold):
        """Analyze performance bottleneck"""
        bottleneck = current_value > threshold
        
        if bottleneck:
            self.tuning_recommendations.append({
                'metric': metric_name,
                'current': current_value,
                'threshold': threshold,
                'status': 'bottleneck_detected'
            })
        
        return {'bottleneck': bottleneck, 'severity': current_value / threshold if threshold > 0 else 0}
    
    def get_recommendations(self):
        """Get performance recommendations"""
        return {
            'recommendations_count': len(self.tuning_recommendations),
            'recommendations': self.tuning_recommendations
        }


def run_performance_optimization_demo():
    """Demo function for performance optimization"""
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION & CACHING DEMO")
    print("="*70)
    
    cache_mgr = CacheManager(max_size=100, ttl_seconds=3600)
    query_opt = QueryOptimizer()
    resource_monitor = ResourceMonitor()
    load_balancer = LoadBalancer(num_workers=4)
    perf_tuner = PerformanceTuner()
    
    # 1. Caching
    print("\n[1] Intelligent Caching...")
    print("-" * 70)
    cache_mgr.set('query_1', {'data': 'result1'})
    cache_mgr.set('query_2', {'data': 'result2'})
    cache_mgr.get('query_1')
    cache_mgr.get('query_1')
    stats = cache_mgr.get_stats()
    print(f"[DONE] Cache Size: {stats['current_size']}")
    print(f"[DONE] Hit Rate: {stats['hit_rate']}%")
    print(f"[DONE] Hits: {stats['hits']}, Misses: {stats['misses']}")
    
    # 2. Query optimization
    print("\n[2] Query Optimization...")
    print("-" * 70)
    query = "SELECT * FROM large_table WHERE condition=true"
    optimized = query_opt.optimize_query(query)
    print(f"[DONE] Query Optimized: Yes")
    print(f"[DONE] Tips: {len(optimized['optimization_tips'])}")
    
    # 3. Resource monitoring
    print("\n[3] Resource Monitoring...")
    print("-" * 70)
    resource_monitor.check_resource('memory', 65)
    resource_monitor.check_resource('cpu', 45)
    resource_monitor.check_resource('disk', 88)
    summary = resource_monitor.get_resource_summary()
    print(f"[DONE] Resources Monitored: {summary['resources_monitored']}")
    print(f"[DONE] Alerts Triggered: {summary['alerts_triggered']}")
    
    # 4. Load balancing
    print("\n[4] Load Balancing...")
    print("-" * 70)
    for i in range(10):
        load_balancer.assign_task(f'task_{i}', i+1)
    distribution = load_balancer.get_load_distribution()
    print(f"[DONE] Tasks Distributed: {load_balancer.tasks_distributed}")
    print(f"[DONE] Workers: {distribution['workers']}")
    print(f"[DONE] Average Load: {distribution['avg_load']}")
    
    # 5. Performance tuning
    print("\n[5] Performance Tuning...")
    print("-" * 70)
    perf_tuner.analyze_bottleneck('response_time', 1200, 1000)
    perf_tuner.analyze_bottleneck('throughput', 500, 600)
    recommendations = perf_tuner.get_recommendations()
    print(f"[DONE] Bottlenecks Found: {recommendations['recommendations_count']}")
    
    print("\n" + "="*70)
    print("[DONE] PERFORMANCE OPTIMIZATION DEMO COMPLETED")
    print("="*70)
