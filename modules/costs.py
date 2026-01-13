import streamlit as st
import pandas as pd
import plotly.express as px

def render_costs(data_manager):
    st.header("Cost Analysis & Optimization")
    
    df = data_manager.get_data()
    
    if df.empty:
        st.info("No data available for analysis.")
        return

    # --- Calculations ---
    # Estimated Total Fuel Cost to date (lifetime)
    # Formula: (Current Mileage / 100) * Avg Consumption * Fuel Price
    df['est_fuel_cost'] = (df['current_mileage'] / 100) * df['avg_consumption_l_100km'] * df['fuel_cost_per_l']
    
    # Maintenance Cost Estimation (Simple heuristic: 0.10 per km for light, 0.30 for heavy, 0.05 for moto)
    # In a real app, this would be historical data.
    def estimate_maint_cost(row):
        rate = 0.10
        if row['type'] == 'Heavy Truck': rate = 0.30
        elif row['type'] == 'Motorcycle': rate = 0.05
        return row['current_mileage'] * rate

    df['est_maint_cost'] = df.apply(estimate_maint_cost, axis=1)
    df['total_cost'] = df['est_fuel_cost'] + df['est_maint_cost']
    df['cost_per_km'] = df['total_cost'] / df['current_mileage'].replace(0, 1)

    # --- KPIs ---
    total_fuel_spend = df['est_fuel_cost'].sum()
    total_maint_spend = df['est_maint_cost'].sum()
    avg_cpk = df['cost_per_km'].mean()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Est. Lifetime Fuel Cost", f"${total_fuel_spend:,.0f}")
    with c2:
        st.metric("Est. Lifetime Maint. Cost", f"${total_maint_spend:,.0f}")
    with c3:
        st.metric("Avg Cost per Km", f"${avg_cpk:.2f}")

    st.markdown("---")

    # --- Charts ---
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        st.subheader("Cost Distribution by Vehicle Type")
        # Aggregation
        cost_by_type = df.groupby('type')[['est_fuel_cost', 'est_maint_cost']].sum().reset_index()
        # Melt for stacked bar
        cost_melted = cost_by_type.melt(id_vars='type', var_name='Cost Type', value_name='Amount')
        
        # Get theme text color
        theme_text = st.session_state.get('theme', {}).get('text_color', '#FAFAFA')

        fig_cost = px.bar(cost_melted, x='type', y='Amount', color='Cost Type',
                          color_discrete_sequence=['#4A90E2', '#EF5350'], barmode='group')
        fig_cost.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=theme_text)
        st.plotly_chart(fig_cost, use_container_width=True)

    with c_chart2:
        st.subheader("Cost Efficiency (Cost/Km vs Mileage)")
        fig_scatter = px.scatter(df, x='current_mileage', y='cost_per_km', color='type',
                                 hover_data=['vehicle_id'], size='avg_consumption_l_100km')
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=theme_text)
        st.plotly_chart(fig_scatter, use_container_width=True)
