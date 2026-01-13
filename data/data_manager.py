import pandas as pd
import streamlit as st
import numpy as np

class FleetDataManager:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initializes the fleet data in session state if it doesn't exist."""
        if 'fleet_data' not in st.session_state:
            st.session_state.fleet_data = self.generate_mock_data()

    def generate_mock_data(self):
        """Generates a realistic mock dataset for the fleet."""
        data = {
            'vehicle_id': [f'FLT-{i:03d}' for i in range(1, 21)],
            'type': np.random.choice(['Light Vehicle', 'Heavy Truck', 'Motorcycle'], 20, p=[0.5, 0.3, 0.2]),
            'model': np.random.choice(['Toyota Hilux', 'Ford Ranger', 'Volvo FH16', 'Scania R500', 'Honda CRF', 'Yamaha XT'], 20),
            'status': np.random.choice(['Active', 'Maintenance', 'Inactive'], 20, p=[0.8, 0.15, 0.05]),
            'current_mileage': np.random.randint(1000, 150000, 20),
            'last_service_mileage': np.zeros(20), # Will be calculated relative to current
            'service_interval_km': np.zeros(20),
            'avg_consumption_l_100km': np.zeros(20),
            'fuel_cost_per_l': 1.50 # Standard placeholder
        }
        
        df = pd.DataFrame(data)
        
        # Refine data based on type
        for index, row in df.iterrows():
            interval = 10000
            consumption = 10.0
            
            if row['type'] == 'Light Vehicle':
                interval = 10000
                consumption = np.random.uniform(9, 12)
            elif row['type'] == 'Heavy Truck':
                interval = 25000
                consumption = np.random.uniform(25, 35)
            else: # Motorcycle
                interval = 5000
                consumption = np.random.uniform(3, 5)
            
            df.at[index, 'service_interval_km'] = interval
            df.at[index, 'avg_consumption_l_100km'] = consumption
            
            # Set last service reasonably close to calculated logic or random
            # Logic: last service was somewhere between (current - interval) and current
            # Use local 'interval' variable as row['service_interval_km'] is from before the update in this loop iteration
            high_bound = int(interval * 1.1)
            if high_bound <= 500: high_bound = 501 # Safety check
            
            last_service = max(0, row['current_mileage'] - np.random.randint(500, high_bound))
            df.at[index, 'last_service_mileage'] = int(last_service)

        return df

    def get_data(self):
        """Returns the current fleet dataframe."""
        return st.session_state.fleet_data

    def add_vehicle(self, vehicle_data):
        """Adds a new vehicle to the session state dataframe."""
        new_row = pd.DataFrame([vehicle_data])
        st.session_state.fleet_data = pd.concat([st.session_state.fleet_data, new_row], ignore_index=True)

    def load_from_csv(self, file_buffer):
        """Loads data from an uploaded CSV file."""
        try:
            df = pd.read_csv(file_buffer)
            # Basic validation could go here
            st.session_state.fleet_data = df
            return True, "Data loaded successfully."
        except Exception as e:
            return False, str(e)

    def get_csv_template(self):
        """Returns a CSV string of the current data (or empty template) for download."""
        return st.session_state.fleet_data.to_csv(index=False).encode('utf-8')
