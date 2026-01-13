import streamlit as st
import pandas as pd
import plotly.express as px

def render_overview(data_manager):
    st.header("Fleet Overview")
    
    df = data_manager.get_data()
    
    # 1. Top Level KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_vehicles = len(df)
    active_vehicles = len(df[df['status'] == 'Active'])
    active_pct = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
    avg_mileage = df['current_mileage'].mean()
    total_maintenance = len(df[df['status'] == 'Maintenance'])

    with col1:
        st.metric("Total Fleet Size", f"{total_vehicles}")
    with col2:
        st.metric("Active Units", f"{active_vehicles}", delta=f"{active_pct:.1f}% of fleet")
    with col3:
        st.metric("Avg Mileage", f"{avg_mileage:,.0f} km")
    with col4:
        st.metric("In Maintenance", f"{total_maintenance}", delta_color="inverse")

    st.markdown("---")

    # 2. Composition Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Fleet Composition by Type")
        if not df.empty:
            # Custom industrial palette
            industrial_colors = ['#4A90E2', '#546E7A', '#78909C', '#B0BEC5', '#ECEFF1']
            
            # Get theme text color (default to white if not set)
            theme_text = st.session_state.get('theme', {}).get('text_color', '#FAFAFA')
            
            fig_type = px.pie(df, names='type', hole=0.4, color_discrete_sequence=industrial_colors)
            fig_type.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=theme_text)
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("No data available.")

    with c2:
        st.subheader("Operational Status")
        if not df.empty:
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            
            # Custom colors for status
            color_map = {'Active': '#2E7D32', 'Maintenance': '#F9A825', 'Inactive': '#C62828'}
            
            fig_status = px.bar(status_counts, x='status', y='count', color='status', 
                                color_discrete_map=color_map)
            fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=theme_text, showlegend=False)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No data available.")

    # 3. Quick Table Preview (Top 5 mileage)
    st.subheader("High Mileage Assets (Top 5)")
    if not df.empty:
        top_mileage = df.nlargest(5, 'current_mileage')[['vehicle_id', 'type', 'model', 'current_mileage', 'status']]
        st.dataframe(top_mileage, use_container_width=True, hide_index=True)
