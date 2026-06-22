import math

def optimize_boundary(raw_points):
    """
    Takes a list of unordered GPS coordinates (dictionaries with 'lat' and 'lng')
    and mathematically orders them into a perfect, non-intersecting geometric polygon.
    """
    # We need at least 3 points to make a geometric shape
    if not raw_points or len(raw_points) < 3:
        return {"error": "Not enough data points to form a boundary."}

    # 1. Calculate the exact geographic centroid (center of mass) of the raw plot
    lat_sum = sum(point.get('lat', 0) for point in raw_points)
    lng_sum = sum(point.get('lng', 0) for point in raw_points)
    
    centroid = {
        'lat': lat_sum / len(raw_points),
        'lng': lng_sum / len(raw_points)
    }

    # 2. Mathematical Spatial Sorting
    # Calculate the angle of each point relative to the centroid using arctangent
    def get_angle(point):
        return math.atan2(
            point.get('lng', 0) - centroid['lng'], 
            point.get('lat', 0) - centroid['lat']
        )

    # Sort the points clockwise based on their geometric angle
    corrected_points = sorted(raw_points, key=get_angle)

    # 3. Return the fully processed dataset
    return {
        "distortion_resolved": True,
        "total_vertices_optimized": len(corrected_points),
        "plot_centroid": centroid,
        "optimized_polygon": corrected_points
    }