import streamlit as st
import pandas as pd
import plotly.express as px
import gdown


# Download the dataset from Google Drive
file_id = '1fC6ULmOHcKezv63dLHW0jqlOJh3FvbCM'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
output = 'data.csv'
gdown.download(url, output, quiet=False)

df = pd.read_csv(output)
st.set_page_config(page_title="Company Sales and Profitability Dashboard", layout="wide")

# Sidebar Filters (Global)
st.sidebar.header('Filters')

# Global Year Filter
year_filter = st.sidebar.selectbox(
    'Select Year',
    options=['All'] + list(df['year'].unique()),
    index=0  # Default to 'All'
)

# Global Product Filter
product_filter = st.sidebar.multiselect(
    'Select Product(s)',
    options=['All'] + list(df['product_name'].unique()),
    default=['All']  # Default to all products selected
)

# Filter the data based on global selections
filtered_df = df.copy()

# Apply global filters
if year_filter != 'All':
    filtered_df = filtered_df[filtered_df['year'] == year_filter]

if 'All' not in product_filter:
    filtered_df = filtered_df[filtered_df['product_name'].isin(product_filter)]

background_image_url = "https://images.pexels.com/photos/269077/pexels-photo-269077.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"

# Set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            max-width: 100%;
            padding: 0;
        }
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: white;
            background-color: #FF6347;  /* Tomato color for background */
            padding: 15px;
            border-radius: 10px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .kpi-container {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            margin-top: 20px;
        }
        .kpi {
            border: 2px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            width: 22%;
            text-align: center;
            background-color: #4682B4;  /* SteelBlue background */
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Display Dashboard Title
st.markdown("""
    <h1 style="text-align: center; font-size: 1.8em; color: white; background-color: #4682B4; 
    padding: 15px; border-radius: 10px; margin-top: 10px;">
        Sales and Profitability Dashboard by Maxwell Adigwe
    </h1>
""", unsafe_allow_html=True)


# KPIs
total_sales = round(filtered_df['total_sales'].sum(), 2)
total_profit = round(filtered_df['net_profit'].sum(), 2)
total_discounted_sales = round(filtered_df['discounted_sales'].sum(), 2)
total_units_sold = round(filtered_df['unit_sold'].sum(), 2)

# Display KPIs
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi">
            <strong>Total Sales:</strong><br> {total_sales:,.2f}
        </div>
        <div class="kpi">
            <strong>Total Profit:</strong><br> {total_profit:,.2f}
        </div>
        <div class="kpi">
            <strong>Total Discounted Sales:</strong><br> {total_discounted_sales:,.2f}
        </div>
        <div class="kpi">
            <strong>Total Units Sold:</strong><br> {total_units_sold}
        </div>
    </div>
""", unsafe_allow_html=True)

# First Row: Visualizations
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Individual Filter for Profit Margin Plot
    product_filter_profit_margin = st.selectbox(
        'Select Product for Profit Margin Plot',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df1 = filtered_df.copy()
    if product_filter_profit_margin != 'All':
        plot_filtered_df1 = plot_filtered_df1[plot_filtered_df1['product_name'] == product_filter_profit_margin]
    
    fig2 = px.bar(plot_filtered_df1, x='product_name', y='profit_margin (%)', title="Profit Margin by Product", labels={"product_name": "Product", "profit_margin (%)": "Profit Margin (%)"}, color_discrete_sequence=['#32CD32'])  # LimeGreen
    st.plotly_chart(fig2)

with col2:
    # Individual Filter for Sales vs Temperature Plot
    year_filter_temp = st.selectbox(
        'Select Year for Sales vs Temperature',
        options=['All'] + list(filtered_df['year'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df2 = filtered_df.copy()
    if year_filter_temp != 'All':
        plot_filtered_df2 = plot_filtered_df2[plot_filtered_df2['year'] == year_filter_temp]

    plot_filtered_df2['temperature'] = plot_filtered_df2['temperature'].round()
    temp_sales = plot_filtered_df2.groupby('temperature')['total_sales'].mean().reset_index()
    fig3 = px.line(temp_sales, x='temperature', y='total_sales', title="Sales vs Temperature", labels={"temperature": "Temperature", "total_sales": "Total Sales"}, line_shape="linear", markers=True, color_discrete_sequence=['#1E90FF'])  # DodgerBlue
    st.plotly_chart(fig3)

with col3:
    # Individual Filter for Net Profit by Product Plot
    product_filter_net_profit = st.selectbox(
        'Select Product for Net Profit Plot',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df3 = filtered_df.copy()
    if product_filter_net_profit != 'All':
        plot_filtered_df3 = plot_filtered_df3[plot_filtered_df3['product_name'] == product_filter_net_profit]
    
    fig4 = px.bar(plot_filtered_df3, x='product_name', y='net_profit', title="Net Profit by Product", labels={"product_name": "Product", "net_profit": "Net Profit"}, color_discrete_sequence=['#FF6347'])  # Tomato
    st.plotly_chart(fig4)

with col4:
    # Individual Filter for Discounted vs Non-Discounted Sales Plot
    product_filter_sales = st.selectbox(
        'Select Product for Discounted vs Non-Discounted Sales',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df4 = filtered_df.copy()
    if product_filter_sales != 'All':
        plot_filtered_df4 = plot_filtered_df4[plot_filtered_df4['product_name'] == product_filter_sales]
    
    plot_filtered_df4['discounted_sales'] = plot_filtered_df4['total_sales'].where(plot_filtered_df4['discount'] > 0, 0)
    plot_filtered_df4['non_discounted_sales'] = plot_filtered_df4['total_sales'].where(plot_filtered_df4['discount'] == 0, 0)
    yearly_sales = plot_filtered_df4.groupby('year')[['discounted_sales', 'non_discounted_sales']].sum().reset_index()
    fig = px.line(yearly_sales, x='year', y=['discounted_sales', 'non_discounted_sales'], title='Yearly Sales: Discounted vs Non-Discounted', labels={'year': 'Year', 'value': 'Total Sales'}, markers=True, color_discrete_sequence=['#8A2BE2', '#FF1493'])  # BlueViolet, DeepPink
    fig.update_layout(legend_title="Sales Type", template='plotly_white', xaxis_title="Year", yaxis_title="Total Sales")
    st.plotly_chart(fig)

# Second Row: Visualizations
col5, col6, col7, col8 = st.columns(4)

with col5:
    temp_sales_sorted = temp_sales.sort_values(by='total_sales', ascending=False)
    temperature_filter = st.selectbox(
        'Select Temperature Range for Sales',
        options=['All'] + list(temp_sales_sorted['temperature'].unique()),  
        index=0  # Default to 'All'
    )
    
    # Apply temperature filter if selected
    temp_sales_filtered = temp_sales_sorted.copy()
    if temperature_filter != 'All':
        temp_sales_filtered = temp_sales_filtered[temp_sales_filtered['temperature'] == temperature_filter]
    
    # Create the bar chart for average sales by temperature
    fig5 = px.bar(temp_sales_filtered, x='temperature', y='total_sales', 
                  title='Average Sales by Temperature', 
                  labels={'temperature': 'Temperature', 'total_sales': 'Average Sales'})
    
    st.plotly_chart(fig5)

with col6:
    # Individual Filter for Sales by Day of the Week Plot
    day_filter = st.selectbox(
        'Select Day for Sales by Day of the Week',
        options=['All'] + list(filtered_df['day'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df6 = filtered_df.copy()
    if day_filter != 'All':
        plot_filtered_df6 = plot_filtered_df6[plot_filtered_df6['day'] == day_filter]
    
    day_sales = plot_filtered_df6.groupby('day')['total_sales'].sum().reset_index()
    day_sales['day'] = pd.Categorical(day_sales['day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
    day_sales = day_sales.sort_values('day')
    fig1 = px.line(day_sales, x='day', y='total_sales', title="Sales by Day of the Week", labels={'day': 'Day of the Week', 'total_sales': 'Total Sales'}, markers=True, line_shape="linear", color_discrete_sequence=['#FFD700'])  # Gold
    st.plotly_chart(fig1)

with col7:
    # Profit Margin by Day Filter
    profit_margin_day_filter = st.selectbox(
        'Select Day for Profit Margin by Day',
        options=['All'] + list(filtered_df['day'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df7 = filtered_df.copy()
    if profit_margin_day_filter != 'All':
        plot_filtered_df7 = plot_filtered_df7[plot_filtered_df7['day'] == profit_margin_day_filter]
    
    profit_margin_day = plot_filtered_df7.groupby('day')['profit_margin (%)'].mean().reset_index()
    profit_margin_day['day'] = pd.Categorical(profit_margin_day['day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
    fig7 = px.line(profit_margin_day, x='day', y='profit_margin (%)', title="Profit Margin by Day", labels={'day': 'Day of the Week', 'profit_margin (%)': 'Profit Margin (%)'}, markers=True, line_shape="linear", color_discrete_sequence=['#20B2AA'])  # LightSeaGreen
    st.plotly_chart(fig7)

with col8:
    # Scatter Plot Filter for Revenue vs Units Sold
    product_filter_scatter = st.selectbox(
        'Select Product for Revenue vs Units Sold',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df8 = filtered_df.copy()
    if product_filter_scatter != 'All':
        plot_filtered_df8 = plot_filtered_df8[plot_filtered_df8['product_name'] == product_filter_scatter]
    
    fig8 = px.scatter(plot_filtered_df8, x='unit_sold', y='total_sales', title="Revenue vs Units Sold", labels={"unit_sold": "Units Sold", "total_sales": "Revenue"}, color_discrete_sequence=['#DC143C'])  # Crimson
    st.plotly_chart(fig8)

col9, col10, col11, col12 = st.columns(4)

with col9:
    sales_by_product = df.groupby('product_name')['total_sales'].sum().reset_index()
    fig9 = px.bar(sales_by_product, x='product_name', y='total_sales', title="Sales by Product", labels={"product_name": "Product", "total_sales": "Total Sales"}, color_discrete_sequence=['#8B0000'])  # DarkRed
    st.plotly_chart(fig9)

with col10:
    product_profit = df.groupby('product_name')[['net_profit', 'profit_margin (%)']].mean().reset_index()
    fig7 = px.bar(product_profit, x='product_name', y=['net_profit', 'profit_margin (%)'], title="Average Profit and Profit Margin by Product", labels={'product_name': 'Product Name', 'value': 'Values'}, barmode='group', color_discrete_map={'net_profit': '#4682B4', 'profit_margin (%)': '#32CD32'})  # SteelBlue, LimeGreen
    fig7.update_layout(xaxis_title='Product Name', yaxis_title='Values', legend_title_text='Metrics', margin=dict(t=40, b=40))
    st.plotly_chart(fig7)

with col11:
    units_by_product = df.groupby('product_name')['unit_sold'].sum().reset_index()
    fig11 = px.pie(units_by_product, names='product_name', values='unit_sold', title="Units Sold by Product", labels={"product_name": "Product", "unit_sold": "Units Sold"}, hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig11)

with col12:
    sales_by_month = df.groupby('month')['total_sales'].sum().reset_index()
    fig12 = px.bar(sales_by_month, x='month', y='total_sales', title="Sales by Month", labels={'month': 'Month', 'total_sales': 'Total Sales'}, color_discrete_sequence=['#20B2AA'])  # LightSeaGreen
    st.plotly_chart(fig12)



col13, col14, col15, col16 = st.columns(4)

with col13:
    # Individual Filter for Seasonality by Product Plot
    product_filter_seasonality = st.selectbox(
        'Select Product for Seasonality Plot',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df13 = filtered_df.copy()
    if product_filter_seasonality != 'All':
        plot_filtered_df13 = plot_filtered_df13[plot_filtered_df13['product_name'] == product_filter_seasonality]
    
    seasonality_product = plot_filtered_df13.groupby(['month', 'product_name'])['total_sales'].sum().unstack()
    fig13 = px.imshow(seasonality_product, labels={'x': 'Product Name', 'y': 'Month', 'color': 'Total Sales'}, title="Seasonality by Product", color_continuous_scale='YlGnBu')
    st.plotly_chart(fig13)

with col14:
    # Individual Filter for Promotion Sales Plot
    promotion_filter = st.selectbox(
        'Select Promotion for Sales Plot',
        options=['All'] + list(filtered_df['promotion'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df14 = filtered_df.copy()
    if promotion_filter != 'All':
        plot_filtered_df14 = plot_filtered_df14[plot_filtered_df14['promotion'] == promotion_filter]
    
    promotion_sales = plot_filtered_df14.groupby('promotion')['total_sales'].mean().reset_index()
    fig14 = px.pie(promotion_sales, values='total_sales', names='promotion', title="Average Sales with and without Promotions", labels={"promotion": "Promotion Applied ( No,  Yes)", "total_sales": "Average Total Sales"}, hole=0.4, color_discrete_sequence=['#FF1493', '#00FA9A'])  # DeepPink, MediumSpringGreen
    fig14.update_traces(textinfo='percent+value')
    st.plotly_chart(fig14)

with col15:
    # Individual Filter for Monthly Sales Comparison by Product Plot
    product_filter_monthly_comparison = st.selectbox(
        'Select Product for Monthly Sales Comparison',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df15 = filtered_df.copy()
    if product_filter_monthly_comparison != 'All':
        plot_filtered_df15 = plot_filtered_df15[plot_filtered_df15['product_name'] == product_filter_monthly_comparison]
    
    monthly_comparison = plot_filtered_df15.groupby(['month', 'product_name'])['total_sales'].sum().unstack()
    fig15 = px.bar(monthly_comparison, 
                   x=monthly_comparison.index, 
                   y=monthly_comparison.columns,
                   title="Monthly Sales Comparison by Product",
                   labels={'x': 'Month', 'value': 'Total Sales', 'variable': 'Product'},
                   barmode='group')
    st.plotly_chart(fig15)

with col16:
    # Individual Filter for Yearly Sales Comparison by Product Plot
    product_filter_yearly_comparison = st.selectbox(
        'Select Product for Yearly Sales Comparison',
        options=['All'] + list(filtered_df['product_name'].unique()),
        index=0  # Default to 'All'
    )
    plot_filtered_df16 = filtered_df.copy()
    if product_filter_yearly_comparison != 'All':
        plot_filtered_df16 = plot_filtered_df16[plot_filtered_df16['product_name'] == product_filter_yearly_comparison]
    
    yearly_comparison = plot_filtered_df16.groupby(['year', 'product_name'])['total_sales'].sum().unstack()
    fig16 = px.bar(yearly_comparison, 
                   x=yearly_comparison.index, 
                   y=yearly_comparison.columns,
                   title="Yearly Sales Comparison by Product",
                   labels={'x': 'Year', 'value': 'Total Sales', 'variable': 'Product'},
                   barmode='group')
    st.plotly_chart(fig16)
