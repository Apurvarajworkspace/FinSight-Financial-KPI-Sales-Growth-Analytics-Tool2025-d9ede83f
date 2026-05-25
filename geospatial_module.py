"""
Geospatial Analysis & Location Intelligence Module
Geographic analysis, location-based insights, and spatial analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import math


class GeoAnalyzer:
    """Perform geospatial analysis"""
    
    def __init__(self):
        self.locations = {}
        self.distance_matrix = {}
        self.location_clusters = {}
    
    def add_location(self, location_id, name, latitude, longitude, attributes=None):
        """Add location with coordinates"""
        self.locations[location_id] = {
            'id': location_id,
            'name': name,
            'latitude': latitude,
            'longitude': longitude,
            'attributes': attributes or {},
            'added_at': datetime.now().isoformat()
        }
        return {'status': 'added', 'location_id': location_id}
    
    def calculate_distance(self, loc_id_1, loc_id_2):
        """Calculate distance between two locations (Haversine formula)"""
        if loc_id_1 not in self.locations or loc_id_2 not in self.locations:
            return None
        
        loc1 = self.locations[loc_id_1]
        loc2 = self.locations[loc_id_2]
        
        lat1, lon1 = math.radians(loc1['latitude']), math.radians(loc1['longitude'])
        lat2, lon2 = math.radians(loc2['latitude']), math.radians(loc2['longitude'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Earth's radius in km
        
        return c * r
    
    def get_nearest_locations(self, location_id, radius_km=10):
        """Find nearest locations within radius"""
        if location_id not in self.locations:
            return []
        
        nearest = []
        for other_id, location in self.locations.items():
            if other_id != location_id:
                distance = self.calculate_distance(location_id, other_id)
                if distance and distance <= radius_km:
                    nearest.append({
                        'location_id': other_id,
                        'name': location['name'],
                        'distance_km': round(distance, 2)
                    })
        
        return sorted(nearest, key=lambda x: x['distance_km'])
    
    def cluster_locations(self, method='kmeans_simple', num_clusters=3):
        """Cluster locations by geographic proximity"""
        if len(self.locations) < num_clusters:
            return None
        
        # Simple clustering: assign to nearest centroid
        locations_list = list(self.locations.items())
        clusters = {i: [] for i in range(num_clusters)}
        
        # Assign to clusters
        for loc_id, loc in locations_list:
            cluster = hash(loc_id) % num_clusters
            clusters[cluster].append(loc_id)
        
        self.location_clusters = clusters
        return {
            'method': method,
            'num_clusters': num_clusters,
            'cluster_sizes': {i: len(c) for i, c in clusters.items()}
        }


class LocationIntelligence:
    """Extract insights from location data"""
    
    def __init__(self):
        self.location_statistics = {}
        self.demographic_data = {}
        self.traffic_patterns = {}
    
    def analyze_location_density(self, locations_dict):
        """Analyze concentration of locations"""
        if not locations_dict:
            return None
        
        lats = [loc['latitude'] for loc in locations_dict.values()]
        lons = [loc['longitude'] for loc in locations_dict.values()]
        
        density = {
            'center_latitude': np.mean(lats),
            'center_longitude': np.mean(lons),
            'lat_spread': max(lats) - min(lats),
            'lon_spread': max(lons) - min(lons),
            'location_count': len(locations_dict),
            'concentration_score': 100 - ((max(lats) - min(lats) + max(lons) - min(lons)) / 360 * 100)
        }
        return density
    
    def get_location_insights(self, location_id, locations_dict, transactions_by_location=None):
        """Get insights for specific location"""
        if location_id not in locations_dict:
            return None
        
        location = locations_dict[location_id]
        insights = {
            'location_id': location_id,
            'name': location['name'],
            'coordinates': {
                'latitude': location['latitude'],
                'longitude': location['longitude']
            },
            'region': self._determine_region(location['latitude'], location['longitude']),
            'nearby_locations': len([l for l in locations_dict.values() 
                                    if self._is_nearby(l, location)]),
            'population_segment': self._estimate_segment(location['latitude']),
            'growth_potential': self._estimate_growth(location['latitude'], location['longitude'])
        }
        
        if transactions_by_location and location_id in transactions_by_location:
            insights['transaction_volume'] = len(transactions_by_location[location_id])
        
        return insights
    
    def _determine_region(self, lat, lon):
        """Determine geographic region"""
        if lat > 30:
            if lon < 0:
                return 'North America'
            elif lon < 30:
                return 'Europe'
            else:
                return 'Asia'
        elif lat > 0:
            if lon < 0:
                return 'Central America'
            elif lon < 30:
                return 'Africa'
            else:
                return 'Southeast Asia'
        else:
            if lon < 0:
                return 'South America'
            elif lon < 30:
                return 'Southern Africa'
            else:
                return 'Oceania'
    
    def _is_nearby(self, loc1, loc2, threshold=10):
        """Check if two locations are nearby (simple heuristic)"""
        lat_diff = abs(loc1['latitude'] - loc2['latitude'])
        lon_diff = abs(loc1['longitude'] - loc2['longitude'])
        return (lat_diff + lon_diff) < threshold
    
    def _estimate_segment(self, latitude):
        """Estimate market segment based on latitude"""
        if latitude > 45:
            return 'Developed Northern'
        elif latitude > 30:
            return 'Developed Mid-Latitude'
        elif latitude > 0:
            return 'Emerging Tropical'
        else:
            return 'Emerging Southern'
    
    def _estimate_growth(self, lat, lon):
        """Estimate growth potential (simplified)"""
        score = (abs(lat) + abs(lon % 100)) / 100 * 50
        return min(score, 100)


class RouteOptimizer:
    """Optimize routes and logistics"""
    
    def __init__(self):
        self.routes = {}
        self.optimization_history = []
    
    def plan_route(self, start_location, end_location, waypoints, locations_dict):
        """Plan optimal route between locations"""
        route_id = f"route_{int(datetime.now().timestamp())}"
        
        # Simple route calculation
        total_distance = 0
        route_sequence = [start_location] + waypoints + [end_location]
        
        for i in range(len(route_sequence) - 1):
            if route_sequence[i] in locations_dict and route_sequence[i+1] in locations_dict:
                distance = self._calc_distance(
                    locations_dict[route_sequence[i]],
                    locations_dict[route_sequence[i+1]]
                )
                total_distance += distance
        
        self.routes[route_id] = {
            'route_id': route_id,
            'sequence': route_sequence,
            'total_distance_km': round(total_distance, 2),
            'created_at': datetime.now().isoformat(),
            'status': 'optimized'
        }
        return self.routes[route_id]
    
    def _calc_distance(self, loc1, loc2):
        """Calculate simple distance"""
        lat_diff = (loc1['latitude'] - loc2['latitude']) ** 2
        lon_diff = (loc1['longitude'] - loc2['longitude']) ** 2
        return math.sqrt(lat_diff + lon_diff) * 111  # Approximate km
    
    def get_route_efficiency(self, route_id):
        """Get route efficiency metrics"""
        if route_id not in self.routes:
            return None
        
        route = self.routes[route_id]
        return {
            'route_id': route_id,
            'total_distance_km': route['total_distance_km'],
            'waypoints': len(route['sequence']) - 2,
            'efficiency_score': min(100, 100 - (route['total_distance_km'] / 10))
        }


class HeatmapGenerator:
    """Generate activity heatmaps by location"""
    
    def __init__(self):
        self.heatmaps = {}
    
    def create_heatmap(self, heatmap_name, locations_with_intensity):
        """Create heatmap from location intensity data"""
        heatmap_id = f"heatmap_{int(datetime.now().timestamp())}"
        
        # Group intensities
        intensity_distribution = Counter(locations_with_intensity.values())
        
        self.heatmaps[heatmap_id] = {
            'heatmap_id': heatmap_id,
            'name': heatmap_name,
            'data_points': len(locations_with_intensity),
            'intensity_range': {
                'min': min(locations_with_intensity.values()),
                'max': max(locations_with_intensity.values()),
                'avg': np.mean(list(locations_with_intensity.values()))
            },
            'created_at': datetime.now().isoformat()
        }
        return self.heatmaps[heatmap_id]


def run_geospatial_demo():
    """Demo function for geospatial analysis"""
    print("\n" + "="*70)
    print("GEOSPATIAL ANALYSIS & LOCATION INTELLIGENCE DEMO")
    print("="*70)
    
    # Initialize geospatial systems
    geo = GeoAnalyzer()
    intelligence = LocationIntelligence()
    router = RouteOptimizer()
    heatmap = HeatmapGenerator()
    
    # 1. Location data
    print("\n[1] Location Data Management...")
    print("-" * 70)
    locations_data = {
        'LOC001': {'name': 'San Francisco HQ', 'lat': 37.7749, 'lon': -122.4194},
        'LOC002': {'name': 'New York Office', 'lat': 40.7128, 'lon': -74.0060},
        'LOC003': {'name': 'London Office', 'lat': 51.5074, 'lon': -0.1278},
        'LOC004': {'name': 'Tokyo Office', 'lat': 35.6762, 'lon': 139.6503},
        'LOC005': {'name': 'Sydney Office', 'lat': -33.8688, 'lon': 151.2093}
    }
    
    for loc_id, loc_data in locations_data.items():
        geo.add_location(loc_id, loc_data['name'], loc_data['lat'], loc_data['lon'])
    
    print(f"[DONE] Locations Added: {len(geo.locations)}")
    print("[DONE] Locations: SF HQ, NY, London, Tokyo, Sydney")
    
    # 2. Distance calculations
    print("\n[2] Distance & Proximity Analysis...")
    print("-" * 70)
    distance = geo.calculate_distance('LOC001', 'LOC002')
    print(f"[DONE] SF to NY Distance: {distance:.2f} km")
    
    nearest = geo.get_nearest_locations('LOC001', radius_km=20000)
    print(f"[DONE] Nearest Locations to SF: {len(nearest)}")
    
    # 3. Location clustering
    print("\n[3] Geographic Clustering...")
    print("-" * 70)
    geo.cluster_locations('kmeans_simple', 2)
    clusters = geo.location_clusters
    print(f"[DONE] Clusters Created: {len(clusters)}")
    for cluster_id, locs in clusters.items():
        print(f"[DONE] Cluster {cluster_id}: {len(locs)} locations")
    
    # 4. Location intelligence
    print("\n[4] Location Intelligence...")
    print("-" * 70)
    locations_dict = {k: v for k, v in geo.locations.items()}
    density = intelligence.analyze_location_density(locations_dict)
    print(f"[DONE] Concentration Score: {density['concentration_score']:.1f}")
    print(f"[DONE] Center: ({density['center_latitude']:.2f}, {density['center_longitude']:.2f})")
    
    insight = intelligence.get_location_insights('LOC001', locations_dict)
    print(f"[DONE] SF Region: {insight['region']}")
    print(f"[DONE] Growth Potential: {insight['growth_potential']:.1f}%")
    
    # 5. Route optimization
    print("\n[5] Route Optimization...")
    print("-" * 70)
    route = router.plan_route('LOC001', 'LOC005', ['LOC002', 'LOC003'], locations_dict)
    efficiency = router.get_route_efficiency(route['route_id'])
    print(f"[DONE] Route Distance: {efficiency['total_distance_km']:.2f} km")
    print(f"[DONE] Efficiency Score: {efficiency['efficiency_score']:.1f}")
    print(f"[DONE] Waypoints: {efficiency['waypoints']}")
    
    print("\n" + "="*70)
    print("[DONE] GEOSPATIAL ANALYSIS DEMO COMPLETED")
    print("="*70)
