import streamlit as st
from styles.style_config import apply_theme
from data.data_manager import FleetDataManager
from modules.overview import render_overview
from modules.vehicles import render_vehicles
from modules.costs import render_costs
from modules.maintenance import render_maintenance
from modules.insights import render_insights

# Page Config
st.set_page_config(
    page_title="Fleet Operations Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Industrial CSS (Moved to inside main for Dynamic Theme support)
# load_css()

def main():
    # Initialize Data Manager
    data_manager = FleetDataManager()
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("Fleet Ops")
        st.markdown("Operational Control Unit")
        st.markdown("---")
        
        nav_options = [
            "Network Overview", 
            "Vehicle Register", 
            "Cost Analysis", 
            "Maintenance Planner",
            "Predictive Insights"
        ]
        
        selection = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        
        # Theme Selector
        theme_choice = st.selectbox(
            "Visual Theme", 
            ["Industrial Dark", "Light Corporate", "Midnight Blue"],
            index=0
        )
        
        st.caption("v1.1.0 | Enterprise Edition")

    # Apply Theme
    apply_theme(theme_choice)

    # Routing
    if selection == "Network Overview":
        render_overview(data_manager)
    elif selection == "Vehicle Register":
        render_vehicles(data_manager)
    elif selection == "Cost Analysis":
        render_costs(data_manager)
    elif selection == "Maintenance Planner":
        render_maintenance(data_manager)
    elif selection == "Predictive Insights":
        render_insights(data_manager)

if __name__ == "__main__":
    main()
