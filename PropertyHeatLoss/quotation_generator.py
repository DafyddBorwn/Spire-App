import random

def generate_quotation(heat_loss, product_packs, property_data):
    """
    Generate an air source heat pump quotation based on heat loss calculation and available product packs.
    
    Args:
        heat_loss: Dictionary containing heat loss calculations
        product_packs: List of available air source heat pump product packs
        property_data: Dictionary containing property information
        
    Returns:
        A dictionary with quotation details
    """
    # Extract total heat loss
    total_heat_loss = heat_loss["total_heat_loss"]
    
    # Find suitable product packs based on total heat loss
    suitable_packs = []
    for pack in product_packs:
        if pack["min_heat_loss"] <= total_heat_loss <= pack["max_heat_loss"]:
            suitable_packs.append(pack)
    
    # If no suitable packs, select the one with closest max_heat_loss
    if not suitable_packs:
        if total_heat_loss < min(pack["min_heat_loss"] for pack in product_packs):
            suitable_packs = [min(product_packs, key=lambda x: x["min_heat_loss"])]
        else:
            suitable_packs = [max(product_packs, key=lambda x: x["max_heat_loss"])]
    
    # Select the most appropriate pack (middle of the range)
    recommended_pack = sorted(suitable_packs, key=lambda x: abs(total_heat_loss - (x["min_heat_loss"] + x["max_heat_loss"]) / 2))[0]
    
    # Find alternative packs (up to 3)
    alternative_packs = []
    for pack in product_packs:
        if pack["id"] != recommended_pack["id"]:
            alternative_packs.append(pack)
    
    # Sort alternatives by price and select up to 3
    alternative_packs = sorted(alternative_packs, key=lambda x: x["price"])[:3]
    
    # Calculate installation costs (based on property size, heat loss, and additional ASHP factors)
    base_installation_cost = 3500  # Higher base cost for ASHP installation
    size_factor = property_data["floor_area"] / 100  # Normalize to 100m²
    complexity_factor = 1.0
    
    # Adjust complexity factor based on property type and construction year
    if property_data["property_type"] in ["Detached House", "Bungalow"]:
        complexity_factor *= 1.2
    
    if property_data["construction_year"] in ["Pre-1919", "1919-1944"]:
        complexity_factor *= 1.4  # Older properties often need more work for ASHP
    
    # ASHP-specific factors
    # Check if radiator upgrades likely needed (based on insulation level and windows)
    radiator_upgrade_factor = 1.0
    if property_data["insulation_level"] in ["Poor", "Below Average"] or property_data["windows_quality"] == "Single Glazed":
        radiator_upgrade_factor = 1.3  # Likely needs radiator upgrades for ASHP
    
    installation_cost = base_installation_cost * size_factor * complexity_factor * radiator_upgrade_factor
    
    # Calculate total cost
    total_cost = recommended_pack["price"] + installation_cost
    
    # Calculate estimated annual savings compared to traditional heating
    # This is a simplified calculation for demonstration purposes
    average_gas_heating_cost = 1200  # Assumed average annual gas heating cost
    average_electricity_cost_for_ashp = 800  # Assumed average electricity cost to run ASHP
    
    # Calculate estimated savings based on efficiency ratings
    base_savings = average_gas_heating_cost - average_electricity_cost_for_ashp
    
    efficiency_multiplier = 1.0
    if heat_loss["efficiency_rating"] == "A":
        efficiency_multiplier = 1.3  # Better efficiency = better savings
    elif heat_loss["efficiency_rating"] == "B":
        efficiency_multiplier = 1.2
    elif heat_loss["efficiency_rating"] == "C":
        efficiency_multiplier = 1.1
    elif heat_loss["efficiency_rating"] == "D":
        efficiency_multiplier = 1.0
    elif heat_loss["efficiency_rating"] == "E":
        efficiency_multiplier = 0.9
    else:
        efficiency_multiplier = 0.8  # Poor efficiency = lower savings
    
    estimated_annual_savings = base_savings * efficiency_multiplier
    
    # Calculate payback period
    payback_period = total_cost / estimated_annual_savings if estimated_annual_savings > 0 else float('inf')
    
    # Generate additional recommendations based on property data with ASHP focus
    additional_recommendations = []
    
    if property_data["insulation_level"] in ["Poor", "Below Average"]:
        additional_recommendations.append("Improve wall and loft insulation to maximize heat pump efficiency")
    
    if property_data["windows_quality"] in ["Single Glazed", "Double Glazed (Old)"]:
        additional_recommendations.append("Upgrade windows to improve insulation for optimal heat pump performance")
    
    # ASHP-specific recommendations
    if property_data["construction_year"] in ["Pre-1919", "1919-1944", "1945-1964"]:
        additional_recommendations.append("Consider upgrading to larger radiators or underfloor heating for optimal heat pump operation")
    
    # Add ASHP-specific general recommendations
    additional_recommendations.extend([
        "Install smart controls to optimize heat pump performance throughout the day",
        "Consider adding an additional hot water cylinder for increased efficiency",
        "Check eligibility for renewable heat incentive payments from the government"
    ])
    
    # Create quotation dictionary
    quotation = {
        "recommended_pack": recommended_pack,
        "alternative_packs": alternative_packs,
        "installation_cost": installation_cost,
        "total_cost": total_cost,
        "estimated_annual_savings": estimated_annual_savings,
        "payback_period": payback_period,
        "additional_recommendations": additional_recommendations
    }
    
    return quotation
