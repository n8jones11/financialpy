import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- Configuration & Constants ---
# Define the impact of market events as a percentage drop (e.g., 0.10 for a 10% drop)
TARIFF_IMPACTS = {"Low": 0.05, "Medium": 0.10, "High": 0.15}
EXTREME_EVENT_IMPACTS = {"Low": 0.15, "Medium": 0.25, "High": 0.35}

# Define when the events occur in the simulation (in months)
# We'll place them at fixed points for this simulation.
TARIFF_EVENT_MONTH = 24  # 2 years in
EXTREME_EVENT_MONTH = 36 # 3 years in

# --- Core Simulation Logic ---
def run_simulation(years, monthly_deposit, annual_rate, tariff_impact_level, extreme_event_impact_level):
    """
    Calculates the growth of an investment fund over time.
    """
    total_months = years * 12
    monthly_rate = (annual_rate / 100) / 12

    # Get the impact values from the dictionaries, or 0 if not enabled
    tariff_shock = TARIFF_IMPACTS.get(tariff_impact_level, 0)
    extreme_event_shock = EXTREME_EVENT_IMPACTS.get(extreme_event_impact_level, 0)

    # Initialize lists to store monthly data for the chart
    dates = []
    fund_values = []
    accumulated_deposits_list = []

    # Set initial values
    current_fund_value = 0
    total_deposits = 0
    start_date = datetime.now()

    for month in range(1, total_months + 1):
        # 1. Add this month's deposit
        current_fund_value += monthly_deposit
        total_deposits += monthly_deposit

        # 2. Calculate and add compound interest for the month
        interest_earned = current_fund_value * monthly_rate
        current_fund_value += interest_earned

        # 3. Apply market event shocks if they occur in the current month
        if tariff_shock > 0 and month == TARIFF_EVENT_MONTH:
            current_fund_value *= (1 - tariff_shock)
        
        if extreme_event_shock > 0 and month == EXTREME_EVENT_MONTH:
            current_fund_value *= (1 - extreme_event_shock)
            
        # Ensure fund value doesn't go below zero
        if current_fund_value < 0:
            current_fund_value = 0

        # Store results for this month
        current_date = start_date + relativedelta(months=month)
        dates.append(current_date)
        fund_values.append(current_fund_value)
        accumulated_deposits_list.append(total_deposits)

    # Create a DataFrame for easy plotting
    results_df = pd.DataFrame({
        'Date': dates,
        'Accumulated Deposits': accumulated_deposits_list,
        'Fund Value with Growth': fund_values
    })

    return total_deposits, current_fund_value, results_df

# --- Streamlit Web Application UI ---

st.set_page_config(layout="wide")

st.title("Investment Fund Growth Simulator")

st.markdown("""
This application simulates the growth of an investment fund over time. 
Adjust the parameters in the sidebar to see how different factors like monthly deposits, 
interest rates, and simulated market events can impact your final fund value.
""")

# --- Sidebar for User Inputs ---
st.sidebar.header("Simulation Parameters")

# Input 1: Investment Period
years = st.sidebar.slider(
    "Investment Period (Years)", 
    min_value=1, 
    max_value=50, 
    value=20, 
    step=1
)

# Input 2: Monthly Deposit
monthly_deposit = st.sidebar.number_input(
    "Monthly Deposit (£)",
    min_value=0,
    max_value=10000,
    value=500,
    step=50
)

# Input 3: Annual Interest Rate
annual_rate = st.sidebar.slider(
    "Variable Annual Interest Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=7.0,
    step=0.5,
    format="%.1f%%"
)

st.sidebar.markdown("---")
st.sidebar.header("Market Event Simulation")

# Event 1: Tariff Impact
enable_tariff = st.sidebar.checkbox('Simulate "Tariff Impact" Event (at Year 2)')
tariff_variance = "None"
if enable_tariff:
    tariff_variance = st.sidebar.select_slider(
        "Tariff Impact Severity",
        options=["Low", "Medium", "High"],
        value="Medium"
    )

# Event 2: Extreme Event
enable_extreme = st.sidebar.checkbox('Simulate "Extreme" Event (at Year 3)')
extreme_variance = "None"
if enable_extreme:
    extreme_variance = st.sidebar.select_slider(
        "Extreme Event Severity",
        options=["Low", "Medium", "High"],
        value="Medium"
    )

# --- Main Page for Results ---

if st.sidebar.button("Run Simulation", type="primary"):
    # Determine which impact levels to pass to the simulation function
    tariff_level = tariff_variance if enable_tariff else None
    extreme_level = extreme_variance if enable_extreme else None
    
    # Run the simulation
    final_deposits, final_value, results_df = run_simulation(
        years, 
        monthly_deposit, 
        annual_rate, 
        tariff_level, 
        extreme_level
    )
    
    st.header("Simulation Results")
    
    # Display final numbers in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Accumulated Deposits",
            value=f"£{final_deposits:,.2f}"
        )
    with col2:
        st.metric(
            label="Final Fund Value (with Growth & Events)",
            value=f"£{final_value:,.2f}",
            delta=f"£{final_value - final_deposits:,.2f} in growth"
        )
        
    st.markdown("---")
    
    # --- Data Visualization ---
    st.header("Fund Growth Over Time")
    
    fig = go.Figure()

    # Line 1: Accumulated Deposits
    fig.add_trace(go.Scatter(
        x=results_df['Date'],
        y=results_df['Accumulated Deposits'],
        mode='lines',
        name='Accumulated Deposits (No Interest)',
        line=dict(color='royalblue', dash='dash')
    ))

    # Line 2: Fund Value with Growth
    fig.add_trace(go.Scatter(
        x=results_df['Date'],
        y=results_df['Fund Value with Growth'],
        mode='lines',
        name='Fund Value (with Interest & Events)',
        line=dict(color='firebrick', width=3)
    ))
    
    # Add annotations for market events
    if enable_tariff:
        event_date = results_df['Date'][TARIFF_EVENT_MONTH - 1]
        fig.add_vline(x=event_date, line_width=1, line_dash="dash", line_color="grey")
        fig.add_annotation(x=event_date, y=results_df['Fund Value with Growth'].max(), text="Tariff Event", showarrow=False, yshift=10)
        
    if enable_extreme:
        event_date = results_df['Date'][EXTREME_EVENT_MONTH - 1]
        fig.add_vline(x=event_date, line_width=1, line_dash="dash", line_color="grey")
        fig.add_annotation(x=event_date, y=results_df['Fund Value with Growth'].max(), text="Extreme Event", showarrow=False, yshift=10)


    fig.update_layout(
        title_text='Investment Growth vs. Deposits Over Time',
        xaxis_title='Date',
        yaxis_title='Fund Value (£)',
        legend_title='Legend',
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info('Adjust the parameters in the sidebar and click "Run Simulation" to see the results.')