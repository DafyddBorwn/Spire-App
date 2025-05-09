import pandas as pd

def calculate_heat_loss(property_data):
    """
    Calculate the heat loss of a property based on its characteristics.
    
    Args:
        property_data: A dictionary containing property information
        
    Returns:
        A dictionary with calculated heat loss values and ratings
    """
    # Extract property data
    property_type = property_data["property_type"]
    construction_year = property_data["construction_year"]
    floor_area = property_data["floor_area"]
    ceiling_height = property_data["ceiling_height"]
    insulation_level = property_data["insulation_level"]
    windows_quality = property_data["windows_quality"]
    num_bedrooms = property_data["num_bedrooms"]
    location = property_data["location"]
    
    # Calculate volume
    volume = floor_area * ceiling_height
    
    # Base heat loss factors (W/m²K)
    # These are approximate U-values used for estimation
    insulation_factors = {
        "Poor": 1.5,
        "Below Average": 1.2,
        "Average": 1.0,
        "Good": 0.8,
        "Excellent": 0.6
    }
    
    window_factors = {
        "Single Glazed": 5.0,
        "Double Glazed (Old)": 3.0,
        "Double Glazed (New)": 1.8,
        "Triple Glazed": 1.0
    }
    
    construction_factors = {
        "Pre-1919": 1.4,
        "1919-1944": 1.3,
        "1945-1964": 1.2,
        "1965-1980": 1.1,
        "1981-2000": 0.9,
        "Post-2000": 0.7
    }
    
    property_type_factors = {
        "Detached House": 1.3,
        "Semi-Detached House": 1.1,
        "Terraced House": 1.0,
        "Apartment/Flat": 0.9,
        "Bungalow": 1.2
    }
    
    location_factors = {
        "North": 1.15,
        "Midlands": 1.05,
        "South": 1.0,
        "Scotland": 1.2,
        "Wales": 1.1,
        "Northern Ireland": 1.1
    }
    
    # Apply factors to calculate component heat losses
    
    # Determine wall area (approximate)
    perimeter = (4 * (floor_area ** 0.5))  # Estimate perimeter based on square floor area
    wall_area = perimeter * ceiling_height
    
    # Calculate individual component heat losses
    base_temp_diff = 20  # Base temperature difference between inside and outside (°C)
    
    # Wall heat loss
    wall_u_value = 1.0 * insulation_factors[insulation_level] * construction_factors[construction_year]
    wall_loss = wall_area * wall_u_value * base_temp_diff / 1000  # Convert W to kW
    
    # Roof heat loss (estimated as 25% of floor area)
    roof_area = floor_area
    roof_u_value = 0.8 * insulation_factors[insulation_level] * construction_factors[construction_year]
    roof_loss = roof_area * roof_u_value * base_temp_diff / 1000
    
    # Window heat loss (estimated as 15% of wall area)
    window_area = wall_area * 0.15
    window_u_value = window_factors[windows_quality]
    window_loss = window_area * window_u_value * base_temp_diff / 1000
    
    # Floor heat loss
    floor_u_value = 0.7 * insulation_factors[insulation_level] * construction_factors[construction_year]
    floor_loss = floor_area * floor_u_value * base_temp_diff / 1000
    
    # Ventilation heat loss
    air_change_rate = 0.5  # air changes per hour (average)
    specific_heat_capacity = 0.33  # Wh/m³K
    ventilation_loss = volume * air_change_rate * specific_heat_capacity * base_temp_diff / 1000
    
    # Calculate total heat loss
    total_heat_loss = (wall_loss + roof_loss + window_loss + floor_loss + ventilation_loss) * \
                      property_type_factors[property_type] * location_factors[location]
    
    # Heat loss per m²
    heat_loss_per_sqm = (total_heat_loss * 1000) / floor_area  # W/m²
    
    # Determine efficiency rating based on heat loss per m²
    efficiency_rating = "F"
    if heat_loss_per_sqm < 40:
        efficiency_rating = "A"
    elif heat_loss_per_sqm < 60:
        efficiency_rating = "B"
    elif heat_loss_per_sqm < 90:
        efficiency_rating = "C"
    elif heat_loss_per_sqm < 120:
        efficiency_rating = "D"
    elif heat_loss_per_sqm < 150:
        efficiency_rating = "E"
    
    # Create result dictionary
    result = {
        "total_heat_loss": total_heat_loss,
        "heat_loss_per_sqm": heat_loss_per_sqm,
        "wall_loss": wall_loss,
        "roof_loss": roof_loss,
        "window_loss": window_loss,
        "floor_loss": floor_loss,
        "ventilation_loss": ventilation_loss,
        "efficiency_rating": efficiency_rating
    }
    
    return result
