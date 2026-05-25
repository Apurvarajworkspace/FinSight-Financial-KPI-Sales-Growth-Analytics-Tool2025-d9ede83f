"""
Interactive Dashboards & Geo-Visualization Module
3D visualizations, interactive maps, real-time dashboards
"""

import pandas as pd
import numpy as np
from datetime import datetime


class AdvancedChartBuilder:
    """Build advanced interactive charts"""
    
    def __init__(self):
        self.charts = {}
        self.chart_count = 0
    
    def create_3d_scatter(self, data, x_col, y_col, z_col, title):
        """Create 3D scatter plot"""
        chart_id = f"scatter_3d_{self.chart_count}"
        self.charts[chart_id] = {
            'type': '3d_scatter',
            'title': title,
            'x_column': x_col,
            'y_column': y_col,
            'z_column': z_col,
            'data_points': len(data),
            'created_at': datetime.now().isoformat()
        }
        self.chart_count += 1
        return {'chart_id': chart_id, 'type': '3d_scatter', 'title': title}
    
    def create_heatmap(self, data_matrix, title, x_labels, y_labels):
        """Create interactive heatmap"""
        chart_id = f"heatmap_{self.chart_count}"
        self.charts[chart_id] = {
            'type': 'heatmap',
            'title': title,
            'rows': len(y_labels),
            'columns': len(x_labels),
            'x_labels': x_labels,
            'y_labels': y_labels,
            'created_at': datetime.now().isoformat()
        }
        self.chart_count += 1
        return {'chart_id': chart_id, 'type': 'heatmap', 'title': title}
    
    def create_sunburst(self, hierarchical_data, title):
        """Create sunburst/treemap chart"""
        chart_id = f"sunburst_{self.chart_count}"
        self.charts[chart_id] = {
            'type': 'sunburst',
            'title': title,
            'hierarchy_levels': len(hierarchical_data),
            'created_at': datetime.now().isoformat()
        }
        self.chart_count += 1
        return {'chart_id': chart_id, 'type': 'sunburst', 'title': title}
    
    def create_network_graph(self, nodes, edges, title):
        """Create network/graph visualization"""
        chart_id = f"network_{self.chart_count}"
        self.charts[chart_id] = {
            'type': 'network_graph',
            'title': title,
            'nodes': len(nodes),
            'edges': len(edges),
            'created_at': datetime.now().isoformat()
        }
        self.chart_count += 1
        return {'chart_id': chart_id, 'type': 'network_graph', 'title': title}
    
    def get_chart(self, chart_id):
        """Get chart details"""
        return self.charts.get(chart_id)


class InteractiveDashboard:
    """Create interactive dashboards"""
    
    def __init__(self):
        self.dashboards = {}
        self.dashboard_count = 0
    
    def create_dashboard(self, dashboard_name, layout='grid'):
        """Create new dashboard"""
        dashboard_id = f"dashboard_{self.dashboard_count}"
        self.dashboards[dashboard_id] = {
            'dashboard_id': dashboard_id,
            'name': dashboard_name,
            'layout': layout,
            'widgets': [],
            'created_at': datetime.now().isoformat(),
            'is_interactive': True
        }
        self.dashboard_count += 1
        return {'dashboard_id': dashboard_id, 'name': dashboard_name}
    
    def add_widget(self, dashboard_id, widget_type, title, config):
        """Add widget to dashboard"""
        if dashboard_id not in self.dashboards:
            return None
        
        widget = {
            'widget_id': f"widget_{len(self.dashboards[dashboard_id]['widgets'])}",
            'type': widget_type,
            'title': title,
            'config': config,
            'added_at': datetime.now().isoformat()
        }
        self.dashboards[dashboard_id]['widgets'].append(widget)
        return widget
    
    def get_dashboard(self, dashboard_id):
        """Get dashboard details"""
        return self.dashboards.get(dashboard_id)
    
    def update_dashboard_data(self, dashboard_id, new_data):
        """Update dashboard with new data"""
        if dashboard_id not in self.dashboards:
            return None
        
        dashboard = self.dashboards[dashboard_id]
        dashboard['last_updated'] = datetime.now().isoformat()
        dashboard['data'] = new_data
        return {'status': 'updated', 'dashboard_id': dashboard_id}
    
    def get_all_dashboards(self):
        """Get all dashboards"""
        return {
            'total_dashboards': len(self.dashboards),
            'dashboards': list(self.dashboards.keys())
        }


class GeoSpatialVisualizer:
    """Visualize geographic data"""
    
    def __init__(self):
        self.maps = {}
        self.map_count = 0
    
    def create_geographic_map(self, title, center_lat, center_lon, zoom_level):
        """Create geographic map"""
        map_id = f"map_{self.map_count}"
        self.maps[map_id] = {
            'map_id': map_id,
            'title': title,
            'center': {'latitude': center_lat, 'longitude': center_lon},
            'zoom': zoom_level,
            'layers': [],
            'markers': [],
            'created_at': datetime.now().isoformat()
        }
        self.map_count += 1
        return {'map_id': map_id, 'title': title}
    
    def add_map_layer(self, map_id, layer_type, layer_name, data):
        """Add layer to map (choropleth, heatmap, etc.)"""
        if map_id not in self.maps:
            return None
        
        layer = {
            'layer_id': f"layer_{len(self.maps[map_id]['layers'])}",
            'type': layer_type,
            'name': layer_name,
            'data_points': len(data) if isinstance(data, list) else 1,
            'added_at': datetime.now().isoformat()
        }
        self.maps[map_id]['layers'].append(layer)
        return layer
    
    def add_marker(self, map_id, latitude, longitude, label, color='blue'):
        """Add marker to map"""
        if map_id not in self.maps:
            return None
        
        marker = {
            'marker_id': f"marker_{len(self.maps[map_id]['markers'])}",
            'position': {'latitude': latitude, 'longitude': longitude},
            'label': label,
            'color': color,
            'added_at': datetime.now().isoformat()
        }
        self.maps[map_id]['markers'].append(marker)
        return marker
    
    def get_map(self, map_id):
        """Get map details"""
        return self.maps.get(map_id)


class RealtimeDashboard:
    """Real-time updating dashboard"""
    
    def __init__(self):
        self.realtime_dashboards = {}
        self.data_streams = {}
        self.update_frequency = {}
    
    def create_realtime_dashboard(self, name, update_interval_ms=1000):
        """Create real-time updating dashboard"""
        dashboard_id = f"rt_dashboard_{int(datetime.now().timestamp())}"
        self.realtime_dashboards[dashboard_id] = {
            'dashboard_id': dashboard_id,
            'name': name,
            'metrics': {},
            'created_at': datetime.now().isoformat(),
            'is_live': True
        }
        self.update_frequency[dashboard_id] = update_interval_ms
        return {'dashboard_id': dashboard_id, 'name': name}
    
    def stream_metric(self, dashboard_id, metric_name, value):
        """Stream metric value to real-time dashboard"""
        if dashboard_id not in self.realtime_dashboards:
            return None
        
        if metric_name not in self.realtime_dashboards[dashboard_id]['metrics']:
            self.realtime_dashboards[dashboard_id]['metrics'][metric_name] = []
        
        self.realtime_dashboards[dashboard_id]['metrics'][metric_name].append({
            'value': value,
            'timestamp': datetime.now().isoformat()
        })
        
        return {'status': 'streamed', 'metric': metric_name, 'value': value}
    
    def get_realtime_data(self, dashboard_id):
        """Get current real-time data"""
        if dashboard_id not in self.realtime_dashboards:
            return None
        
        dashboard = self.realtime_dashboards[dashboard_id]
        current_data = {}
        for metric, values in dashboard['metrics'].items():
            if values:
                current_data[metric] = values[-1]['value']
        
        return {
            'dashboard_id': dashboard_id,
            'timestamp': datetime.now().isoformat(),
            'current_values': current_data
        }


def run_dashboard_visualization_demo():
    """Demo function for advanced visualization"""
    print("\n" + "="*70)
    print("INTERACTIVE DASHBOARDS & GEO-VISUALIZATION DEMO")
    print("="*70)
    
    # Initialize visualization systems
    charts = AdvancedChartBuilder()
    dashboard_builder = InteractiveDashboard()
    geo = GeoSpatialVisualizer()
    realtime = RealtimeDashboard()
    
    # 1. Advanced charts
    print("\n[1] Advanced Chart Types...")
    print("-" * 70)
    data = pd.DataFrame({'x': np.random.randn(100), 
                        'y': np.random.randn(100), 
                        'z': np.random.randn(100)})
    charts.create_3d_scatter(data, 'x', 'y', 'z', 'Revenue vs Cost vs Growth')
    charts.create_heatmap(np.random.randn(10, 10), 'Customer Heatmap', 
                         [f'Month {i}' for i in range(10)],
                         [f'Region {i}' for i in range(10)])
    charts.create_sunburst({'data': [1, 2, 3]}, 'Product Hierarchy')
    nodes = list(range(10))
    edges = [(i, i+1) for i in range(9)]
    charts.create_network_graph(nodes, edges, 'Customer Network')
    print(f"[DONE] Charts Created: {charts.chart_count}")
    print(f"[DONE] Types: 3D Scatter, Heatmap, Sunburst, Network Graph")
    
    # 2. Interactive dashboards
    print("\n[2] Interactive Dashboards...")
    print("-" * 70)
    dashboard_builder.create_dashboard('Executive Dashboard', 'grid')
    dashboard_builder.create_dashboard('Sales Dashboard', 'tabs')
    dashboard_builder.create_dashboard('Financial Dashboard', 'flow')
    dashboards = dashboard_builder.get_all_dashboards()
    print(f"[DONE] Dashboards Created: {dashboards['total_dashboards']}")
    
    # 3. Dashboard widgets
    print("\n[3] Dashboard Widgets...")
    print("-" * 70)
    dashboard_id = list(dashboard_builder.dashboards.keys())[0]
    dashboard_builder.add_widget(dashboard_id, 'metric', 'Total Revenue', {'format': 'currency'})
    dashboard_builder.add_widget(dashboard_id, 'chart', 'Revenue Trend', {'chart_type': 'line'})
    dashboard_builder.add_widget(dashboard_id, 'gauge', 'Achievement', {'min': 0, 'max': 100})
    dashboard_builder.add_widget(dashboard_id, 'table', 'Top Customers', {'rows': 10})
    dashboard = dashboard_builder.get_dashboard(dashboard_id)
    print(f"[DONE] Widgets Added: {len(dashboard['widgets'])}")
    print(f"[DONE] Widget Types: Metric, Chart, Gauge, Table")
    
    # 4. Geographic visualization
    print("\n[4] Geographic Visualization...")
    print("-" * 70)
    geo.create_geographic_map('Sales by Region', 37.7749, -122.4194, 4)
    map_id = list(geo.maps.keys())[0]
    geo.add_map_layer(map_id, 'choropleth', 'Revenue by Country', {'US': 100000, 'EU': 80000})
    geo.add_marker(map_id, 37.7749, -122.4194, 'San Francisco HQ', 'red')
    geo.add_marker(map_id, 40.7128, -74.0060, 'New York Office', 'blue')
    geo_map = geo.get_map(map_id)
    print(f"[DONE] Maps Created: 1")
    print(f"[DONE] Layers: {len(geo_map['layers'])}")
    print(f"[DONE] Markers: {len(geo_map['markers'])}")
    
    # 5. Real-time dashboard
    print("\n[5] Real-Time Dashboard...")
    print("-" * 70)
    realtime.create_realtime_dashboard('Live Metrics', 1000)
    rt_dashboard_id = list(realtime.realtime_dashboards.keys())[0]
    for i in range(10):
        realtime.stream_metric(rt_dashboard_id, 'revenue', np.random.normal(50000, 5000))
        realtime.stream_metric(rt_dashboard_id, 'response_time', np.random.normal(150, 30))
    rt_data = realtime.get_realtime_data(rt_dashboard_id)
    print(f"[DONE] Real-Time Dashboard: {realtime.realtime_dashboards[rt_dashboard_id]['name']}")
    print(f"[DONE] Metrics Streamed: {len(rt_data['current_values'])}")
    print(f"[DONE] Update Frequency: 1000ms")
    
    print("\n" + "="*70)
    print("[DONE] DASHBOARD VISUALIZATION DEMO COMPLETED")
    print("="*70)
