import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import requests
import json
from datetime import datetime

# --- Global Streamlit Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Define Real Story Variables Globally (for use in both reveal and visualizations stages) ---
real_noun_1 = "humanity"
real_noun_2 = "present"
real_noun_3 = "past"
real_noun_4 = "evidence"
real_noun_resource = "resources"
real_noun_society_plural = "societies"
real_proper_noun_1 = "Mesopotamia"
real_proper_noun_2 = "Japan"
real_plural_noun_3 = "hierarchies"
real_adjective_1 = "dominant"
real_noun_5 = "class"
real_noun_6 = "existence"
real_plural_noun_4 = "cohorts"
real_plural_noun_5 = "underclasses"
real_noun_7 = "poor"
real_verb_1 = "toiled"
real_adjective_2 = "higher"
real_noun_8 = "slavery"
real_noun_9 = "serfdom"
real_proper_noun_3 = "Europe"
real_noun_10 = "humanity"
real_noun_11 = "labor"

real_adjective_3 = "extreme"
real_noun_12 = "wealth"
real_noun_13 = "status"
real_noun_14 = "millennia"
real_adverb_1 = "indeed"
real_noun_15 = "empires"
real_noun_16 = "empires"
real_verb_2 = "fallen"
real_adjective_4 = "invading"
real_noun_17 = "forces"
real_verb_3 = "hoard"
real_noun_18 = "wealth"
real_noun_19 = "land"
real_noun_20 = "labor"
real_noun_21 = "violence"
real_noun_22 = "systems"
real_noun_23 = "inequality"
real_noun_24 = "slave"
real_adjective_5 = "antebellum"
real_noun_25 = "immigrants"
real_proper_noun_4 = "ICE"
real_noun_26 = "violence"
real_noun_27 = "tool"
real_verb_4 = "favored"
real_noun_28 = "elites"
real_noun_29 = "compliance"
real_noun_30 = "poor"

# --- Global list for text collage (shortened version as per previous instructions) ---
all_real_words = [
    real_noun_1, real_noun_2, real_noun_3, real_noun_4, real_noun_resource, real_noun_society_plural,
    real_proper_noun_1, real_proper_noun_2, real_plural_noun_3, real_adjective_1, real_noun_5,
    real_plural_noun_4, real_plural_noun_5, real_noun_7, real_verb_1,
    real_noun_8, real_noun_9,
    real_proper_noun_3, real_adjective_3, real_noun_12, real_noun_13, real_noun_14,
    real_noun_15, real_verb_2, real_adjective_4, real_noun_17, real_verb_3,
    real_noun_18, real_noun_20, real_noun_22, real_noun_23,
    real_adjective_5, real_noun_25, real_proper_noun_4, real_noun_26, real_noun_27, real_verb_4, real_noun_28,
    real_noun_29, real_noun_30
]

# --- Function to display the text collage ---
def display_text_collage():
    random.seed(42) # for reproducibility
    random.shuffle(all_real_words)
    collage_html = ""
    colors = ['#FF0000', '#0000FF', '#333333', '#666666'] # Red, Blue, Dark Gray, Medium Gray
    font_sizes = ['1.0em', '1.2em', '1.4em', '1.6em', '1.8em']
    for word in all_real_words:
        color = random.choice(colors)
        font_size = random.choice(font_sizes)
        collage_html += f"<span style='color:{color}; font-size:{font_size}; margin: 0 5px; display: inline-block;'>{word}</span> "
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) # Spacing before
    st.markdown(collage_html, unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) # Spacing after

# --- Data Loading and Processing Function ---
@st.cache_data
def load_and_process_bls_data():
    headers = {'Content-type': 'application/json'}
    current_year = datetime.now().year
    data = json.dumps(
        {
            "seriesid": [
                'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004', # Existing Unemployment IDs
                'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001', 'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',  # New Labor Force IDs
                'LNU02032526', 'LNU02032468', 'LNU02035886', 'LNU02035918', 'LNU02035957', 'LNU02035874', # New Industry Series IDs - Management
                'LNU02032539', 'LNU02032481', 'LNU02035042', 'LNU02035006', 'LNU02035041', 'LNU02035007', # New Industry Series IDs - Service
                'LNU02032545', 'LNU02032487', 'LNU02035920', 'LNU02035959', 'LNU02035877', 'LNU02035889', # New Industry Series IDs - Sales and Office
                'LNU02032490', 'LNU02034909', 'LNU02032548', 'LNU02034877', 'LNU02034935Q', 'LNU02034893' # New Industry Series IDs - Natural Resources, Construction, and Maintenance
            ],
            "startyear": str(current_year - 4),
            "endyear": str(current_year),
            "registrationkey": "9dd192e92c9c4989985db57deede9647"
        }
    )
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
                    all_series_data.append(
                        {
                            'series_id': seriesId,
                            'year': year,
                            'period': period,
                            'value': value,
                            'footnotes': footnotes
                        }
                    )
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
            'LNU02035041': 'Employment Level - Service, Black or African American',
            'LNU02035007': 'Employment Level - Service, Hispanic or Latino',
            # Industry Series - Sales and Office Occupations
            'LNU02032545': 'Employment Level - Sales and Office, Women',
            'LNU02032487': 'Employment Level - Sales and Office, Men',
            'LNU02035920': 'Employment Level - Sales and Office, White',
            'LNU02035959': 'Employment Level - Sales and Office, Hispanic or Latino',
            'LNU02035877': 'Employment Level - Sales and Office, Black or African American',
            'LNU02035889': 'Employment Level - Sales and Office, Asian',
            # Industry Series - Natural resources, construction, and maintenance occupations
            'LNU02032490': 'Employment Level - Natural resources, construction, and maintenance, Men',
            'LNU02034909': 'Employment Level - Natural resources, construction, and maintenance, Asian',
            'LNU02032548': 'Employment Level - Natural resources, construction, and maintenance, Women',
            'LNU02034877': 'Employment Level - Natural resources, construction, and maintenance, White',
            'LNU02034935Q': 'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
            'LNU02034893': 'Employment Level - Natural resources, construction, and maintenance, Black or African American'
        }
        series_name_mapping = sn_map

        # Add series_name to df_filtered before returning
        df_filtered['series_name'] = df_filtered['series_id'].map(series_name_mapping)

        latest_full_year = df_filtered['year'].astype(int).max()
        if latest_full_year == datetime.now().year:
            latest_full_year -= 1 # Use the last full year if current year is not complete

        df_seasonal = df_filtered[df_filtered['year'].astype(int) == latest_full_year].copy()
        df_seasonal['series_name'] = df_seasonal['series_id'].map(series_name_mapping)

        avg_rates_latest_year = df_seasonal.groupby('series_id')['value'].mean().reset_index()
        avg_rates_latest_year['series_name'] = avg_rates_latest_year['series_id'].map(series_name_mapping)

        # Separate unemployment, labor force, and industry management dataframes
        unemployment_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Unemployment')].copy()
        labor_force_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Labor Force')].copy()
        industry_management_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Management, Professional')].copy()
        industry_service_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Service')].copy()
        industry_sales_office_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Sales and Office')].copy()
        industry_natural_construction_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Employment Level - Natural resources, construction, and maintenance')].copy()

        # Calculate 'proportion' for labor_force_avg_df for display in About page
        if not labor_force_avg_df.empty:
            total_labor_force_sum = labor_force_avg_df['value'].sum()
            if total_labor_force_sum > 0:
                labor_force_avg_df['proportion'] = labor_force_avg_df['value'] / total_labor_force_sum
            else:
                labor_force_avg_df['proportion'] = 0.0 # Assign 0.0 if sum is zero

        # Calculate 'proportion' for industry_management_avg_df
        if not industry_management_avg_df.empty:
            total_management_prof_sum = industry_management_avg_df['value'].sum()
            if total_management_prof_sum > 0:
                industry_management_avg_df['proportion'] = industry_management_avg_df['value'] / total_management_prof_sum
            else:
                industry_management_avg_df['proportion'] = 0.0

        # Calculate 'proportion' for industry_service_avg_df
        if not industry_service_avg_df.empty:
            total_service_sum = industry_service_avg_df['value'].sum()
            if total_service_sum > 0:
                industry_service_avg_df['proportion'] = industry_service_avg_df['value'] / total_service_sum
            else:
                industry_service_avg_df['proportion'] = 0.0

        # Calculate 'proportion' for industry_sales_office_avg_df
        if not industry_sales_office_avg_df.empty:
            total_sales_office_sum = industry_sales_office_avg_df['value'].sum()
            if total_sales_office_sum > 0:
                industry_sales_office_avg_df['proportion'] = industry_sales_office_avg_df['value'] / total_sales_office_sum
            else:
                industry_sales_office_avg_df['proportion'] = 0.0

        # Calculate 'proportion' for industry_natural_construction_avg_df
        if not industry_natural_construction_avg_df.empty:
            total_natural_construction_sum = industry_natural_construction_avg_df['value'].sum()
            if total_natural_construction_sum > 0:
                industry_natural_construction_avg_df['proportion'] = industry_natural_construction_avg_df['value'] / total_natural_construction_sum
            else:
                industry_natural_construction_avg_df['proportion'] = 0.0

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
            'Employment Level - Management, Professional, Women',
            'Employment Level - Management, Professional, Men',
            'Employment Level - Management, Professional, Asian',
            'Employment Level - Management, Professional, White',
            'Employment Level - Management, Professional, Hispanic or Latino',
            'Employment Level - Management, Professional, Black or African American',
            'Employment Level - Service, Women',
            'Employment Level - Service, Men',
            'Employment Level - Service, Asian',
            'Employment Level - Service, White',
            'Employment Level - Service, Hispanic or Latino',
            'Employment Level - Service, Black or African American',
            'Employment Level - Sales and Office, Women',
            'Employment Level - Sales and Office, Men',
            'Employment Level - Sales and Office, White',
            'Employment Level - Sales and Office, Hispanic or Latino',
            'Employment Level - Sales and Office, Black or African American',
            'Employment Level - Sales and Office, Asian',
            'Employment Level - Natural resources, construction, and maintenance, Women',
            'Employment Level - Natural resources, construction, and maintenance, Men',
            'Employment Level - Natural resources, construction, and maintenance, Asian',
            'Employment Level - Natural resources, construction, and maintenance, White',
            'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
            'Employment Level - Natural resources, construction, and maintenance, Black or African American'
        ]
        unemployment_avg_df['series_name'] = pd.Categorical(
            unemployment_avg_df['series_name'],
            categories=desired_order,
            ordered=True
        )
        unemployment_avg_df = unemployment_avg_df.sort_values('series_name')

        # Re-apply categorical order for labor_force_avg_df as well
        labor_force_avg_df['series_name'] = pd.Categorical(
            labor_force_avg_df['series_name'],
            categories=desired_order, # Use the same overall desired order
            ordered=True
        )
        labor_force_avg_df = labor_force_avg_df.sort_values('series_name')

        industry_management_avg_df['series_name'] = pd.Categorical(
            industry_management_avg_df['series_name'],
            categories=desired_order,
            ordered=True
        )
        industry_management_avg_df = industry_management_avg_df.sort_values('series_name')

        industry_service_avg_df['series_name'] = pd.Categorical(
            industry_service_avg_df['series_name'],
            categories=desired_order,
            ordered=True
        )
        industry_service_avg_df = industry_service_avg_df.sort_values('series_name')

        industry_sales_office_avg_df['series_name'] = pd.Categorical(
            industry_sales_office_avg_df['series_name'],
            categories=desired_order,
            ordered=True
        )
        industry_sales_office_avg_df = industry_sales_office_avg_df.sort_values('series_name')

        industry_natural_construction_avg_df['series_name'] = pd.Categorical(
            industry_natural_construction_avg_df['series_name'],
            categories=desired_order,
            ordered=True
        )
        industry_natural_construction_avg_df = industry_natural_construction_avg_df.sort_values('series_name')

        return df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, industry_natural_construction_avg_df
    return pd.DataFrame(), None, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- Visualization Functions ---
def plot_rates_by_sex(avg_df, year, chart_type_prefix):
    if chart_type_prefix == 'Employment Level - Management, Professional':
        sex_groups = [
            'Employment Level - Management, Professional, Men',
            'Employment Level - Management, Professional, Women'
        ]
    elif chart_type_prefix == 'Employment Level - Service':
        sex_groups = [
            'Employment Level - Service, Men',
            'Employment Level - Service, Women'
        ]
    elif chart_type_prefix == 'Employment Level - Sales and Office':
        sex_groups = [
            'Employment Level - Sales and Office, Men',
            'Employment Level - Sales and Office, Women'
        ]
    elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
        sex_groups = [
            'Employment Level - Natural resources, construction, and maintenance, Men',
            'Employment Level - Natural resources, construction, and maintenance, Women'
        ]
    else:
        sex_groups = [f'{chart_type_prefix} - Men', f'{chart_type_prefix} - Women', f'{chart_type_prefix} - White Men', f'{chart_type_prefix} - White Women']
    df_sex = avg_df[avg_df['series_name'].isin(sex_groups)].copy()

    y_column = 'value'
    y_axis_label = ''
    tick_format = None
    text_auto_format = False

    if chart_type_prefix == 'Unemployment':
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
    elif chart_type_prefix == 'Employment Level - Management, Professional':
        # We want to plot this proportion directly.
        y_column = 'proportion'
        y_axis_label = 'Proportion of Management, Professional Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Service':
        # We want to plot this proportion directly.
        y_column = 'proportion'
        y_axis_label = 'Proportion of Service Occupations Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Sales and Office':
        y_column = 'proportion'
        y_axis_label = 'Proportion of Sales and Office Occupations Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
        y_column = 'proportion'
        y_axis_label = 'Proportion of Natural Resources, Construction, and Maintenance Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'

    df_sex = df_sex.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_sex,
        x='series_name',
        y=y_column,
        title=f'Average {chart_type_prefix} by Sex in {year}',
        labels={'series_name': 'Demographic Group', y_column: y_axis_label},
        color='series_name',
        text_auto=text_auto_format
    )

    fig.update_layout(
        xaxis_title='Demographic Group',
        yaxis_title=y_axis_label,
        showlegend=False
    )
    if tick_format:
        fig.update_yaxes(tickformat=tick_format)

    return fig

def plot_rates_by_race(avg_df, year, chart_type_prefix):
    if chart_type_prefix == 'Employment Level - Management, Professional':
        race_groups = [
            'Employment Level - Management, Professional, Black or African American',
            'Employment Level - Management, Professional, Hispanic or Latino',
            'Employment Level - Management, Professional, Asian',
            'Employment Level - Management, Professional, White'
        ]
    elif chart_type_prefix == 'Employment Level - Service':
        race_groups = [
            'Employment Level - Service, Black or African American',
            'Employment Level - Service, Hispanic or Latino',
            'Employment Level - Service, Asian',
            'Employment Level - Service, White'
        ]
    elif chart_type_prefix == 'Employment Level - Sales and Office':
        race_groups = [
            'Employment Level - Sales and Office, Black or African American',
            'Employment Level - Sales and Office, Hispanic or Latino',
            'Employment Level - Sales and Office, Asian',
            'Employment Level - Sales and Office, White'
        ]
    elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
        race_groups = [
            'Employment Level - Natural resources, construction, and maintenance, Black or African American',
            'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
            'Employment Level - Natural resources, construction, and maintenance, Asian',
            'Employment Level - Natural resources, construction, and maintenance, White'
        ]
    else:
        race_groups = [f'{chart_type_prefix} - Black or African American', f'{chart_type_prefix} - Hispanic or Latino', f'{chart_type_prefix} - Asian', f'{chart_type_prefix} - White']
    df_race = avg_df[avg_df['series_name'].isin(race_groups)].copy()

    y_column = 'value'
    y_axis_label = ''
    tick_format = None
    text_auto_format = False

    if chart_type_prefix == 'Unemployment':
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
    elif chart_type_prefix == 'Employment Level - Management, Professional':
        # We want to plot this proportion directly.
        y_column = 'proportion'
        y_axis_label = 'Proportion of Management, Professional Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Service':
        # We want to plot this proportion directly.
        y_column = 'proportion'
        y_axis_label = 'Proportion of Service Occupations Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Sales and Office':
        y_column = 'proportion'
        y_axis_label = 'Proportion of Sales and Office Occupations Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'
    elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
        y_column = 'proportion'
        y_axis_label = 'Proportion of Natural Resources, Construction, and Maintenance Employment'
        tick_format = '.1%'
        text_auto_format = '.1%'

    df_race = df_race.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_race,
        x='series_name',
        y=y_column,
        title=f'Average {chart_type_prefix} by Race in {year}',
        labels={'series_name': 'Demographic Group', y_column: y_axis_label},
        color='series_name',
        text_auto=text_auto_format
    )

    fig.update_layout(
        xaxis_title='Demographic Group',
        yaxis_title=y_axis_label,
        showlegend=False
    )
    if tick_format:
        fig.update_yaxes(tickformat=tick_format)

    return fig

def plot_rate_comparisons(avg_df, year, chart_type_prefix):
    # This function is not used for industry visualizations based on user feedback.
    # However, it's kept here in case it's needed for unemployment comparisons later.
    white_women_avg_series_name = f'{chart_type_prefix} - White Women'
    if white_women_avg_series_name not in avg_df['series_name'].values:
        if chart_type_prefix == 'Employment Level - Management, Professional':
            white_women_avg_series_name = 'Employment Level - Management, Professional, Women'
            if white_women_avg_series_name not in avg_df['series_name'].values:
                return []
        elif chart_type_prefix == 'Employment Level - Service':
            white_women_avg_series_name = 'Employment Level - Service, Women'
            if white_women_avg_series_name not in avg_df['series_name'].values:
                return []
        elif chart_type_prefix == 'Employment Level - Sales and Office':
            white_women_avg_series_name = 'Employment Level - Sales and Office, Women'
            if white_women_avg_series_name not in avg_df['series_name'].values:
                return []
        elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
            white_women_avg_series_name = 'Employment Level - Natural resources, construction, and maintenance, Women'
            if white_women_avg_series_name not in avg_df['series_name'].values:
                return []
        else:
            return []

    white_women_avg = avg_df[avg_df['series_name'] == white_women_avg_series_name].iloc[0]

    comparison_order_unemployment = [
        'Unemployment - Asian',
        'Unemployment - White Men',
        'Unemployment - Men',
        'Unemployment - Women',
        'Unemployment - Hispanic or Latino',
        'Unemployment - Black or African American'
    ]

    comparison_order_labor_force = [
        'Labor Force - Asian',
        'Labor Force - White Men',
        'Labor Force - Men',
        'Labor Force - Women',
        'Labor Force - Hispanic or Latino',
        'Labor Force - Black or African American'
    ]
    comparison_order_industry_management = [
        'Employment Level - Management, Professional, Asian',
        'Employment Level - Management, Professional, Men',
        'Employment Level - Management, Professional, Hispanic or Latino',
        'Employment Level - Management, Professional, Black or African American'
    ]
    comparison_order_industry_service = [
        'Employment Level - Service, Asian',
        'Employment Level - Service, Men',
        'Employment Level - Service, Hispanic or Latino',
        'Employment Level - Service, Black or African American'
    ]
    comparison_order_industry_sales_office = [
        'Employment Level - Sales and Office, Asian',
        'Employment Level - Sales and Office, Men',
        'Employment Level - Sales and Office, Hispanic or Latino',
        'Employment Level - Sales and Office, Black or African American'
    ]
    comparison_order_industry_natural_construction = [
        'Employment Level - Natural resources, construction, and maintenance, Asian',
        'Employment Level - Natural resources, construction, and maintenance, Men',
        'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino',
        'Employment Level - Natural resources, construction, and maintenance, Black or African American'
    ]

    if chart_type_prefix == 'Unemployment':
        comparison_order = comparison_order_unemployment
    elif chart_type_prefix == 'Labor Force':
        comparison_order = comparison_order_labor_force
    elif chart_type_prefix == 'Employment Level - Management, Professional':
        comparison_order = comparison_order_industry_management
    elif chart_type_prefix == 'Employment Level - Service':
        comparison_order = comparison_order_industry_service
    elif chart_type_prefix == 'Employment Level - Sales and Office':
        comparison_order = comparison_order_industry_sales_office
    elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
        comparison_order = comparison_order_industry_natural_construction
    else:
        comparison_order = []

    label_mapping = {
        'Unemployment - Asian': 'Asian, Men/Women',
        'Unemployment - White Men': 'White Men',
        'Unemployment - Men': 'Men, All Races',
        'Unemployment - Women': 'Women, All Races',
        'Unemployment - Hispanic or Latino': 'Hispanic or Latino, Men/Women',
        'Unemployment - Black or African American': 'Black or African American, Men/Women',
        'Labor Force - Asian': 'Asian, Men/Women',
        'Labor Force - White Men': 'White Men',
        'Labor Force - Men': 'Men, All Races',
        'Labor Force - Women': 'Women, All Races',
        'Labor Force - Hispanic or Latino': 'Hispanic or Latino, Men/Women',
        'Labor Force - Black or African American': 'Black or African American, Men/Women',
        'Employment Level - Management, Professional, Asian': 'Management, Professional, Asian',
        'Employment Level - Management, Professional, Men': 'Management, Professional, Men',
        'Employment Level - Management, Professional, Hispanic or Latino': 'Management, Professional, Hispanic or Latino',
        'Employment Level - Management, Professional, Black or African American': 'Management, Professional, Black or African American',
        'Employment Level - Service, Asian': 'Service, Asian',
        'Employment Level - Service, Men': 'Service, Men',
        'Employment Level - Service, Hispanic or Latino': 'Service, Hispanic or Latino',
        'Employment Level - Service, Black or African American': 'Service, Black or African American',
        'Employment Level - Sales and Office, Asian': 'Sales and Office, Asian',
        'Employment Level - Sales and Office, Men': 'Sales and Office, Men',
        'Employment Level - Sales and Office, Hispanic or Latino': 'Sales and Office, Hispanic or Latino',
        'Employment Level - Sales and Office, Black or African American': 'Sales and Office, Black or African American',
        'Employment Level - Natural resources, construction, and maintenance, Asian': 'Natural resources, construction, and maintenance, Asian',
        'Employment Level - Natural resources, construction, and maintenance, Men': 'Natural resources, construction, and maintenance, Men',
        'Employment Level - Natural resources, construction, and maintenance, Hispanic or Latino': 'Natural resources, construction, and maintenance, Hispanic or Latino',
        'Employment Level - Natural resources, construction, and maintenance, Black or African American': 'Natural resources, construction, and maintenance, Black or African American'
    }

    other_demographics_ordered = avg_df[
        (avg_df['series_name'] != white_women_avg_series_name) & (avg_df['series_name'].isin(comparison_order))
    ].set_index('series_name').loc[comparison_order].reset_index()

    charts = []
    for index, row in other_demographics_ordered.iterrows():
        comparison_group_name = row['series_name']
        display_comparison_group_name = label_mapping.get(comparison_group_name, comparison_group_name)

        y_column = 'value'
        y_axis_label = ''
        tick_format = None
        text_auto_format = False
        comparison_df = pd.DataFrame() # Initialize comparison_df

        if chart_type_prefix == 'Unemployment':
            y_axis_label = 'Average Unemployment Rate (Proportion)'
            chart_title = f"Average Unemployment: White Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'
            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name, display_comparison_group_name],
                'value': [white_women_avg[y_column], row[y_column]]
            })
        elif chart_type_prefix == 'Labor Force':
            total_relevant_value = avg_df['value'].sum()
            if total_relevant_value > 0:
                white_women_proportion = white_women_avg['value'] / total_relevant_value
                row_proportion = row['value'] / total_relevant_value
            else:
                white_women_proportion = 0
                row_proportion = 0

            y_column = 'proportion'
            y_axis_label = f'Proportion of Total {chart_type_prefix} Force'
            chart_title = f"Average {chart_type_prefix}: White Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })
        elif chart_type_prefix == 'Employment Level - Management, Professional':
            # For Management, Professional, the comparison should be against 'Employment Level - Management, Professional, Women'
            white_women_avg_series_name_mp = 'Employment Level - Management, Professional, Women'
            if white_women_avg_series_name_mp not in avg_df['series_name'].values:
                return [] # Should not happen if data is loaded correctly, but for safety

            white_women_avg_mp = avg_df[avg_df['series_name'] == white_women_avg_series_name_mp].iloc[0]

            # Use the pre-calculated proportions from the avg_df for the comparison
            white_women_proportion = white_women_avg_mp['proportion']
            row_proportion = row['proportion']

            y_column = 'proportion' # Plotting proportions for y-axis
            y_axis_label = f'Proportion of Management, Professional Employment'
            chart_title = f"Average Management, Professional: Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name_mp, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })
        elif chart_type_prefix == 'Employment Level - Service':
            white_women_avg_series_name_sv = 'Employment Level - Service, Women'
            if white_women_avg_series_name_sv not in avg_df['series_name'].values:
                return []

            white_women_avg_sv = avg_df[avg_df['series_name'] == white_women_avg_series_name_sv].iloc[0]

            white_women_proportion = white_women_avg_sv['proportion']
            row_proportion = row['proportion']

            y_column = 'proportion'
            y_axis_label = f'Proportion of Service Occupations Employment'
            chart_title = f"Average Service Occupations: Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name_sv, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })
        elif chart_type_prefix == 'Employment Level - Sales and Office':
            white_women_avg_series_name_so = 'Employment Level - Sales and Office, Women'
            if white_women_avg_series_name_so not in avg_df['series_name'].values:
                return []

            white_women_avg_so = avg_df[avg_df['series_name'] == white_women_avg_series_name_so].iloc[0]

            white_women_proportion = white_women_avg_so['proportion']
            row_proportion = row['proportion']

            y_column = 'proportion'
            y_axis_label = f'Proportion of Sales and Office Occupations Employment'
            chart_title = f"Average Sales and Office Occupations: Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name_so, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })
        elif chart_type_prefix == 'Employment Level - Natural resources, construction, and maintenance':
            white_women_avg_series_name_nr = 'Employment Level - Natural resources, construction, and maintenance, Women'
            if white_women_avg_series_name_nr not in avg_df['series_name'].values:
                return []

            white_women_avg_nr = avg_df[avg_df['series_name'] == white_women_avg_series_name_nr].iloc[0]

            white_women_proportion = white_women_avg_nr['proportion']
            row_proportion = row['proportion']

            y_column = 'proportion'
            y_axis_label = f'Proportion of Natural Resources, Construction, and Maintenance Employment'
            chart_title = f"Average Natural Resources, Construction, and Maintenance: Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name_nr, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })

        fig = px.bar(
            comparison_df,
            x='series_name',
            y=y_column,
            title=chart_title,
            labels={'series_name': 'Demographic Group', y_column: y_axis_label},
            color='series_name',
            text_auto=text_auto_format
        )

        fig.update_layout(
            xaxis_title='Demographic Group',
            yaxis_title=y_axis_label,
            showlegend=False
        )
        if tick_format:
            fig.update_yaxes(tickformat=tick_format)
        charts.append(fig)
    return charts

def plot_labor_force_vs_industry_comparison_by_race(labor_force_avg_df, industry_df, year, industry_name):
    """
    Generates a grouped bar chart comparing the proportion of each race in the total labor force
    with their proportion in a specified industry.
    """
    race_groups_labor_force = [
        'Labor Force - Black or African American',
        'Labor Force - Hispanic or Latino',
        'Labor Force - Asian',
        'Labor Force - White'
    ]

    # Dynamically create race_groups for the specified industry
    race_groups_industry = [
        f'Employment Level - {industry_name}, Black or African American',
        f'Employment Level - {industry_name}, Hispanic or Latino',
        f'Employment Level - {industry_name}, Asian',
        f'Employment Level - {industry_name}, White'
    ]

    # Extract relevant data from labor force
    df_labor_force = labor_force_avg_df[labor_force_avg_df['series_name'].isin(race_groups_labor_force)].copy()
    df_labor_force['category'] = 'Total Labor Force'
    df_labor_force['demographic'] = df_labor_force['series_name'].str.replace('Labor Force - ', '')

    # Extract relevant data from industry
    df_industry = industry_df[df_industry['series_name'].isin(race_groups_industry)].copy()
    df_industry['category'] = industry_name + ' Occupations'
    df_industry['demographic'] = df_industry['series_name'].str.replace(f'Employment Level - {industry_name}, ', '')

    # Concatenate the two dataframes
    comparison_df = pd.concat([df_labor_force, df_industry])

    # Ensure 'demographic' column is consistent for plotting
    # Remove ' or African American' from Black or African American if it exists
    comparison_df['demographic'] = comparison_df['demographic'].replace('Black or African American', 'Black')


    fig = px.bar(
        comparison_df,
        x='demographic',
        y='proportion',
        color='category',
        barmode='group',
        title=f'Comparison of Racial Representation: Labor Force vs. {industry_name} Occupations in {year}',
        labels={
            'demographic': 'Racial/Ethnic Group',
            'proportion': 'Proportion of Group Total',
            'category': 'Category'
        },
        text_auto='.1%'
    )

    fig.update_layout(
        yaxis_title='Proportion',
        showlegend=True,
        legend_title_text='Category'
    )
    fig.update_yaxes(tickformat='.1%')

    return fig

def plot_management_proportion_of_labor_force_by_sex(labor_force_avg_df, industry_df, year, industry_prefix, plot_color):
    # Define series names for labor force and management for men and women
    lf_men_series = 'Labor Force - Men'
    lf_women_series = 'Labor Force - Women'
    mp_men_series = f'Employment Level - {industry_prefix}, Men'
    mp_women_series = f'Employment Level - {industry_prefix}, Women'

    # Get values for men
    lf_men_value = labor_force_avg_df[labor_force_avg_df['series_name'] == lf_men_series]['value'].iloc[0] if not labor_force_avg_df[labor_force_avg_df['series_name'] == lf_men_series].empty else 0
    mp_men_value = industry_df[industry_df['series_name'] == mp_men_series]['value'].iloc[0] if not industry_df[industry_df['series_name'] == mp_men_series].empty else 0

    # Get values for women
    lf_women_value = labor_force_avg_df[labor_force_avg_df['series_name'] == lf_women_series]['value'].iloc[0] if not labor_force_avg_df[labor_force_avg_df['series_name'] == lf_women_series].empty else 0
    mp_women_value = industry_df[industry_df['series_name'] == mp_women_series]['value'].iloc[0] if not industry_df[industry_df['series_name'] == mp_women_series].empty else 0

    # Calculate proportions
    prop_men = mp_men_value / lf_men_value if lf_men_value > 0 else 0
    prop_women = mp_women_value / lf_women_value if lf_women_value > 0 else 0

    # Create DataFrame for plotting
    data_to_plot = pd.DataFrame({
        'Demographic Group': ['Men', 'Women'],
        'Proportion in Occupations': [prop_men, prop_women]
    })

    fig = px.bar(
        data_to_plot,
        x='Demographic Group',
        y='Proportion in Occupations',
        title=f'Proportion of Labor Force in {industry_prefix} Occupations by Sex in {year}',
        labels={'Proportion in Occupations': 'Proportion'},
        color_discrete_sequence=[plot_color],
        text_auto='.1%'
    )

    fig.update_layout(
        yaxis_title='Proportion',
        showlegend=False
    )
    fig.update_yaxes(tickformat='.1%')
    return fig

def plot_management_proportion_of_labor_force_by_race(labor_force_avg_df, industry_df, year, industry_prefix, plot_color):
    # Define series names for labor force and management for race groups
    race_groups = {
        'White': {'lf': 'Labor Force - White', 'mp': f'Employment Level - {industry_prefix}, White'},
        'Black or African American': {'lf': 'Labor Force - Black or African American', 'mp': f'Employment Level - {industry_prefix}, Black or African American'},
        'Asian': {'lf': 'Labor Force - Asian', 'mp': f'Employment Level - {industry_prefix}, Asian'},
        'Hispanic or Latino': {'lf': 'Labor Force - Hispanic or Latino', 'mp': f'Employment Level - {industry_prefix}, Hispanic or Latino'}
    }

    proportions = []
    for race, series_names in race_groups.items():
        lf_value = labor_force_avg_df[labor_force_avg_df['series_name'] == series_names['lf']]['value'].iloc[0] if not labor_force_avg_df[labor_force_avg_df['series_name'] == series_names['lf']].empty else 0
        mp_value = industry_df[industry_df['series_name'] == series_names['mp']]['value'].iloc[0] if not industry_df[industry_df['series_name'] == series_names['mp']].empty else 0

        proportion = mp_value / lf_value if lf_value > 0 else 0
        proportions.append({'Demographic Group': race, 'Proportion in Occupations': proportion})

    data_to_plot = pd.DataFrame(proportions)

    fig = px.bar(
        data_to_plot,
        x='Demographic Group',
        y='Proportion in Occupations',
        title=f'Proportion of Labor Force in {industry_prefix} Occupations by Race in {year}',
        labels={'Proportion in Occupations': 'Proportion'},
        color_discrete_sequence=[plot_color],
        text_auto='.1%'
    )

    fig.update_layout(
        yaxis_title='Proportion',
        showlegend=False
    )
    fig.update_yaxes(tickformat='.1%')
    return fig

# --- Streamlit App ---
col_title_global, col_subtitle_global = st.columns([0.3, 0.7])
with col_title_global:
    st.markdown("<div style='background-color:red; padding: 2px; border-radius: 10px;'><h1 style='color:white; text-align:center; margin: 0; padding: 0;'>Mad Liberal</h1></div>", unsafe_allow_html=True)
with col_subtitle_global:
    st.markdown("""
        <div style='display: flex; flex-direction: column; justify: space-around; height: 100%; padding: 5px 0;'>
            <h4 style='color:blue; text-align:left; margin: 0; padding: 0;'>Python Programming by Casey Hallas for UNO Econ 8320 - May 2026</h4>
            <h4 style='color:black; text-align:left; margin: 0; padding: 0;'>Data collected from The US Bureau of Labor Statistics, www.bls.gov</h4>
        </div>
    """, unsafe_allow_html=True)


# Initialize session state to control app flow - always set to 'industry_visualizations' for this isolated app
st.session_state.game_stage = 'industry_visualizations'

# Global layout: left sidebar (20%), main content (60%), right sidebar (20%)
left_sidebar, main_content, right_sidebar = st.columns([0.2, 0.6, 0.2])

with left_sidebar:
    st.subheader("The Real Story:")
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From <b>{real_proper_noun_1}</b> to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

    st.markdown("-" * 3)

with main_content:
    # --- Industry Visualizations Stage ---
    if st.session_state.game_stage == 'industry_visualizations':
        # Force scroll to the top of the main content area when entering this stage
        st.components.v1.html("<script>window.top.scroll(0, 0);</script>", height=0, width=0)

        viz_col = st.columns([1]) # Use a single column for visualizations in main_content

        with viz_col[0]:
            st.subheader("Industry Visualizations about Sex and Race")
            st.markdown("The US Census Bureau website provides statistics for race in the United States at the current levels: White Alone 74.8&, Black Alone 13.7%, Asian Alone 6.7%, Hispanic or Latino Alone 20%. To calculate our totals we applied data based on seasonal employment rates averaged and totaled - White, Asian, Black or African American and Hispanic or Latino based on the Civilian Labor Force Level. That is to create an active comparison to employment levels by industry against a measurable estimate provided by the BLS.")
            st.markdown("The Department of Labor presents a measure of data called Employed people by detailed occupation, sex, race, and Hispanic or Latino ethnicity (https://www.bls.gov/cps/cpsaat11.htm) that presents percentages of demographics employed in each of those occupations, grouped by industry. I’ve collected data for the primary Industries for gender and race to compare the distribution of demographics across the entire US job market, including the most popular occupations in all 4 categories.")

            df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, industry_natural_construction_avg_df = load_and_process_bls_data()

            # Store data in session state for other pages (if this were a multi-page app)
            st.session_state.df_cleaned_for_display = df_filtered.copy()
            st.session_state.latest_full_year = latest_full_year
            st.session_state.unemployment_avg_df = unemployment_avg_df
            st.session_state.labor_force_avg_df = labor_force_avg_df
            st.session_state.industry_management_avg_df = industry_management_avg_df
            st.session_state.industry_service_avg_df = industry_service_avg_df
            st.session_state.industry_sales_office_avg_df = industry_sales_office_avg_df
            st.session_state.industry_natural_construction_avg_df = industry_natural_construction_avg_df

            if not labor_force_avg_df.empty:
                st.subheader("Average Labor Force by Sex and Race")
                st.plotly_chart(plot_rates_by_sex(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)
                st.plotly_chart(plot_rates_by_race(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)

                st.markdown("---" * 3)
                st.subheader("Management, professional and related occupations")
                if not industry_management_avg_df.empty:
                    # Removed existing plots and added new ones as per user request
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_sex(labor_force_avg_df, industry_management_avg_df, latest_full_year, 'Management, Professional', '#006400'), use_container_width=True)
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_race(labor_force_avg_df, industry_management_avg_df, latest_full_year, 'Management, Professional', '#006400'), use_container_width=True)

                    # New headers for OLS models
                    st.subheader("Mad Liberal Comparisons")
                    st.markdown("#### Check your privilege!")

                else:
                    st.warning("Cannot generate management, professional, and related occupations visualizations, data not available.")

                st.markdown("---" * 3)
                st.subheader("Service Occupations")
                if not industry_service_avg_df.empty:
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_sex(labor_force_avg_df, industry_service_avg_df, latest_full_year, 'Service', '#00008B'), use_container_width=True)
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_race(labor_force_avg_df, industry_service_avg_df, latest_full_year, 'Service', '#00008B'), use_container_width=True)
                    st.subheader("Mad Liberal Comparisons")
                    st.markdown("#### Check your privilege!")
                else:
                    st.warning("Cannot generate Service Occupations visualizations, data not available.")

                st.markdown("---" * 3)
                st.subheader("Sales and Office Occupations")
                if not industry_sales_office_avg_df.empty:
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_sex(labor_force_avg_df, industry_sales_office_avg_df, latest_full_year, 'Sales and Office', '#FF4500'), use_container_width=True)
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_race(labor_force_avg_df, industry_sales_office_avg_df, latest_full_year, 'Sales and Office', '#FF4500'), use_container_width=True)
                    st.subheader("Mad Liberal Comparisons")
                    st.markdown("#### Check your privilege!")
                else:
                    st.warning("Cannot generate Sales and Office Occupations visualizations, data not available.")

                st.markdown("---" * 3)
                st.subheader("Natural resources, construction, and maintenance occupations")
                if not industry_natural_construction_avg_df.empty:
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_sex(labor_force_avg_df, industry_natural_construction_avg_df, latest_full_year, 'Natural resources, construction, and maintenance', '#8B0000'), use_container_width=True)
                    st.plotly_chart(plot_management_proportion_of_labor_force_by_race(labor_force_avg_df, industry_natural_construction_avg_df, latest_full_year, 'Natural resources, construction, and maintenance', '#8B0000'), use_container_width=True)
                    st.subheader("Mad Liberal Comparisons")
                    st.markdown("#### Check your privilege!")
                else:
                    st.warning("Cannot generate Natural resources, construction, and maintenance occupations visualizations, data not available.")

                st.markdown("---" * 3)
                st.subheader("Production, transportation, and material moving occupations")

            else:
                st.warning("Cannot generate labor force visualizations, data not available.")

# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
