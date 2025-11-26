"""
Areas Configuration - Define available AOIs and their metadata
"""

AREAS = {
    "new_york": {
        "name": "New York City",
        "center_lat": 40.7128,
        "center_lon": -74.0060,
        "zoom_level": 12,
        "tile_coverage_km": 10,  # Approximate coverage per tile
        "description": "Manhattan and surrounding areas",
        "priority_locations": [
            {"name": "Times Square", "lat": 40.7580, "lon": -73.9855},
            {"name": "Central Park", "lat": 40.7829, "lon": -73.9654},
            {"name": "Financial District", "lat": 40.7074, "lon": -74.0113}
        ]
    },
    "tehran": {
        "name": "Tehran",
        "center_lat": 35.6892,
        "center_lon": 51.3890,
        "zoom_level": 12,
        "tile_coverage_km": 10,
        "description": "Tehran metropolitan area",
        "priority_locations": [
            {"name": "Azadi Tower", "lat": 35.6996, "lon": 51.3380},
            {"name": "Milad Tower", "lat": 35.7448, "lon": 51.3753},
            {"name": "Tehran Bazaar", "lat": 35.6738, "lon": 51.4237}
        ]
    }
}


def get_area_by_id(area_id: str):
    """Get area configuration by ID."""
    return AREAS.get(area_id)


def get_all_areas():
    """Get all available areas."""
    return AREAS


def find_nearest_area(lat: float, lon: float):
    """Find nearest area to given coordinates."""
    import math
    
    nearest = None
    min_distance = float('inf')
    
    for area_id, config in AREAS.items():
        # Calculate approximate distance
        dlat = lat - config['center_lat']
        dlon = lon - config['center_lon']
        distance = math.sqrt(dlat**2 + dlon**2)
        
        if distance < min_distance:
            min_distance = distance
            nearest = area_id
    
    return nearest
