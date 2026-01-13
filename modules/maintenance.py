import streamlit as st
import pandas as pd

def render_maintenance(data_manager):
    st.header("Preventive Maintenance Planner")
    
    df = data_manager.get_data()
    
    if df.empty:
        st.info("No data.")
        return

    # Calculate Due
    # Next Service = Last Service + Interval
    # Remaining = Next Service - Current
    df['next_service_at'] = df['last_service_mileage'] + df['service_interval_km']
    df['km_remaining'] = df['next_service_at'] - df['current_mileage']
    
    # Classify Status
    def get_maint_status(remaining):
        if remaining < 0: return "OVERDUE"
        if remaining < 1000: return "DUE SOON"
        return "OK"

    df['maint_status'] = df['km_remaining'].apply(get_maint_status)

    # Filters
    backlog = df[df['maint_status'] == 'OVERDUE']
    urgent = df[df['maint_status'] == 'DUE SOON']

    # --- Summary ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Maintenance Backlog (Overdue)", f"{len(backlog)} units", delta_color="inverse")
    with c2:
        st.metric("Upcoming (Next 1000km)", f"{len(urgent)} units")
    with c3:
        st.metric("Healthy Status", f"{len(df) - len(backlog) - len(urgent)} units")

    st.markdown("### Action Required")
    
    # Combined View of Overdue + Urgent
    action_items = pd.concat([backlog, urgent])
    
    if not action_items.empty:
        # Styling for DataTable to highlight rows (Streamlit doesn't support row-styling widely yet, using column logic)
        st.dataframe(
            action_items[['vehicle_id', 'type', 'current_mileage', 'km_remaining', 'maint_status']],
            use_container_width=True,
            column_config={
                "maint_status": st.column_config.TextColumn(
                    "Status",
                    help="Maintenance Status",
                ),
                "km_remaining": st.column_config.NumberColumn(
                    "Km Remaining",
                    format="%d km"
                )
            },
            hide_index=True
        )
    else:
        st.success("No immediate maintenance actions required.")

    st.markdown("### Full Schedule")
    st.dataframe(
        df[['vehicle_id', 'type', 'last_service_mileage', 'next_service_at', 'km_remaining', 'maint_status']].sort_values('km_remaining'),
        use_container_width=True,
        hide_index=True
    )
