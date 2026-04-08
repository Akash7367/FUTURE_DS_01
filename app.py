import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Business Sales Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Dark Theme & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium aesthetics */
    .stApp {
        background-color: #0f1115;
    }
    
    /* Style metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700;
        color: #ffffff;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        color: #a0aec0;
        font-weight: 600;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f7fafc;
    }
    
    /* Adjust Tab text */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
        color: #cbd5e0;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #63b3ed;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a202c;
        border-right: 1px solid #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(show_spinner="Loading data...")
def load_data():
    file_path = "data/online_retail_cleaned.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Dataset not found at {file_path}. Please ensure it is downloaded and placed correctly.")
        st.stop()
        
    # Convert dates
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Feature Engineering
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Hour'] = df['InvoiceDate'].dt.hour
    df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
    
    # Identify Returns
    df['IsReturn'] = df['InvoiceNo'].astype(str).str.startswith('C')
    
    # Estimate Profit (assuming 20% margin on revenue for non-returns)
    df['EstimatedProfit'] = df['Revenue'] * 0.20
    
    return df

df_raw = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("## 🔍 Filters")

# Date range
min_date = df_raw['InvoiceDate'].min().date()
max_date = df_raw['InvoiceDate'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
if len(date_range) == 2:
    start_date, end_date = date_range
elif len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date, end_date = min_date, max_date

# Country Filter
all_countries = sorted(df_raw['Country'].unique())
selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=[])

# Apply filters
df = df_raw[
    (df_raw['InvoiceDate'].dt.date >= start_date) & 
    (df_raw['InvoiceDate'].dt.date <= end_date)
]
if selected_countries:
    df = df[df['Country'].isin(selected_countries)]

# --- CURRENCY CONVERSION ---
currency_map = {
    'United Kingdom': ('£', 1.0),
    'France': ('€', 1.17),
    'Germany': ('€', 1.17),
    'EIRE': ('€', 1.17),
    'Spain': ('€', 1.17),
    'Netherlands': ('€', 1.17),
    'Belgium': ('€', 1.17),
    'Italy': ('€', 1.17),
    'Portugal': ('€', 1.17),
    'Austria': ('€', 1.17),
    'Finland': ('€', 1.17),
    'Cyprus': ('€', 1.17),
    'Greece': ('€', 1.17),
    'Australia': ('A$', 1.93),
    'USA': ('$', 1.26),
    'Switzerland': ('CHF', 1.14),
    'Japan': ('¥', 190.0),
    'Sweden': ('SEK', 13.5),
    'Norway': ('NOK', 13.5),
    'Denmark': ('DKK', 8.7),
    'Singapore': ('S$', 1.70),
    'Israel': ('₪', 4.7),
    'Hong Kong': ('HK$', 9.8),
    'Canada': ('C$', 1.7),
    'Poland': ('PLN', 5.0),
    'United Arab Emirates': ('AED', 4.6),
    'Saudi Arabia': ('SAR', 4.7),
}

if len(selected_countries) == 1:
    disp_sym, disp_rate = currency_map.get(selected_countries[0], ('£', 1.0))
else:
    disp_sym, disp_rate = ('£', 1.0)

# Separate sales and returns for certain views
df_sales = df[~df['IsReturn']].copy()
df_returns = df[df['IsReturn']].copy()

if disp_rate != 1.0:
    df_sales['Revenue'] = df_sales['Revenue'] * disp_rate
    df_sales['EstimatedProfit'] = df_sales['EstimatedProfit'] * disp_rate
    df_returns['Revenue'] = df_returns['Revenue'] * disp_rate
    df_returns['EstimatedProfit'] = df_returns['EstimatedProfit'] * disp_rate

# --- MAIN DASHBOARD AREA ---
st.title("📈 Business Sales Performance Dashboard")
st.markdown("Analyze business performance, product trends, and international reach.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⏳ Sales Trends", "🛒 Customer & Product", "💡 Business Insights"])

# Dark chart template
plotly_template = "plotly_dark"

with tab1:
    st.header("High-Level Performance KPIs")
    
    # KPIS
    total_revenue = df_sales['Revenue'].sum()
    total_orders = df_sales['InvoiceNo'].nunique()
    total_items = df_sales['Quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"{disp_sym}{total_revenue:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"{disp_sym}{avg_order_value:,.2f}")
    col4.metric("Items Sold", f"{total_items:,}")
    
    st.divider()
    
    st.subheader("🌍 Top 10 Countries by Revenue")
    country_rev = df_sales.groupby('Country')['Revenue'].sum().reset_index()
    country_rev = country_rev.sort_values('Revenue', ascending=False).head(10)
    
    fig_geo = px.bar(
        country_rev, x='Revenue', y='Country', 
        orientation='h', 
        color='Revenue', 
        color_continuous_scale='Blues',
        text_auto='.2s'
    )
    fig_geo.update_layout(template=plotly_template, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_geo, use_container_width=True)

with tab2:
    st.header("Sales Trends Over Time")
    
    col_t1, col_t2 = st.columns([3, 2])
    
    with col_t1:
        st.subheader("Monthly Revenue & Estimated Profit")
        monthly_trend = df_sales.groupby('YearMonth')[['Revenue', 'EstimatedProfit']].sum().reset_index()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=monthly_trend['YearMonth'], y=monthly_trend['Revenue'], mode='lines+markers', name='Revenue', line=dict(color='#63b3ed', width=3)))
        fig_trend.add_trace(go.Scatter(x=monthly_trend['YearMonth'], y=monthly_trend['EstimatedProfit'], mode='lines+markers', name='Est. Profit', line=dict(color='#4fd1c5', width=3, dash='dot')))
        fig_trend.update_layout(template=plotly_template, xaxis_title="Month", yaxis_title=f"Amount ({disp_sym})", hovermode='x unified', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        st.subheader("Revenue Heatmap (Day vs. Hour)")
        heatmap_data = df_sales.groupby(['DayOfWeek', 'Hour'])['Revenue'].sum().reset_index()
        # Order days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_data.pivot(index='DayOfWeek', columns='Hour', values='Revenue').reindex(days_order)
        
        fig_heat = px.imshow(
            heatmap_pivot, 
            labels=dict(x="Hour of Day", y="Day of Week", color="Revenue"),
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            color_continuous_scale='Purples',
            aspect="auto"
        )
        fig_heat.update_layout(template=plotly_template, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.header("Customer & Product Analytics")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("🏆 Top 10 Products by Revenue")
        prod_rev = df_sales.groupby('Description')['Revenue'].sum().reset_index()
        prod_rev = prod_rev.sort_values('Revenue', ascending=False).head(10)
        
        fig_prod = px.bar(
            prod_rev, x='Revenue', y='Description', 
            orientation='h', 
            color='Revenue', 
            color_continuous_scale='Tealgrn',
            text_auto='.2s'
        )
        fig_prod.update_layout(template=plotly_template, yaxis={'categoryorder':'total ascending', 'title': ''}, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col_c2:
        st.subheader("📉 Impact of Returns")
        rev_gained = df_sales['Revenue'].sum()
        rev_lost = abs(df_returns['Revenue'].sum())
        
        pie_data = pd.DataFrame({
            'Category': ['Completed Revenue', 'Lost to Returns'],
            'Value': [rev_gained, rev_lost]
        })
        
        fig_pie = px.pie(pie_data, names='Category', values='Value', hole=0.4, color='Category', color_discrete_map={'Completed Revenue':'#4fd1c5', 'Lost to Returns':'#fc8181'})
        fig_pie.update_layout(template=plotly_template, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.divider()
    st.subheader("💸 Order Value Distribution")
    order_vals = df_sales.groupby('InvoiceNo')['Revenue'].sum().reset_index()
    # Filter extreme outliers for better visualization (e.g. 99th percentile)
    if not order_vals.empty:
        p99 = order_vals['Revenue'].quantile(0.99)
        order_vals_filtered = order_vals[order_vals['Revenue'] <= p99]
        
        fig_hist = px.histogram(
            order_vals_filtered, x='Revenue', nbins=50, 
            color_discrete_sequence=['#9f7aea'],
            labels={'Revenue': f'Total Invoice Value ({disp_sym})'}
        )
        fig_hist.update_layout(template=plotly_template, yaxis_title="Number of Orders", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_hist, use_container_width=True)

with tab4:
    st.header("💡 Business Insights & Recommendations")
    
    st.markdown("""
    ### 1. Which products generate the most revenue?
    Based on the analysis, products like the **White Hanging Heart T-Light Holder** and **DOTCOM POSTAGE** generally top the revenue charts. 
    *Recommendation*: Ensure consistent stock levels for these top 10 best-sellers, particularly leading up to holiday seasons. Consider bundling lower-selling items with these flagship products to drive up the average order value.

    ### 2. Where should the business focus to grow faster?
    The **United Kingdom** vastly dominates total volume, but looking at top international markets (like **Netherlands, EIRE, Germany, and France**), there is significant traction.
    *Recommendation*: To grow faster, expand targeted marketing campaigns in these highly profitable European countries. Localized promotions or optimized international shipping rates could yield strong growth.

    ### 3. When are peak shopping times?
    The revenue heatmap consistently reveals strong purchasing activity around **mid-day (10 AM to 3 PM)**, particularly earlier in the week.
    *Recommendation*: Launch email marketing campaigns and flash sales heavily between 9 AM and 10 AM to catch users right as they begin their shopping habits. Ensure server capacity and customer service availability peaks during these daytime hours.

    ### 4. What is the impact of returns?
    Returns account for a notable slice of lost revenue. 
    *Recommendation*: Analyze the specific products with the highest return rates to determine if there are quality issues, sizing discrepancies, or misleading descriptions. Improving pre-purchase clarity can directly mitigate profit leakage.
    """)
