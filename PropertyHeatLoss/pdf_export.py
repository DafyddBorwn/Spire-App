import base64
from fpdf import FPDF
from datetime import datetime
import streamlit as st

def get_pdf_download_link(heat_loss, quotation, property_data, filename="ashp_quotation.txt"):
    """
    Generate a download link for the quotation PDF
    
    Args:
        heat_loss: Dictionary containing heat loss calculations
        quotation: Dictionary containing quotation details
        property_data: Dictionary containing property information
        filename: Name of the file to download
        
    Returns:
        HTML string with download link
    """
    pdf_content = create_pdf_content(heat_loss, quotation, property_data)
    
    # Encode the string as bytes and then base64
    b64 = base64.b64encode(pdf_content.encode()).decode()
    
    # Create download link with styling
    href = f'''
    <a href="data:text/plain;base64,{b64}" 
       download="{filename}" 
       style="display: inline-block; 
              background-color: #4CAF50; 
              color: white; 
              padding: 12px 20px; 
              text-align: center; 
              text-decoration: none; 
              font-size: 16px; 
              margin: 4px 2px; 
              border-radius: 8px;">
        📥 Download Quotation
    </a>
    '''
    
    return href

def create_pdf_content(heat_loss, quotation, property_data):
    """
    Create a simple text version of the quotation content
    
    Args:
        heat_loss: Dictionary containing heat loss calculations
        quotation: Dictionary containing quotation details
        property_data: Dictionary containing property information
        
    Returns:
        String with formatted content
    """
    content = []
    
    # Title
    content.append("AIR SOURCE HEAT PUMP QUOTATION")
    content.append(f"Generated on {datetime.now().strftime('%Y-%m-%d')}")
    content.append("\n")
    
    # Property Information
    content.append("PROPERTY INFORMATION")
    content.append("-" * 50)
    content.append(f"Property Type: {property_data['property_type']}")
    content.append(f"Construction Year: {property_data['construction_year']}")
    content.append(f"Floor Area: {property_data['floor_area']} m²")
    content.append(f"Insulation Level: {property_data['insulation_level']}")
    content.append(f"Windows Quality: {property_data['windows_quality']}")
    content.append("\n")
    
    # Heat Loss Results
    content.append("HEAT LOSS ASSESSMENT")
    content.append("-" * 50)
    content.append(f"Total Heat Loss: {heat_loss['total_heat_loss']:.2f} kW")
    content.append(f"Heat Loss per m²: {heat_loss['heat_loss_per_sqm']:.2f} W/m²")
    content.append(f"Energy Efficiency Rating: {heat_loss['efficiency_rating']}")
    content.append("\n")
    
    # Heat Loss Breakdown
    content.append("HEAT LOSS BREAKDOWN")
    content.append("-" * 50)
    content.append(f"Wall Heat Loss: {heat_loss['wall_loss']:.2f} kW")
    content.append(f"Roof Heat Loss: {heat_loss['roof_loss']:.2f} kW")
    content.append(f"Window Heat Loss: {heat_loss['window_loss']:.2f} kW")
    content.append(f"Floor Heat Loss: {heat_loss['floor_loss']:.2f} kW")
    content.append(f"Ventilation Heat Loss: {heat_loss['ventilation_loss']:.2f} kW")
    content.append("\n")
    
    # Recommended Solution
    content.append("RECOMMENDED AIR SOURCE HEAT PUMP SOLUTION")
    content.append("-" * 50)
    
    recommended_pack = quotation['recommended_pack']
    
    content.append(f"Package: {recommended_pack['name']}")
    content.append(f"Description: {recommended_pack['description']}")
    
    # Features
    content.append("\nFeatures:")
    for feature in recommended_pack['features']:
        content.append(f"- {feature}")
    
    # Costs
    content.append("\nPRICING DETAILS")
    content.append("-" * 50)
    content.append(f"Product Price: £{recommended_pack['price']:.2f}")
    content.append(f"Installation Cost: £{quotation['installation_cost']:.2f}")
    content.append(f"Total Cost: £{quotation['total_cost']:.2f}")
    content.append("\n")
    
    # Savings
    content.append("POTENTIAL SAVINGS")
    content.append("-" * 50)
    content.append(f"Estimated Annual Savings: £{quotation['estimated_annual_savings']:.2f}")
    content.append(f"Payback Period: {quotation['payback_period']:.1f} years")
    content.append("\n")
    
    # Recommendations
    content.append("ADDITIONAL RECOMMENDATIONS")
    content.append("-" * 50)
    for recommendation in quotation['additional_recommendations']:
        content.append(f"- {recommendation}")
    
    # Disclaimer
    content.append("\nDISCLAIMER")
    content.append("-" * 50)
    content.append("This is an estimated quotation based on the information provided. A detailed site survey would be required for a final quotation. Prices are inclusive of VAT. The estimated savings are based on average energy usage and may vary depending on your specific usage patterns and energy prices.")
    
    return "\n".join(content)