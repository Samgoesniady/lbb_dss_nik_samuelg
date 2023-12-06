import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout='wide')

# --- READ DATA ---
customer_merge = pd.read_pickle('data/customer_merge.pkl')
coord = pd.read_csv('data/coordinate.csv')

# --- ROW 1 ---
st.write('# Customer Demography Dashboard')
st.write("""Explore dynamics customer behavior at a glance with this Customer Demography Dashboard. 
         Track history trends over time, visualize customer distribution across provinces, 
         and delve into generational and gender insights within Professions—all in one comprehensive view.""")


# --- ROW 3 ---
col6, col7 = st.columns(2)

## --- BAR PLOT ---

# data: Bar plot
dept = pd.crosstab(index=customer_merge['Profession'],
                   columns='Jumlah Customer',
                   colnames=[None])
dept = dept.reset_index()

# plot: Bar plot
plot_dept = px.bar(data_frame=dept, x = 'Profession', y='Jumlah Customer',
                  labels={'Profession': 'Profession',
                          'Jumlah Customer':'Customer Count'}, color = 'Profession')

col6.write('### Customer Professions Frequency')
col6.plotly_chart(plot_dept, use_container_width=True)

## --- MAP PLOT ---
# data: map
prov_gender = pd.crosstab(index=customer_merge['province'],
                        columns=customer_merge['gender'], colnames=[None])
prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']
df_map = prov_gender.merge(coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             color = 'Total',
                             hover_name='province',
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False})

col7.write('### Customer Count across Indonesia')
col7.plotly_chart(plot_map, use_container_width=True)

# --- ROW 3 ---
st.divider()
col8, col9 = st.columns(2)

## --- INPUT SELECT ---
input_select = col8.selectbox(
    label='Select Profession',
    options=customer_merge['Profession'].unique().sort_values()
)

## --- INPUT SLIDER ---
input_slider = col9.slider(
    label='Select age range',
    min_value=customer_merge['age'].min(),
    max_value=customer_merge['age'].max(),
    value=[20,50]
)

min_slider = input_slider[0]
max_slider = input_slider[1]

# --- ROW 4 ---
col10, col11 = st.columns(2)

## --- BARPLOT ---
# data: barplot
customer_artist = customer_merge[customer_merge['Profession'] == input_select]
df_gen = pd.crosstab(index=customer_artist['generation'], columns='num_people', colnames=[None])
df_gen = df_gen.reset_index()

# plot: barplot
plot_gen = px.bar(df_gen, x='generation', y='num_people', 
                   labels = {'generation' : 'Generation',
                             'num_people' : 'Employee Count'})

col10.write(f'### Customer Count per Generation in {input_select} Profession.') # f-string
col10.plotly_chart(plot_gen, use_container_width=True)

## --- MULTIVARIATE ---
# data: multivariate
cust_age = customer_merge[customer_merge['age'].between(left=min_slider, right=max_slider)]
dept_gender = pd.crosstab(index=cust_age['Profession'],
                          columns=cust_age['gender'],
                          colnames=[None])
dept_gender_melt = dept_gender.melt(ignore_index=False, var_name='gender', value_name='num_people')
dept_gender_melt = dept_gender_melt.reset_index()

# plot: multivariate
plot_dept = px.bar(dept_gender_melt.sort_values(by='num_people'), 
                   x="num_people", y="Profession", 
                   color="gender", 
                   barmode='group',
                   labels = {'num_people' : 'Customer Count',
                             'Profession' : 'Profession',
                             'gender': 'Gender'}
                             )

col11.write(f'### Gender per Profession, Age {min_slider} to {max_slider}')
col11.plotly_chart(plot_dept, use_container_width=True)

# Row 5
st.divider()
col12, col13 = st.columns(2)

plot_corr = px.scatter(data_frame=customer_merge, x = customer_merge['Spending_Score'], 
                        y = customer_merge['Annual_Income'], color = customer_merge['Spending_Score'], 
                        labels = {'Annual_Income':'Customer Income', 'Spending_Score':'Spending Score'})

col12.write('### Customer Income & Spending Score Correlation')
col12.plotly_chart(plot_corr, use_container_width=True)

plot_dist = px.histogram(customer_merge, x = customer_merge['Annual_Income'], nbins = 20, 
                        labels = {'Annual_Income':'Customer Income'})

col13.write('### Customer Income Histogram')
col13.plotly_chart(plot_dist, use_container_width=True)