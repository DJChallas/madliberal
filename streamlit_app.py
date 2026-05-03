import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import json
from datetime import datetime

# --- Global Streamlit Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded") # Keep sidebar expanded for easier navigation

# --- Data Loading and Processing Function ---
@st.cache_data
def load_and_process_bls_data():
    headers = {'Content-type': 'application/json'}
    current_year = datetime.now().year
    data = json.dumps({
        "seriesid": [
            # Unemployment Series
            'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004',
            # Labor Force Series
            'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001', 'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',
            # Management, Professional, and Related Occupations
            'LNU02032526', 'LNU02032468', 'LNU02035886', 'LNU02035918', 'LNU02035957', 'LNU02035874',
            # Service Occupations
            'LNU02032539', 'LNU02032481', 'LNU02035042', 'LNU02035006', 'LNU02035074', 'LNU02035018',
            # Sales and Office Occupations
            'LNU02032545', 'LNU02032487', 'LNU02035941', 'LNU02035920', 'LNU02035959', 'LNU02035898',
            # Natural resources, construction, and maintenance occupations
            'LNU02032548', 'LNU02032490', 'LNU02034909', 'LNU02034877', 'LNU02034937', 'LNU02034891',
            # Production, transportation, and material moving occupations
            'LNU02032554', 'LNU02032496', 'LNU02035873', 'LNU02035897', 'LNU02035933', 'LNU02035885'
        ],
        "startyear": str(current_year - 4),
        "endyear": str(current_year),
        "registrationkey": "9dd192e92c9c4989985db57deede9647"
    })
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    all_series_data = []

    def period_to_month(period_str):
        if period_str.startswith('M'):
            return int(period_str[1:])
        elif period_str == 'Q01':
            return 1
        elif period_str == 'Q02':
            return 4
        elif period_str == 'Q03':
            return 7
        elif period_str == 'Q04':
            return 10
        return None

    df = pd.DataFrame() # Initialize df outside if/else for broader scope
    if 'Results' in json_data and 'series' in json_data['Results']:
        for series in json_data['Results']['series']:
            seriesId = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                footnotes_list = []
                for footnote in item['footnotes']:
                    if footnote:
                        footnotes_list.append(footnote['text'])
                footnotes = ','.join(footnotes_list)

                if ('M01' <= period <= 'M12') or ('Q01' <= period <= 'Q04'):
                    all_series_data.append({
                        'series_id': seriesId,
                        'year': year,
                        'period': period,
                        'value': value,
                        'footnotes': footnotes
                    })
        df = pd.DataFrame(all_series_data)
        df['month'] = df['period'].apply(period_to_month)
        df = df.dropna(subset=['month'])
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(int).astype(str) + '-01')
        df = df.drop(columns=['month'])

    # Data Cleaning and value conversion based on series type
    if not df.empty:
        # Convert 'value' to numeric, coercing errors
        df['value'] = pd.to_numeric(df['value'].astype(str).replace(r'\s+\(\d+\)', '', regex=True), errors='coerce')

        # Apply division by 100 only for Unemployment series (which are proportions)
        unemployment_series_ids = [
            'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183',
            'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004'
        ]
        df.loc[df['series_id'].isin(unemployment_series_ids), 'value'] = df.loc[df['series_id'].isin(unemployment_series_ids), 'value'] / 100

        df_filtered = df.dropna(subset=['value']).copy()

        sn_map = {
            # Unemployment Series
            'LNS14000006': 'Unemployment - Black or African American',
            'LNS14000009': 'Unemployment - Hispanic or Latino',
            'LNS14000003': 'Unemployment - White',
            'LNS14032183': 'Unemployment - Asian',
            'LNS14000002': 'Unemployment - Women',
            'LNS14000001': 'Unemployment - Men',
            'LNS14000005': 'Unemployment - White Women',
            'LNS14000004': 'Unemployment - White Men',
            # Civilian Labor Force Level Series (these values are in thousands, not proportions)
            'LNS11000004': 'Labor Force - White Men',
            'LNS11000005': 'Labor Force - White Women',
            'LNS11032183': 'Labor Force - Asian',
            'LNS11000001': 'Labor Force - Men',
            'LNS11000002': 'Labor Force - Women',
            'LNS11000003': 'Labor Force - White',
            'LNS11000006': 'Labor Force - Black or African American',
            'LNS11000009': 'Labor Force - Hispanic or Latino',
            # Industry Series - Management, Professional, and Related Occupations
            'LNU02032526': 'Employment Level - Management, Professional, Women',
            'LNU02032468': 'Employment Level - Management, Professional, Men',
            'LNU02035886': 'Employment Level - Management, Professional, Asian',
            'LNU02035918': 'Employment Level - Management, Professional, White',
            'LNU02035957': 'Employment Level - Management, Professional, Hispanic or Latino',
            'LNU02035874': 'Employment Level - Management, Professional, Black or African American',
            # Industry Series - Service Occupations
            'LNU02032539': 'Employment Level - Service, Women',
            'LNU02032481': 'Employment Level - Service, Men',
            'LNU02035042': 'Employment Level - Service, Asian',
            'LNU02035006': 'Employment Level - Service, White',
            'LNU02035074': 'Employment Level - Service, Hispanic or Latino',
            'LNU02035018': 'Employment Level - Service, Black or African American',
            # Industry Series - Sales and Office Occupations
            'LNU02032545': 'Employment Level - Sales and Office, Women',
            'LNU02032487': 'Employment Level - Sales and Office, Men',
            'LNU02035941': 'Employment Level - Sales and Office, Asian',
            'LNU02035920': 'Employment Level - Sales and Office, White',
            'LNU02035959': 'Employment Level - Sales and Office, Hispanic or Latino',
            'LNU02035898': 'Employment Level - Sales and Office, Black or African American',
            # Industry Series - Natural resources, construction, and maintenance occupations
            'LNU02032548': 'Employment Level - Natural resources, construction, and maintenance, Women',
            'LNU02032490': 'Employment Level - Natural resources, construction, and maintenance, Men',
            'LNU02034909': 'Employment Level - Natural resources, construction, and maintenance, Asian',
            'LNU02034877': 'Employment Level - Natural resources, construction, and maintenance, White',
            'LNU02034937': 'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
            'LNU02034891': 'Employment Level - Natural resources, construction, and maintenance, Black or African American',
            # Industry Series - Production, transportation, and material moving occupations
            'LNU02032554': 'Employment Level - Production, transportation, and material moving, Women',
            'LNU02032496': 'Employment Level - Production, transportation, and material moving, Men',
            'LNU02035873': 'Employment Level - Production, transportation, and material moving, Asian',
            'LNU02035897': 'Employment Level - Production, transportation, and material moving, White',
            'LNU02035933': 'Employment Level - Production, transportation, and material moving, Hispanic or Latino',
            'LNU02035885': 'Employment Level - Production, transportation, and material moving, Black or African American'
        }
        series_name_mapping = sn_map

        # Add series_name to df_filtered
        df_filtered['series_name'] = df_filtered['series_id'].map(series_name_mapping)

        latest_full_year = df_filtered['year'].astype(int).max()
        if latest_full_year == datetime.now().year:
            latest_full_year -= 1 # Use the last full year if current year is not complete

        df_seasonal = df_filtered[df_filtered['year'].astype(int) == latest_full_year].copy()
        df_seasonal['series_name'] = df_seasonal['series_id'].map(series_name_mapping)

        avg_rates_latest_year = df_seasonal.groupby('series_id')['value'].mean().reset_index()
        avg_rates_latest_year['series_name'] = avg_rates_latest_year['series_id'].map(series_name_mapping)

        # Separate unemployment and labor force dataframes
        unemployment_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Unemployment')].copy()
        labor_force_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Labor Force')].copy()

        # Separate industry dataframes
        industry_management_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Management, Professional')].copy()
        industry_service_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Service,')].copy() # Added comma to avoid 'Service Occupations' matching other services
        industry_sales_office_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Sales and Office')].copy()
        industry_natural_construction_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Natural resources, construction')].copy()
        industry_transportation_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Production, transportation')].copy()

        # Calculate 'proportion' for labor_force_avg_df for display in About page
        if not labor_force_avg_df.empty:
            total_labor_force_sum = labor_force_avg_df['value'].sum()
            if total_labor_force_sum > 0:
                labor_force_avg_df['proportion'] = labor_force_avg_df['value'] / total_labor_force_sum
            else:
                labor_force_avg_df['proportion'] = 0.0 # Assign 0.0 if sum is zero

        # Define desired order for consistent plotting (optional, but good practice)
        desired_order = [
            'Unemployment - Men',
            'Unemployment - Women',
            'Unemployment - White Men',
            'Unemployment - White Women',
            'Unemployment - Black or African American',
            'Unemployment - Hispanic or Latino',
            'Unemployment - Asian',
            'Unemployment - White',
            'Labor Force - Men',
            'Labor Force - Women',
            'Labor Force - White Men',
            'Labor Force - White Women',
            'Labor Force - Black or African American',
            'Labor Force - Hispanic or Latino',
            'Labor Force - Asian',
            'Labor Force - White',
            # Management
            'Employment Level - Management, Professional, Women',
            'Employment Level - Management, Professional, Men',
            'Employment Level - Management, Professional, Asian',
            'Employment Level - Management, Professional, White',
            'Employment Level - Management, Professional, Hispanic or Latino',
            'Employment Level - Management, Professional, Black or African American',
            # Service
            'Employment Level - Service, Women',
            'Employment Level - Service, Men',
            'Employment Level - Service, Asian',
            'Employment Level - Service, White',
            'Employment Level - Service, Hispanic or Latino',
            'Employment Level - Service, Black or African American',
            # Sales and Office
            'Employment Level - Sales and Office, Women',
            'Employment Level - Sales and Office, Men',
            'Employment Level - Sales and Office, Asian',
            'Employment Level - Sales and Office, White',
            'Employment Level - Sales and Office, Hispanic or Latino',
            'Employment Level - Sales and Office, Black or African American',
            # Natural resources, construction, and maintenance
            'Employment Level - Natural resources, construction, and maintenance, Women',
            'Employment Level - Natural resources, construction, and maintenance, Men',
            'Employment Level - Natural resources, construction, and maintenance, Asian',
            'Employment Level - Natural resources, construction, and maintenance, White',
            'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
            'Employment Level - Natural resources, construction, and maintenance, Black or African American',
            # Production, transportation, and material moving
            'Employment Level - Production, transportation, and material moving, Women',
            'Employment Level - Production, transportation, and material moving, Men',
            'Employment Level - Production, transportation, and material moving, Asian',
            'Employment Level - Production, transportation, and material moving, White',
            'Employment Level - Production, transportation, and material moving, Hispanic or Latino',
            'Employment Level - Production, transportation, and material moving, Black or African American'
        ]

        # Apply categorical order to all relevant dataframes
        for df_to_order in [unemployment_avg_df, labor_force_avg_df, industry_management_avg_df, 
                            industry_service_avg_df, industry_sales_office_avg_df, 
                            industry_natural_construction_avg_df, industry_transportation_avg_df]:
            if not df_to_order.empty:
                df_to_order['series_name'] = pd.Categorical(
                    df_to_order['series_name'],
                    categories=desired_order,
                    ordered=True
                )
                df_to_order.sort_values('series_name', inplace=True)

        return df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, \
               industry_management_avg_df, industry_service_avg_df, \
               industry_sales_office_avg_df, industry_natural_construction_avg_df, \
               industry_transportation_avg_df
    return pd.DataFrame(), None, pd.DataFrame(), pd.DataFrame(), \
           pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- Visualization Functions ---
def plot_rates_by_sex(avg_df, year, chart_type_prefix, color_code):
    sex_groups = [
        f'{chart_type_prefix} - Men',
        f'{chart_type_prefix} - Women',
        f'{chart_type_prefix} - White Men',
        f'{chart_type_prefix} - White Women',
        f'{chart_type_prefix} - Black or African American Men' if 'Black or African American Men' in avg_df['series_name'].values else None,
        f'{chart_type_prefix} - Hispanic or Latino Men' if 'Hispanic or Latino Men' in avg_df['series_name'].values else None,
        f'{chart_type_prefix} - Asian Men' if 'Asian Men' in avg_df['series_name'].values else None,
        f'{chart_type_prefix} - Black or African American Women' if 'Black or African American Women' in avg_df['series_name'].values else None,
        f'{chart_type_prefix} - Hispanic or Latino Women' if 'Hispanic or Latino Women' in avg_df['series_name'].values else None,
        f'{chart_type_prefix} - Asian Women' if 'Asian Women' in avg_df['series_name'].values else None,
    ]
    sex_groups = [g for g in sex_groups if g is not None] # Filter out None

    df_sex = avg_df[avg_df['series_name'].isin(sex_groups)].copy()

    y_column = 'value'
    y_axis_label = ''
    tick_format = None
    text_auto_format = False

    # Special handling for Employment Level series which are counts, not proportions
    if 'Employment Level' in chart_type_prefix:
        # For these, calculate proportion relative to total men+women in that specific industry
        base_sex_groups_in_industry = [s for s in sex_groups if f'{chart_type_prefix}' in s and ('Men' in s or 'Women' in s)]
        total_men_women_in_industry = avg_df[avg_df['series_name'].isin(base_sex_groups_in_industry)]['value'].sum()

        if total_men_women_in_industry > 0:
            df_sex['proportion'] = df_sex['value'] / total_men_women_in_industry
        else:
            df_sex['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = f'Proportion of Total {chart_type_prefix.replace("Employment Level - ", "")} Employment (Men + Women)'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Unemployment':
        y_axis_label = 'Average Unemployment Rate (Proportion)'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Labor Force':
        # Calculate proportions relative to total Men + Women labor force
        base_sex_groups = ['Labor Force - Men', 'Labor Force - Women']
        total_men_women_lf = avg_df[avg_df['series_name'].isin(base_sex_groups)]['value'].sum()

        if total_men_women_lf > 0:
            df_sex['proportion'] = df_sex['value'] / total_men_women_lf
        else:
            df_sex['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = 'Proportion of Total Men + Women Labor Force'
        tick_format = '.1%'
        text_auto_format = '.1%'


    df_sex = df_sex.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_sex,
        x='series_name',
        y=y_column,
        title=f'Average {chart_type_prefix} by Sex in {year}',
        labels={'series_name': 'Demographic Group', y_column: y_axis_label},
        color_discrete_sequence=[color_code], # Unified color
        text_auto=text_auto_format if text_auto_format else False
    )
    fig.update_layout(
        xaxis_title='Demographic Group',
        yaxis_title=y_axis_label,
        showlegend=False
    )
    if tick_format:
        fig.update_yaxes(tickformat=tick_format)

    return fig

def plot_rates_by_race(avg_df, year, chart_type_prefix, color_code):
    race_groups = [
        f'{chart_type_prefix} - Black or African American',
        f'{chart_type_prefix} - Hispanic or Latino',
        f'{chart_type_prefix} - Asian',
        f'{chart_type_prefix} - White'
    ]
    df_race = avg_df[avg_df['series_name'].isin(race_groups)].copy()

    y_column = 'value'
    y_axis_label = ''
    tick_format = None
    text_auto_format = False

    if 'Employment Level' in chart_type_prefix:
        # For these, calculate proportion relative to total men+women in that specific industry
        base_race_groups_in_industry = [s for s in race_groups if f'{chart_type_prefix}' in s]
        total_race_in_industry = avg_df[avg_df['series_name'].isin(base_race_groups_in_industry)]['value'].sum()

        if total_race_in_industry > 0:
            df_race['proportion'] = df_race['value'] / total_race_in_industry
        else:
            df_race['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = f'Proportion of Total {chart_type_prefix.replace("Employment Level - ", "")} Employment (Selected Races)'
        tick_format = '.1%'
        text_auto_format = '.1%'

    elif chart_type_prefix == 'Unemployment':
        y_axis_label = 'Average Unemployment Rate (Proportion)'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Labor Force':
        # Calculate proportions relative to specific race groups labor force
        base_race_groups = ['Labor Force - White', 'Labor Force - Black or African American', 'Labor Force - Asian', 'Labor Force - Hispanic or Latino']
        total_race_lf = avg_df[avg_df['series_name'].isin(base_race_groups)]['value'].sum()

        if total_race_lf > 0:
            df_race['proportion'] = df_race['value'] / total_race_lf
        else:
            df_race['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = 'Proportion of Selected Racial/Ethnic Labor Force'
        tick_format = '.1%'
        text_auto_format = '.1%'

    df_race = df_race.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_race,
        x='series_name',
        y=y_column,
        title=f'Average {chart_type_prefix} by Race in {year}',
        labels={'series_name': 'Demographic Group', y_column: y_axis_label},
        color_discrete_sequence=[color_code], # Unified color
        text_auto=text_auto_format if text_auto_format else False
    )
    fig.update_layout(
        xaxis_title='Demographic Group',
        yaxis_title=y_axis_label,
        showlegend=False
    )
    if tick_format:
        fig.update_yaxes(tickformat=tick_format)

    return fig

def plot_industry_distribution_by_race(df_filtered_all_data, year, industry_dfs_list):
    # Filter df_filtered_all_data to only include industry series and desired racial groups
    industry_keywords = [
        'Management, Professional',
        'Service,',
        'Sales and Office',
        'Natural resources, construction',
        'Production, transportation'
    ]
    target_races = ['White', 'Black or African American', 'Asian', 'Hispanic or Latino']

    # Filter for relevant series_names and create 'industry_category' and 'race_category'
    filtered_industry_data = df_filtered_all_data[
        df_filtered_all_data['series_name'].str.contains('Employment Level -')
    ].copy()

    def extract_categories(series_name):
        # Example: 'Employment Level - Management, Professional, Women'
        # Extract industry type and race/sex
        parts = series_name.split(' - ')
        if len(parts) < 2: return None, None

        industry_part = parts[1].split(',')[0].strip()
        demographic_part = parts[1].split(',')[-1].strip()

        # Map industry_part to a consistent short name
        if 'Management, Professional' in industry_part: industry_category = 'Management'
        elif 'Service' in industry_part: industry_category = 'Service'
        elif 'Sales and Office' in industry_part: industry_category = 'Sales & Office'
        elif 'Natural resources, construction' in industry_part: industry_category = 'Nat. Res. & Const.'
        elif 'Production, transportation' in industry_part: industry_category = 'Prod. & Trans.'
        else: industry_category = 'Other Industry'

        # Map demographic_part to a race category, ignoring 'Men'/'Women' directly
        race_category = None
        if 'White' in demographic_part: race_category = 'White'
        elif 'Black or African American' in demographic_part: race_category = 'Black/African American'
        elif 'Asian' in demographic_part: race_category = 'Asian'
        elif 'Hispanic or Latino' in demographic_part: race_category = 'Hispanic/Latino'

        return industry_category, race_category

    # Apply extraction, filter out non-race entries, and ensure specific races
    temp_df = filtered_industry_data.apply(lambda row: extract_categories(row['series_name']), axis=1, result_type='expand')
    temp_df.columns = ['industry_category', 'race_category']
    filtered_industry_data = pd.concat([filtered_industry_data, temp_df], axis=1)
    filtered_industry_data.dropna(subset=['race_category'], inplace=True)

    # Group by race and industry, sum values (employment numbers)
    aggregated_data = filtered_industry_data.groupby(['race_category', 'industry_category'])['value'].sum().reset_index()

    # Calculate total employment for each race across all included industries
    total_employment_per_race = aggregated_data.groupby('race_category')['value'].sum().reset_index()
    total_employment_per_race.rename(columns={'value': 'total_race_employment'}, inplace=True)

    # Merge to calculate proportion within each race
    merged_df = pd.merge(aggregated_data, total_employment_per_race, on='race_category')
    merged_df['proportion_within_race'] = merged_df['value'] / merged_df['total_race_employment']

    # Define explicit order for races and industries for plotting
    race_order_plot = ['White', 'Black/African American', 'Hispanic/Latino', 'Asian']
    industry_order_plot = ['Management', 'Service', 'Sales & Office', 'Nat. Res. & Const.', 'Prod. & Trans.']

    merged_df['race_category'] = pd.Categorical(merged_df['race_category'], categories=race_order_plot, ordered=True)
    merged_df['industry_category'] = pd.Categorical(merged_df['industry_category'], categories=industry_order_plot, ordered=True)
    merged_df.sort_values(by=['race_category', 'industry_category'], inplace=True)

    fig = px.bar(
        merged_df,
        x='race_category',
        y='proportion_within_race',
        color='industry_category',
        title=f'Proportion of Each Racial/Ethnic Group Across Industry Categories in {year}',
        labels={
            'race_category': 'Racial/Ethnic Group',
            'proportion_within_race': 'Proportion of Employment within Group',
            'industry_category': 'Industry Category'
        },
        height=600,
        color_discrete_sequence=px.colors.qualitative.Plotly # Example palette
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(
        xaxis_title="Racial/Ethnic Group",
        yaxis_title="Proportion of Employment within Group",
        legend_title="Industry Category"
    )
    return fig

# --- Streamlit App Entry Point ---
def main():
    st.title("Industry Visualizations Dashboard")
    st.markdown("Exploring employment levels across various industries by sex and race.")

    # Load data once
    df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, \
    industry_management_avg_df, industry_service_avg_df, \
    industry_sales_office_avg_df, industry_natural_construction_avg_df, \
    industry_transportation_avg_df = load_and_process_bls_data()

    if df_filtered.empty:
        st.warning("Could not load data from BLS. Please check the API key or try again later.")
        return

    st.header(f"BLS Employment Data for {latest_full_year}")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Labor Force Visualizations",
        "Management, Professional & Related",
        "Service Occupations",
        "Sales & Office Occupations",
        "Natural Resources, Construction & Maintenance",
        "Production, Transportation & Material Moving",
        "Industry Distribution by Race"
    ])

    if page == "Labor Force Visualizations":
        st.subheader("Average Labor Force by Sex and Race")
        st.plotly_chart(plot_rates_by_sex(labor_force_avg_df, latest_full_year, 'Labor Force', 'steelblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(labor_force_avg_df, latest_full_year, 'Labor Force', 'darkorange'), use_container_width=True)

    elif page == "Management, Professional & Related":
        st.subheader("Management, Professional and Related Occupations")
        st.plotly_chart(plot_rates_by_sex(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional', 'lightblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional', 'lightcoral'), use_container_width=True)

    elif page == "Service Occupations":
        st.subheader("Service Occupations")
        st.plotly_chart(plot_rates_by_sex(industry_service_avg_df, latest_full_year, 'Employment Level - Service', 'lightblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(industry_service_avg_df, latest_full_year, 'Employment Level - Service', 'lightcoral'), use_container_width=True)

    elif page == "Sales & Office Occupations":
        st.subheader("Sales and Office Occupations")
        st.plotly_chart(plot_rates_by_sex(industry_sales_office_avg_df, latest_full_year, 'Employment Level - Sales and Office', 'lightblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(industry_sales_office_avg_df, latest_full_year, 'Employment Level - Sales and Office', 'lightcoral'), use_container_width=True)

    elif page == "Natural Resources, Construction & Maintenance":
        st.subheader("Natural resources, construction, and maintenance occupations")
        st.plotly_chart(plot_rates_by_sex(industry_natural_construction_avg_df, latest_full_year, 'Employment Level - Natural resources, construction, and maintenance', 'lightblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(industry_natural_construction_avg_df, latest_full_year, 'Employment Level - Natural resources, construction, and maintenance', 'lightcoral'), use_container_width=True)

    elif page == "Production, Transportation & Material Moving":
        st.subheader("Production, transportation, and material moving occupations")
        st.plotly_chart(plot_rates_by_sex(industry_transportation_avg_df, latest_full_year, 'Employment Level - Production, transportation, and material moving', 'lightblue'), use_container_width=True)
        st.plotly_chart(plot_rates_by_race(industry_transportation_avg_df, latest_full_year, 'Employment Level - Production, transportation, and material moving', 'lightcoral'), use_container_width=True)

    elif page == "Industry Distribution by Race":
        st.subheader("Industry Distribution by Race")
        all_industry_dfs = [
            industry_management_avg_df,
            industry_service_avg_df,
            industry_sales_office_avg_df,
            industry_natural_construction_avg_df,
            industry_transportation_avg_df
        ]
        st.plotly_chart(plot_industry_distribution_by_race(df_filtered, latest_full_year, all_industry_dfs), use_container_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
