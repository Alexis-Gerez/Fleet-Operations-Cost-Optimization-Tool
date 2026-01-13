import streamlit as st
import pandas as pd

def render_vehicles(data_manager):
    st.header("Vehicle Profiles")

    df = data_manager.get_data()

    # --- Sidebar: Filter & Add ---
    with st.sidebar:
        st.subheader("Actions")
        with st.expander("➕ Add New Vehicle"):
            with st.form("add_vehicle_form"):
                new_id = st.text_input("Vehicle ID (e.g., FLT-099)")
                new_type = st.selectbox("Type", ["Light Vehicle", "Heavy Truck", "Motorcycle"])
                new_model = st.text_input("Model")
                new_status = st.selectbox("Status", ["Active", "Maintenance", "Inactive"])
                new_mileage = st.number_input("Current Mileage (km)", min_value=0, value=0)
                new_consumption = st.number_input("Avg Consumption (L/100km)", min_value=0.0, value=10.0)
                
                submitted = st.form_submit_button("Add Vehicle")
                if submitted:
                    if new_id and new_model:
                        # Basic logic to set defaults for new fields
                        interval = 10000
                        if new_type == 'Heavy Truck': interval = 25000
                        if new_type == 'Motorcycle': interval = 5000
                        
                        vehicle_data = {
                            'vehicle_id': new_id,
                            'type': new_type,
                            'model': new_model,
                            'status': new_status,
                            'current_mileage': new_mileage,
                            'last_service_mileage': new_mileage, # Assume fresh
                            'service_interval_km': interval,
                            'avg_consumption_l_100km': new_consumption,
                            'fuel_cost_per_l': 1.50
                        }
                        data_manager.add_vehicle(vehicle_data)
                        st.success(f"Vehicle {new_id} added.")
                        st.rerun()
                    else:
                        st.error("ID and Model are required.")

    # --- Main Filters ---
    st.subheader("Fleet Register")
    
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.multiselect("Filter by Type", df['type'].unique(), default=df['type'].unique())
    with col2:
        status_filter = st.multiselect("Filter by Status", df['status'].unique(), default=df['status'].unique())

    # --- Apply Filters ---
    filtered_df = df[df['type'].isin(type_filter) & df['status'].isin(status_filter)]

    # --- Display Table ---
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "vehicle_id": "ID",
            "current_mileage": st.column_config.NumberColumn(
                "Mileage",
                format="%d km"
            ),
             "avg_consumption_l_100km": st.column_config.NumberColumn(
                "Consumption",
                format="%.1f L/100km"
            ),
            "status": st.column_config.TextColumn("Status")
        },
        hide_index=True
    )

    # --- Download ---
    st.download_button(
        label="Download Fleet CSV",
        data=data_manager.get_csv_template(),
        file_name='fleet_data.csv',
        mime='text/csv',
    )
