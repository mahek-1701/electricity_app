import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Daily Energy Consumption Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #A23B72;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #A23B72;
        padding-bottom: 0.5rem;
    }
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .day-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .record-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing records
if 'energy_records' not in st.session_state:
    st.session_state.energy_records = []

if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = {}

# Header
st.markdown('<div class="main-header">⚡ Daily Energy Consumption Tracker</div>', unsafe_allow_html=True)

# Sidebar for user information
st.sidebar.header("👤 Personal Information")
name = st.sidebar.text_input("Enter your name:", placeholder="John Doe")
age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("Enter your city:", placeholder="Mumbai")
area = st.sidebar.text_input("Enter your area:", placeholder="Bandra")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Daily Entry", "📊 Weekly View", "📈 Analytics", "📋 Records"])

with tab1:
    st.markdown('<div class="section-header">🏠 Today\'s Energy Calculation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Date selection
        selected_date = st.date_input("Select Date", datetime.now())
        day_name = selected_date.strftime("%A")
        
        st.write(f"**Selected Day:** {day_name}, {selected_date.strftime('%B %d, %Y')}")
        
        # Housing information
        st.subheader("🏠 Housing Information")
        flat_tenament = st.selectbox(
            "Are you living in Flat or Tenement?",
            ["Select...", "Flat", "Tenement"]
        )
        
        facility = st.selectbox(
            "What type of accommodation?",
            ["Select...", "1BHK", "2BHK", "3BHK"]
        )
        
        # Appliances
        st.subheader("🔌 Appliances Usage Today")
        col_app1, col_app2, col_app3 = st.columns(3)
        
        with col_app1:
            ac = st.selectbox("Air Conditioner", ["No", "Yes"])
            if ac == "Yes":
                ac_hours = st.number_input("Hours used:", min_value=0.0, max_value=24.0, value=8.0, step=0.5, key="ac_hours")
        
        with col_app2:
            fridge = st.selectbox("Refrigerator", ["No", "Yes"])
            if fridge == "Yes":
                fridge_hours = st.number_input("Hours used:", min_value=0.0, max_value=24.0, value=24.0, step=0.5, key="fridge_hours")
        
        with col_app3:
            wm = st.selectbox("Washing Machine", ["No", "Yes"])
            if wm == "Yes":
                wm_hours = st.number_input("Hours used:", min_value=0.0, max_value=24.0, value=2.0, step=0.5, key="wm_hours")
        
        # Calculate energy
        def calculate_daily_energy(facility, ac, fridge, wm):
            cal_energy = 0
            breakdown = {}
            
            # Base consumption
            if facility == "1BHK":
                lights = 2 * 0.4
                basic = 2 * 0.8
                breakdown["Lights (2 units)"] = lights
                breakdown["Basic appliances"] = basic
                cal_energy += lights + basic
            elif facility == "2BHK":
                lights = 3 * 0.4
                basic = 3 * 0.8
                breakdown["Lights (3 units)"] = lights
                breakdown["Basic appliances"] = basic
                cal_energy += lights + basic
            elif facility == "3BHK":
                lights = 4 * 0.4
                basic = 4 * 0.8
                breakdown["Lights (4 units)"] = lights
                breakdown["Basic appliances"] = basic
                cal_energy += lights + basic
            
            # Appliances with hourly usage
            if ac == "Yes":
                ac_consumption = 3 * (ac_hours / 24)  # 3 kWh for 24 hours
                cal_energy += ac_consumption
                breakdown["Air Conditioner"] = ac_consumption
            
            if fridge == "Yes":
                fridge_consumption = 3 * (fridge_hours / 24)  # 3 kWh for 24 hours
                cal_energy += fridge_consumption
                breakdown["Refrigerator"] = fridge_consumption
            
            if wm == "Yes":
                wm_consumption = 3 * (wm_hours / 24)  # 3 kWh for 24 hours
                cal_energy += wm_consumption
                breakdown["Washing Machine"] = wm_consumption
            
            return cal_energy, breakdown
        
        # Calculate button
        if st.button("📊 Calculate Today's Energy", type="primary"):
            if facility != "Select..." and name:
                total_energy, energy_breakdown = calculate_daily_energy(facility, ac, fridge, wm)
                
                # Store the record
                record = {
                    "date": selected_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "name": name,
                    "age": age,
                    "city": city,
                    "area": area,
                    "housing": flat_tenament,
                    "facility": facility,
                    "appliances": {
                        "ac": {"used": ac, "hours": ac_hours if ac == "Yes" else 0},
                        "fridge": {"used": fridge, "hours": fridge_hours if fridge == "Yes" else 0},
                        "wm": {"used": wm, "hours": wm_hours if wm == "Yes" else 0}
                    },
                    "total_energy": total_energy,
                    "breakdown": energy_breakdown,
                    "cost": total_energy * 5
                }
                
                # Add to session state
                st.session_state.energy_records.append(record)
                st.session_state.weekly_data[day_name] = total_energy
                
                st.success(f"✅ Record saved for {day_name}!")
            else:
                st.error("Please fill in all required fields!")
    
    with col2:
        if st.session_state.energy_records:
            latest_record = st.session_state.energy_records[-1]
            
            st.markdown('<div class="section-header">📊 Today\'s Results</div>', unsafe_allow_html=True)
            
            # Energy display
            st.markdown(f"""
            <div class="energy-card">
                <h2>{latest_record['total_energy']:.2f} kWh</h2>
                <p>Total Energy Consumption</p>
                <p>Cost: ₹{latest_record['cost']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            st.subheader("Energy Breakdown")
            for appliance, energy in latest_record['breakdown'].items():
                st.write(f"**{appliance}:** {energy:.2f} kWh")

with tab2:
    st.markdown('<div class="section-header">📅 Weekly Energy Consumption</div>', unsafe_allow_html=True)
    
    if st.session_state.energy_records:
        # Create weekly summary
        weekly_summary = {}
        for record in st.session_state.energy_records:
            day = record['day']
            if day not in weekly_summary:
                weekly_summary[day] = []
            weekly_summary[day].append(record['total_energy'])
        
        # Calculate averages
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_data = []
        
        for day in days_order:
            if day in weekly_summary:
                avg_energy = sum(weekly_summary[day]) / len(weekly_summary[day])
                weekly_data.append({"Day": day, "Average Energy (kWh)": avg_energy, "Records": len(weekly_summary[day])})
            else:
                weekly_data.append({"Day": day, "Average Energy (kWh)": 0, "Records": 0})
        
        # Display weekly cards
        col1, col2 = st.columns(2)
        
        for i, day_data in enumerate(weekly_data):
            with col1 if i % 2 == 0 else col2:
                color = "#28a745" if day_data["Records"] > 0 else "#6c757d"
                st.markdown(f"""
                <div class="day-card" style="border-left-color: {color};">
                    <h4>{day_data['Day']}</h4>
                    <p><strong>Avg Energy:</strong> {day_data['Average Energy (kWh)']:.2f} kWh</p>
                    <p><strong>Records:</strong> {day_data['Records']}</p>
                    <p><strong>Avg Cost:</strong> ₹{day_data['Average Energy (kWh)'] * 5:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Weekly chart
        if any(d["Records"] > 0 for d in weekly_data):
            df_week = pd.DataFrame(weekly_data)
            fig_weekly = px.bar(
                df_week, 
                x="Day", 
                y="Average Energy (kWh)",
                title="Weekly Energy Consumption Pattern",
                color="Average Energy (kWh)",
                color_continuous_scale="viridis"
            )
            fig_weekly.update_layout(height=400)
            st.plotly_chart(fig_weekly, use_container_width=True)
    else:
        st.info("No records yet. Add some daily entries to see weekly patterns!")

with tab3:
    st.markdown('<div class="section-header">📈 Energy Analytics</div>', unsafe_allow_html=True)
    
    if st.session_state.energy_records:
        # Convert to DataFrame
        df_records = pd.DataFrame(st.session_state.energy_records)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Energy consumption over time
            fig_timeline = px.line(
                df_records, 
                x="date", 
                y="total_energy",
                title="Energy Consumption Timeline",
                markers=True
            )
            fig_timeline.update_layout(height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Average by day of week
            day_avg = df_records.groupby('day')['total_energy'].mean().reset_index()
            fig_day_avg = px.bar(
                day_avg,
                x="day",
                y="total_energy",
                title="Average Energy by Day of Week",
                color="total_energy",
                color_continuous_scale="plasma"
            )
            fig_day_avg.update_layout(height=400)
            st.plotly_chart(fig_day_avg, use_container_width=True)
        
        with col2:
            # Energy by housing type
            if len(df_records['facility'].unique()) > 1:
                facility_avg = df_records.groupby('facility')['total_energy'].mean().reset_index()
                fig_facility = px.pie(
                    facility_avg,
                    values="total_energy",
                    names="facility",
                    title="Energy Distribution by Housing Type"
                )
                st.plotly_chart(fig_facility, use_container_width=True)
            
            # Monthly cost projection
            if len(df_records) > 0:
                avg_daily = df_records['total_energy'].mean()
                monthly_projection = avg_daily * 30
                yearly_projection = avg_daily * 365
                
                st.markdown("### 💰 Cost Projections")
                st.metric("Daily Average", f"{avg_daily:.2f} kWh", f"₹{avg_daily * 5:.2f}")
                st.metric("Monthly Projection", f"{monthly_projection:.2f} kWh", f"₹{monthly_projection * 5:.2f}")
                st.metric("Yearly Projection", f"{yearly_projection:.2f} kWh", f"₹{yearly_projection * 5:.2f}")
    else:
        st.info("No data available for analytics. Add some records first!")

with tab4:
    st.markdown('<div class="section-header">📋 All Records</div>', unsafe_allow_html=True)
    
    if st.session_state.energy_records:
        # Display options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear All Records"):
                st.session_state.energy_records = []
                st.session_state.weekly_data = {}
                st.rerun()
        
        with col2:
            if st.button("📥 Download Records"):
                df_download = pd.DataFrame(st.session_state.energy_records)
                csv = df_download.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"energy_records_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            st.write(f"**Total Records:** {len(st.session_state.energy_records)}")
        
        # Display records
        st.subheader("Recent Records")
        for i, record in enumerate(reversed(st.session_state.energy_records[-10:])):  # Show last 10
            with st.expander(f"📅 {record['day']} - {record['date']} ({record['total_energy']:.2f} kWh)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {record['name']}")
                    st.write(f"**Location:** {record['city']}, {record['area']}")
                    st.write(f"**Housing:** {record['housing']} - {record['facility']}")
                
                with col2:
                    st.write(f"**Total Energy:** {record['total_energy']:.2f} kWh")
                    st.write(f"**Total Cost:** ₹{record['cost']:.2f}")
                    
                    appliances_used = []
                    for app, details in record['appliances'].items():
                        if details['used'] == 'Yes':
                            appliances_used.append(f"{app.upper()} ({details['hours']}h)")
                    
                    st.write(f"**Appliances:** {', '.join(appliances_used) if appliances_used else 'None'}")
                
                # Breakdown
                st.write("**Energy Breakdown:**")
                for appliance, energy in record['breakdown'].items():
                    st.write(f"- {appliance}: {energy:.2f} kWh")
        
        # Summary statistics
        if len(st.session_state.energy_records) > 1:
            st.subheader("📊 Summary Statistics")
            df_summary = pd.DataFrame(st.session_state.energy_records)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(st.session_state.energy_records))
            
            with col2:
                st.metric("Average Daily", f"{df_summary['total_energy'].mean():.2f} kWh")
            
            with col3:
                st.metric("Highest Day", f"{df_summary['total_energy'].max():.2f} kWh")
            
            with col4:
                st.metric("Lowest Day", f"{df_summary['total_energy'].min():.2f} kWh")
    else:
        st.info("No records available. Start by adding your first daily entry!")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; margin-top: 2rem;">⚡ Daily Energy Tracker | Track your consumption day by day</div>',
    unsafe_allow_html=True
)