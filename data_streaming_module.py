"""
Data Streaming & Real-Time Processing Module
Handles streaming data from Kafka, Redis, and other sources
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import json


class StreamProcessor:
    """Real-time stream data processing"""
    
    def __init__(self, buffer_size=1000):
        self.buffer = deque(maxlen=buffer_size)
        self.stream_stats = {}
        self.processed_records = 0
        self.processing_errors = 0
    
    def process_stream_record(self, record):
        """Process incoming stream record"""
        try:
            # Validate and transform record
            if not isinstance(record, dict):
                self.processing_errors += 1
                return {'status': 'error', 'message': 'Invalid record format'}
            
            # Add timestamp if missing
            if 'timestamp' not in record:
                record['timestamp'] = datetime.now().isoformat()
            
            self.buffer.append(record)
            self.processed_records += 1
            
            return {
                'status': 'processed',
                'record_id': record.get('id'),
                'timestamp': record['timestamp']
            }
        except Exception as e:
            self.processing_errors += 1
            return {'status': 'error', 'message': str(e)}
    
    def get_stream_statistics(self):
        """Get real-time stream statistics"""
        return {
            'total_processed': self.processed_records,
            'errors': self.processing_errors,
            'buffer_size': len(self.buffer),
            'error_rate': (self.processing_errors / self.processed_records * 100) if self.processed_records else 0,
            'throughput': self.processed_records / (len(self.buffer) if self.buffer else 1)
        }
    
    def get_buffered_records(self):
        """Get all buffered records"""
        return list(self.buffer)


class KafkaConnector:
    """Kafka stream connector"""
    
    def __init__(self, brokers=None, topics=None):
        self.brokers = brokers or ['localhost:9092']
        self.topics = topics or []
        self.consumer_groups = {}
        self.messages_received = 0
        self.connection_status = 'disconnected'
    
    def connect(self):
        """Connect to Kafka brokers"""
        try:
            # Simulated connection
            self.connection_status = 'connected'
            return {'status': 'connected', 'brokers': self.brokers}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def subscribe_to_topic(self, topic, consumer_group):
        """Subscribe to Kafka topic"""
        if topic not in self.consumer_groups:
            self.consumer_groups[topic] = []
        
        self.consumer_groups[topic].append(consumer_group)
        return {'status': 'subscribed', 'topic': topic, 'consumer_group': consumer_group}
    
    def consume_messages(self, topic, num_messages=10):
        """Consume messages from topic"""
        if topic not in self.consumer_groups:
            return {'status': 'error', 'message': f'Not subscribed to {topic}'}
        
        # Simulated message consumption
        messages = []
        for i in range(num_messages):
            messages.append({
                'offset': i,
                'key': f'key_{i}',
                'value': f'message_{i}',
                'timestamp': datetime.now().isoformat()
            })
            self.messages_received += 1
        
        return {
            'topic': topic,
            'messages_count': len(messages),
            'messages': messages
        }
    
    def get_kafka_metrics(self):
        """Get Kafka connection metrics"""
        return {
            'connection_status': self.connection_status,
            'brokers': self.brokers,
            'topics_subscribed': len(self.consumer_groups),
            'total_messages_received': self.messages_received
        }


class RedisCache:
    """Redis caching for stream data"""
    
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.cache = {}
        self.access_count = {}
        self.connection_status = 'disconnected'
    
    def connect(self):
        """Connect to Redis"""
        self.connection_status = 'connected'
        return {'status': 'connected', 'host': self.host, 'port': self.port}
    
    def set_value(self, key, value, ttl=None):
        """Set cached value"""
        self.cache[key] = {
            'value': value,
            'created_at': datetime.now().isoformat(),
            'ttl': ttl,
            'expires_at': (datetime.now() + timedelta(seconds=ttl)).isoformat() if ttl else None
        }
        return {'status': 'set', 'key': key, 'ttl': ttl}
    
    def get_value(self, key):
        """Get cached value"""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return {'status': 'found', 'value': self.cache[key]['value']}
        return {'status': 'not_found', 'key': key}
    
    def delete_key(self, key):
        """Delete cached key"""
        if key in self.cache:
            del self.cache[key]
            return {'status': 'deleted', 'key': key}
        return {'status': 'not_found', 'key': key}
    
    def get_cache_statistics(self):
        """Get cache statistics"""
        total_accesses = sum(self.access_count.values())
        hits = len([k for k in self.access_count if self.access_count[k] > 0])
        return {
            'connection_status': self.connection_status,
            'cached_keys': len(self.cache),
            'total_accesses': total_accesses,
            'cache_hits': hits,
            'hit_rate': (hits / len(self.access_count) * 100) if self.access_count else 0
        }


class StreamAggregator:
    """Aggregate stream data by time windows"""
    
    def __init__(self, window_size_seconds=60):
        self.window_size = window_size_seconds
        self.windows = {}
        self.aggregated_data = []
    
    def add_to_window(self, record, metric_field='value'):
        """Add record to current time window"""
        window_key = int(datetime.now().timestamp() / self.window_size) * self.window_size
        
        if window_key not in self.windows:
            self.windows[window_key] = []
        
        self.windows[window_key].append(record)
        return {'status': 'added', 'window': window_key}
    
    def aggregate_window(self, window_key, aggregation='sum'):
        """Aggregate values in a time window"""
        if window_key not in self.windows:
            return None
        
        values = [r.get('value', 0) for r in self.windows[window_key] if isinstance(r.get('value'), (int, float))]
        
        if not values:
            return None
        
        if aggregation == 'sum':
            result = sum(values)
        elif aggregation == 'avg':
            result = np.mean(values)
        elif aggregation == 'max':
            result = max(values)
        elif aggregation == 'min':
            result = min(values)
        elif aggregation == 'count':
            result = len(values)
        else:
            result = None
        
        aggregated = {
            'window': window_key,
            'window_time': datetime.fromtimestamp(window_key).isoformat(),
            'aggregation': aggregation,
            'result': result,
            'record_count': len(self.windows[window_key])
        }
        self.aggregated_data.append(aggregated)
        return aggregated
    
    def get_aggregated_summary(self):
        """Get summary of aggregated data"""
        return {
            'total_windows': len(self.windows),
            'aggregated_results': len(self.aggregated_data),
            'window_size_seconds': self.window_size
        }


def run_data_streaming_demo():
    """Demo function for data streaming capabilities"""
    print("\n" + "="*70)
    print("DATA STREAMING & REAL-TIME PROCESSING DEMO")
    print("="*70)
    
    # Initialize streaming components
    processor = StreamProcessor()
    kafka = KafkaConnector(brokers=['localhost:9092'], topics=['transactions', 'events'])
    redis = RedisCache()
    aggregator = StreamAggregator(window_size_seconds=60)
    
    # 1. Stream processing
    print("\n[1] Stream Record Processing...")
    print("-" * 70)
    for i in range(20):
        record = {
            'id': f'rec_{i}',
            'value': np.random.normal(100, 20),
            'type': 'transaction'
        }
        processor.process_stream_record(record)
    
    stats = processor.get_stream_statistics()
    print(f"[DONE] Records Processed: {stats['total_processed']}")
    print(f"[DONE] Processing Errors: {stats['errors']}")
    print(f"[DONE] Buffer Size: {stats['buffer_size']}")
    
    # 2. Kafka connectivity
    print("\n[2] Kafka Stream Connection...")
    print("-" * 70)
    kafka.connect()
    kafka.subscribe_to_topic('transactions', 'analytics-group')
    messages = kafka.consume_messages('transactions', 10)
    print(f"[DONE] Connection Status: {kafka.get_kafka_metrics()['connection_status']}")
    print(f"[DONE] Topics Subscribed: {kafka.get_kafka_metrics()['topics_subscribed']}")
    print(f"[DONE] Messages Consumed: {messages['messages_count']}")
    
    # 3. Redis caching
    print("\n[3] Redis Caching Layer...")
    print("-" * 70)
    redis.connect()
    redis.set_value('user_123_metrics', {'revenue': 5000, 'transactions': 15}, ttl=3600)
    redis.set_value('trending_products', ['product_1', 'product_2'], ttl=300)
    cached = redis.get_value('user_123_metrics')
    cache_stats = redis.get_cache_statistics()
    print(f"[DONE] Cache Status: {cache_stats['connection_status']}")
    print(f"[DONE] Cached Keys: {cache_stats['cached_keys']}")
    print(f"[DONE] Cache Hit Rate: {cache_stats['hit_rate']:.1f}%")
    
    # 4. Stream aggregation
    print("\n[4] Stream Data Aggregation...")
    print("-" * 70)
    for i in range(30):
        aggregator.add_to_window({'value': np.random.normal(100, 15)})
    
    # Aggregate current window
    current_window = int(datetime.now().timestamp() / 60) * 60
    aggregator.aggregate_window(current_window, 'sum')
    aggregator.aggregate_window(current_window, 'avg')
    
    agg_summary = aggregator.get_aggregated_summary()
    print(f"[DONE] Total Windows: {agg_summary['total_windows']}")
    print(f"[DONE] Aggregated Results: {agg_summary['aggregated_results']}")
    print(f"[DONE] Window Size: {agg_summary['window_size_seconds']} seconds")
    
    # 5. Stream pipeline summary
    print("\n[5] Complete Stream Pipeline...")
    print("-" * 70)
    print(f"[DONE] Records in Pipeline: {stats['total_processed']}")
    print(f"[DONE] Kafka Messages: {kafka.get_kafka_metrics()['total_messages_received']}")
    print(f"[DONE] Cached Entries: {cache_stats['cached_keys']}")
    print(f"[DONE] Aggregated Batches: {agg_summary['aggregated_results']}")
    
    print("\n" + "="*70)
    print("[DONE] DATA STREAMING DEMO COMPLETED")
    print("="*70)
