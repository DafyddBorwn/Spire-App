def get_product_packs():
    """
    Return a list of available air source heat pump product packs with their details.
    
    Returns:
        A list of dictionaries containing product pack information
    """
    # Define air source heat pump product packs with their specifications and prices
    product_packs = [
        {
            "id": "basic_ashp",
            "name": "Bufferless ASHP Package",
            "description": "An air source heat pump system for smaller properties with good insulation.",
            "min_heat_loss": 0,
            "max_heat_loss": 5,
            "price": 6999.99,
            "features": [
                "5-7kW Air Source Heat Pump",
                "Single zone heating control",
                "Manufacturer controller as property thermostat",
                "Hot water cylinder (150L)",
                "Standard radiator compatibility check",
                "7 year heat pump warranty"
            ],
            "ideal_for": ["Apartments", "Small houses", "Well-insulated properties"]
        },
        {
            "id": "standard_ashp",
            "name": "Multizone ASHP Package",
            "description": "Our most popular air source heat pump package, suitable for most average-sized properties.",
            "min_heat_loss": 5,
            "max_heat_loss": 10,
            "price": 8499.99,
            "features": [
                "8-10kW Air Source Heat Pump",
                "Dual zone heating control",
                "Smart thermostat with app control",
                "Hot water cylinder (200L)",
                "Radiator upgrade assessment",
                "Basic underfloor heating compatibility",
                "10 year heat pump warranty"
            ],
            "ideal_for": ["Semi-detached houses", "Terraced houses", "Medium-sized properties"]
        },
        {
            "id": "premium_ashp",
            "name": "Buffer Driven ASHP Package",
            "description": "A comprehensive air source heat pump solution for larger properties with higher heating demands.",
            "min_heat_loss": 10,
            "max_heat_loss": 15,
            "price": 10999.99,
            "features": [
                "11-14kW Air Source Heat Pump",
                "Multi-zone heating control",
                "Advanced smart control system",
                "Hot water cylinder (250L)",
                "Full radiator upgrade package",
                "Underfloor heating integration",
                "Smartphone app with energy monitoring",
                "12 year heat pump warranty"
            ],
            "ideal_for": ["Detached houses", "Larger properties", "Period properties"]
        },
        {
            "id": "elite_ashp",
            "name": "Elite ASHP Package",
            "description": "Our highest specification air source heat pump system for large properties with significant heating requirements.",
            "min_heat_loss": 15,
            "max_heat_loss": 100,
            "price": 14999.99,
            "features": [
                "16-18kW Air Source Heat Pump",
                "Comprehensive multi-zone heating control",
                "Premium smart control system",
                "Hot water cylinder (300L+)",
                "Complete radiator replacement package",
                "Full underfloor heating system",
                "Home energy management system",
                "Full system integration with home automation",
                "15 year heat pump warranty"
            ],
            "ideal_for": ["Large detached properties", "Properties with high heat demand", "Luxury homes"]
        },
        {
            "id": "hybrid_ashp",
            "name": "Hybrid ASHP Package",
            "description": "A flexible heating solution combining an air source heat pump with a backup boiler system for extreme conditions.",
            "min_heat_loss": 10,
            "max_heat_loss": 25,
            "price": 12499.99,
            "features": [
                "8-12kW Air Source Heat Pump",
                "Condensing backup boiler system",
                "Intelligent hybrid controller",
                "Smart energy switching based on efficiency",
                "Hot water cylinder (250L)",
                "Multi-zone temperature control",
                "Smartphone app with energy usage analytics",
                "10 year heat pump warranty"
            ],
            "ideal_for": ["Period properties", "Properties with varied heating needs", "Phased renewable transition"]
        }
    ]
    
    return product_packs
