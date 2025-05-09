import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from streamlit.dataframe_util import OptionSequence
from heat_loss_calculator import calculate_heat_loss
from product_packs import get_product_packs
from quotation_generator import generate_quotation
from pdf_export import get_pdf_download_link
import base64

# Set page configuration with custom energy icon
# This icon was created as a proxy for https://mobile.x.com/SpireRenewables
# If Twitter fetching capability is needed in the future, a more robust solution can be implemented
icon_path = "spire_logo.jpg"
st.set_page_config(
    page_title="Air Source Heat Pump Calculator",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="expanded"
)

# App header and introduction
st.title("Spire Renewables ASHP Calculator")
st.markdown("""
This calculator helps you estimate the heat loss in your property and provides 
recommended air source heat pump solutions with estimated costs.

Fill in the questionnaire below to get your personalized ASHP quotation.
You can easily export your quotation to your mobile phone or computer for saving or sharing.
""")

# Create sidebar with instructions
with st.sidebar:
    st.header("How It Works")
    st.markdown("""
    1. Fill in the questionnaire as accuratly as possible
    2. The calculator will estimate your property's heat loss
    3. Based on the heat loss, we'll recommend appropriate air source heat pump solutions
    4. A detailed quotation will be generated with estimated costs
    """)
    
    st.header("Spire Renewables")
    st.markdown("""
    What Spire Renewables Offer:
    
    - ASHP sizing and design tailored to your property
    - UFH designs and supply
    - Radiator sizing and supply
    - MCS signoff and access to the Boiler Upgrade Scheme
    - Installation and commissioning
    - Aftercare and maintenance support
    - Competitive pricing and no hidden costs
    - Expert advice and guidance
    """)

# Initialize session state variables if they don't exist
if 'calculation_complete' not in st.session_state:
    st.session_state.calculation_complete = False
    
if 'heat_loss' not in st.session_state:
    st.session_state.heat_loss = None
    
if 'quotation' not in st.session_state:
    st.session_state.quotation = None

# Main questionnaire
st.header("Property Details Questionnaire")

with st.form("heat_loss_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        property_type = st.selectbox(
            "Property Type",
            options=["Detached House", "Semi-Detached House", "Terraced House", "Apartment/Flat", "Bungalow"],
            help="Select the type of property you have"
        )
        
        construction_year = st.selectbox(
            "Construction Year",
            options=["Pre-1919", "1919-1944", "1945-1964", "1965-1980", "1981-2000", "Post-2000"],
            help="Select the approximate period when your property was built"
        )
        
        floor_area = st.number_input(
            "Total Floor Area (m²)",
            min_value=10,
            max_value=1000,
            value=100,
            help="Enter the total floor area of your property in square meters"
        )
        
        ceiling_height = st.number_input(
            "Average Ceiling Height (m)",
            min_value=2.0,
            max_value=5.0,
            value=2.4,
            step=0.1,
            help="Enter the average ceiling height in meters"
        )
        
    with col2:
        insulation_level = st.select_slider(
            "Insulation Level",
            options=["Poor", "Below Average", "Average", "Good", "Excellent"],
            value="Average",
            help="Select the level of insulation in your property"
        )
        
        windows_quality = st.selectbox(
            "Windows Quality",
            options=["Single Glazed", "Double Glazed (Old)", "Double Glazed (New)", "Triple Glazed"],
            help="Select the type of windows in your property"
        )
        
        num_bedrooms = st.select_slider(
            "Number of Bedrooms",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            value=3,
            help="Enter the number of bedrooms in your property"
        )
        
        location = st.selectbox(
            "Property Location Region",
            options=["North", "Midlands", "South", "Scotland", "Wales", "Northern Ireland"],
            help="Select the region where your property is located"
        )
    
    submitted = st.form_submit_button("Calculate Heat Loss & Generate ASHP Quotation")
    
    if submitted:
        # Create a dictionary with the form inputs
        property_data = {
            "property_type": property_type,
            "construction_year": construction_year,
            "floor_area": floor_area,
            "ceiling_height": ceiling_height,
            "insulation_level": insulation_level,
            "windows_quality": windows_quality,
            "num_bedrooms": num_bedrooms,
            "location": location
        }
        
        # Calculate the heat loss
        heat_loss = calculate_heat_loss(property_data)
        
        # Get available product packs
        product_packs = get_product_packs()
        
        # Generate quotation based on heat loss and product packs
        quotation = generate_quotation(heat_loss, product_packs, property_data)
        
        # Store results in session state
        st.session_state.heat_loss = heat_loss
        st.session_state.quotation = quotation
        st.session_state.calculation_complete = True
        st.session_state.property_data = property_data

# Display results if calculation is complete
if st.session_state.calculation_complete:
    st.header("Heat Loss Assessment Results")
    
    heat_loss = st.session_state.heat_loss
    quotation = st.session_state.quotation
    property_data = st.session_state.property_data
    
    # Heat loss summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Heat Loss", 
            value=f"{heat_loss['total_heat_loss']:.2f} kW",
            delta=None
        )
        
    with col2:
        st.metric(
            label="Heat Loss per m²", 
            value=f"{heat_loss['heat_loss_per_sqm']:.2f} W/m²",
            delta=None
        )
        
    with col3:
        st.metric(
            label="Energy Efficiency Rating", 
            value=heat_loss['efficiency_rating'],
            delta=None
        )
    
    # Detailed breakdown
    with st.expander("Detailed Heat Loss Breakdown"):
        st.markdown(f"**Wall Heat Loss:** {heat_loss['wall_loss']:.2f} kW")
        st.markdown(f"**Roof Heat Loss:** {heat_loss['roof_loss']:.2f} kW")
        st.markdown(f"**Window Heat Loss:** {heat_loss['window_loss']:.2f} kW")
        st.markdown(f"**Floor Heat Loss:** {heat_loss['floor_loss']:.2f} kW")
        st.markdown(f"**Ventilation Heat Loss:** {heat_loss['ventilation_loss']:.2f} kW")
        
        # Display heat loss chart
        heat_loss_data = {
            'Category': ['Walls', 'Roof', 'Windows', 'Floor', 'Ventilation'],
            'Heat Loss (kW)': [
                heat_loss['wall_loss'],
                heat_loss['roof_loss'],
                heat_loss['window_loss'],
                heat_loss['floor_loss'],
                heat_loss['ventilation_loss']
            ]
        }
        heat_loss_df = pd.DataFrame(heat_loss_data)
        st.bar_chart(heat_loss_df.set_index('Category'))
        
    # Quotation details
    st.header("Air Source Heat Pump Quotation")
    
    # Recommended solution
    st.subheader("Recommended ASHP Solution")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Package:** {quotation['recommended_pack']['name']}")
        st.markdown(f"**Description:** {quotation['recommended_pack']['description']}")
        st.markdown("**Features:**")
        for feature in quotation['recommended_pack']['features']:
            st.markdown(f"- {feature}")
    
    with col2:
        st.markdown(f"**Price:** £{quotation['recommended_pack']['price']:.2f}")
        st.markdown(f"**Installation Estimate:** £{quotation['installation_cost']:.2f}")
        st.markdown(f"**Total Cost:** £{quotation['total_cost']:.2f}")
    
    # Package comparison view
    st.subheader("Package Comparison")
    
    # Create tabs for different comparison views
    tab1, tab2 = st.tabs(["Features Comparison", "Price Comparison"])
    
    with tab1:
        # Prepare data for the comparison table
        comparison_data = {
            "Feature": ["Price", "Installation Cost", "Total Cost"] + 
                      ["Feature: " + feature for feature in quotation['recommended_pack']['features']]
        }
        
        # Add recommended pack to comparison
        recommended = quotation['recommended_pack']
        comparison_data[recommended['name']] = [
            f"£{recommended['price']:.2f}",
            f"£{quotation['installation_cost']:.2f}",
            f"£{quotation['total_cost']:.2f}"
        ]
        
        # Add checkmarks for features
        for feature in comparison_data["Feature"][3:]:
            feature_name = feature.replace("Feature: ", "")
            if feature_name in recommended['features']:
                comparison_data[recommended['name']].append("✅")
            else:
                comparison_data[recommended['name']].append("❌")
        
        # Add alternative packs to comparison
        for pack in quotation['alternative_packs']:
            # Basic information
            comparison_data[pack['name']] = [
                f"£{pack['price']:.2f}",
                f"£{quotation['installation_cost']:.2f}",
                f"£{pack['price'] + quotation['installation_cost']:.2f}"
            ]
            
            # Add checkmarks for features
            for feature in comparison_data["Feature"][3:]:
                feature_name = feature.replace("Feature: ", "")
                if feature_name in pack['features']:
                    comparison_data[pack['name']].append("✅")
                else:
                    comparison_data[pack['name']].append("❌")
        
        # Create DataFrame for display
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df.set_index("Feature"), use_container_width=True)
    
    with tab2:
        # Prepare data for price comparison chart
        price_data = {
            'Package': [recommended['name']] + [pack['name'] for pack in quotation['alternative_packs']],
            'Product Price (£)': [recommended['price']] + [pack['price'] for pack in quotation['alternative_packs']],
            'Installation Cost (£)': [quotation['installation_cost']] * (1 + len(quotation['alternative_packs']))
        }
        
        # Create a DataFrame for the chart
        price_df = pd.DataFrame(price_data)
        
        # Create a stacked bar chart
        st.bar_chart(price_df.set_index('Package'), use_container_width=True)
        
        # Create a table with payback period calculation for each package
        payback_data = {
            'Package': [recommended['name']] + [pack['name'] for pack in quotation['alternative_packs']],
            'Total Cost (£)': [
                quotation['total_cost']] + 
                [pack['price'] + quotation['installation_cost'] for pack in quotation['alternative_packs']
            ],
            'Estimated Annual Savings (£)': [quotation['estimated_annual_savings']] * (1 + len(quotation['alternative_packs'])),
            'Payback Period (years)': [
                quotation['payback_period']] + 
                [(pack['price'] + quotation['installation_cost']) / quotation['estimated_annual_savings'] 
                 for pack in quotation['alternative_packs']
            ]
        }
        
        # Create DataFrame for the payback period table
        payback_df = pd.DataFrame(payback_data)
        st.dataframe(payback_df.set_index('Package'), use_container_width=True)
    
    # Alternative packages
    st.subheader("Alternative ASHP Options")
    alternative_cols = st.columns(len(quotation['alternative_packs']))
    
    for i, (col, pack) in enumerate(zip(alternative_cols, quotation['alternative_packs'])):
        with col:
            st.markdown(f"**{pack['name']}**")
            st.markdown(f"£{pack['price']:.2f}")
            with st.expander("Details"):
                st.markdown(f"**Description:** {pack['description']}")
                st.markdown("**Features:**")
                for feature in pack['features']:
                    st.markdown(f"- {feature}")
    
    # Savings and recommendations
    st.subheader("Potential Savings and Recommendations")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Estimated Annual Savings:** £{quotation['estimated_annual_savings']:.2f}")
        st.markdown(f"**Payback Period:** {quotation['payback_period']:.1f} years")
    
    with col2:
        st.markdown("**Additional Recommendations:**")
        for recommendation in quotation['additional_recommendations']:
            st.markdown(f"- {recommendation}")
    
    # Download Quotation
    st.subheader("Export Quotation")
    st.markdown("Download a detailed quotation to your phone or computer for easy reference or sharing.")
    
    pdf_download = get_pdf_download_link(heat_loss, quotation, property_data)
    st.markdown(pdf_download, unsafe_allow_html=True)
    
    # Reset button
    if st.button("Reset Calculator"):
        st.session_state.calculation_complete = False
        st.session_state.heat_loss = None
        st.session_state.quotation = None
        st.rerun()
