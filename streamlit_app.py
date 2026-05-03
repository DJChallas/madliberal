import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
import random
import requests
import json
from datetime import datetime

# --- Global Streamlit Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Define Real Story Variables Globally ---
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
    data = json.dumps({
        "seriesid": [
            'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004', # Existing Unemployment IDs
            'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001', 'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',  # New Labor Force IDs
            'LNU02032526', 'LNU02032468', # Management, Professional, and Related Occupations - Sex
            'LNU02032539', 'LNU02032481', # Service Occupations - Sex
            'LNU02032545', 'LNU02032487', # Sales and Office Occupations - Sex
            'LNU02032490', 'LNU02032548', # Natural Resources, Construction, and Maintenance Occupations - Sex
            'LNU02032554', 'LNU02032496'  # Transportation and Material Moving Occupations - Sex
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
            # Industry Series - Management, Professional, and Related Occupations - Sex
            'LNU02032526': 'Employment Level - Management, Professional - Women',
            'LNU02032468': 'Employment Level - Management, Professional - Men',
            # Industry Series - Service Occupations - Sex
            'LNU02032539': 'Employment Level - Service Occupations - Women',
            'LNU02032481': 'Employment Level - Service Occupations - Men',
            # Industry Series - Sales and Office Occupations - Sex
            'LNU02032545': 'Employment Level - Sales and Office Occupations - Women',
            'LNU02032487': 'Employment Level - Sales and Office Occupations - Men',
            # Industry Series - Natural Resources, Construction, and Maintenance Occupations - Sex
            'LNU02032490': 'Employment Level - Natural Resources, Construction, and Maintenance - Men',
            'LNU02032548': 'Employment Level - Natural Resources, Construction, and Maintenance - Women',
            # Industry Series - Transportation and Material Moving Occupations - Sex
            'LNU02032554': 'Employment Level - Transportation and Material Moving - Women',
            'LNU02032496': 'Employment Level - Transportation and Material Moving - Men'
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

        # Separate unemployment and labor force dataframes
        unemployment_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Unemployment')].copy()
        labor_force_avg_df = avg_rates_latest_year[avg_rates_latest_year['series_name'].str.contains('Labor Force')].copy()

        # Filter industry-specific dataframes to only include sex-related series
        industry_management_avg_df = avg_rates_latest_year[
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Management, Professional - Men') |
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Management, Professional - Women')
        ].copy()
        industry_service_avg_df = avg_rates_latest_year[
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Service Occupations - Men') |
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Service Occupations - Women')
        ].copy()
        industry_sales_office_avg_df = avg_rates_latest_year[
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Sales and Office Occupations - Men') |
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Sales and Office Occupations - Women')
        ].copy()
        industry_natural_resources_avg_df = avg_rates_latest_year[
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Natural Resources, Construction, and Maintenance - Men') |
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Natural Resources, Construction, and Maintenance - Women')
        ].copy()
        industry_transportation_avg_df = avg_rates_latest_year[
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Transportation and Material Moving - Men') |
            avg_rates_latest_year['series_name'].str.contains('Employment Level - Transportation and Material Moving - Women')
        ].copy()

        # Calculate 'proportion' for labor_force_avg_df for display in About page
        if not labor_force_avg_df.empty:
            total_labor_force_sum = labor_force_avg_df['value'].sum()
            if total_labor_force_sum > 0:
                labor_force_avg_df['proportion'] = labor_force_avg_df['value'] / total_labor_force_sum
            else:
                labor_force_avg_df['proportion'] = 0.0 # Assign 0.0 if sum is zero

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
            'Employment Level - Management, Professional - Women',
            'Employment Level - Management, Professional - Men',
            'Employment Level - Service Occupations - Women',
            'Employment Level - Service Occupations - Men',
            'Employment Level - Sales and Office Occupations - Women',
            'Employment Level - Sales and Office Occupations - Men',
            'Employment Level - Natural Resources, Construction, and Maintenance - Women',
            'Employment Level - Natural Resources, Construction, and Maintenance - Men',
            'Employment Level - Transportation and Material Moving - Women',
            'Employment Level - Transportation and Material Moving - Men'
        ]
        unemployment_avg_df['series_name'] = pd.Categorical(
            unemployment_avg_df['series_name'],
            categories=desired_order, # Only apply to unemployment df for consistency as labor_force_avg_df is separate
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

        for df_name_to_sort in [industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, industry_natural_resources_avg_df, industry_transportation_avg_df]:
            df_name_to_sort['series_name'] = pd.Categorical(
                df_name_to_sort['series_name'],
                categories=desired_order,
                ordered=True
            )
            # Re-assign the sorted dataframe back to its original variable
            if df_name_to_sort is industry_management_avg_df:
                industry_management_avg_df = df_name_to_sort.sort_values('series_name')
            elif df_name_to_sort is industry_service_avg_df:
                industry_service_avg_df = df_name_to_sort.sort_values('series_name')
            elif df_name_to_sort is industry_sales_office_avg_df:
                industry_sales_office_avg_df = df_name_to_sort.sort_values('series_name')
            elif df_name_to_sort is industry_natural_resources_avg_df:
                industry_natural_resources_avg_df = df_name_to_sort.sort_values('series_name')
            elif df_name_to_sort is industry_transportation_avg_df:
                industry_transportation_avg_df = df_name_to_sort.sort_values('series_name')

        return df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, \
               industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, \
               industry_natural_resources_avg_df, industry_transportation_avg_df
    return pd.DataFrame(), None, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- Visualization Functions ---
def plot_rates_by_sex(avg_df, year, chart_type_prefix):
    # Adjust sex_groups generation to handle 'Employment Level' chart types correctly
    if chart_type_prefix.startswith('Employment Level'): # More generic condition
        sex_groups = [f'{chart_type_prefix} - Men', f'{chart_type_prefix} - Women']
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
    elif chart_type_prefix.startswith('Employment Level'): # More generic condition
        base_sex_groups = [f'{chart_type_prefix} - Men', f'{chart_type_prefix} - Women']
        total_men_women_mp = avg_df[avg_df['series_name'].isin(base_sex_groups)]['value'].sum()

        if total_men_women_mp > 0:
            df_sex['proportion'] = df_sex['value'] / total_men_women_mp
        else:
            df_sex['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = 'Proportion of Employment Level' # Dynamically set label
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

def plot_rates_by_race(avg_df, year, chart_type_prefix):
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
    # The 'Employment Level - Management, Professional' race plotting block is removed

    df_race = df_race.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_race,
        x='series_name',
        y=y_column,
        title=f'Average {chart_type_prefix} by Race in {year}',
        labels={'series_name': 'Demographic Group', y_column: y_axis_label},
        color='series_name',
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

def plot_rate_comparisons(avg_df, year, chart_type_prefix):
    white_women_avg_series_name = f'{chart_type_prefix} - White Women'
    if white_women_avg_series_name not in avg_df['series_name'].values:
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
    # Removed race-related entries for industry management comparison
    comparison_order_industry_management = [
        'Employment Level - Management, Professional - Men'
    ]

    if chart_type_prefix == 'Unemployment':
        comparison_order = comparison_order_unemployment
    elif chart_type_prefix == 'Labor Force':
        comparison_order = comparison_order_labor_force
    elif chart_type_prefix == 'Employment Level - Management, Professional':
        comparison_order = comparison_order_industry_management
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
        'Employment Level - Management, Professional - Men': 'Management, Professional - Men'
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
        elif chart_type_prefix == 'Labor Force' or chart_type_prefix.startswith('Employment Level'): # Generic for all employment levels
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

        fig = px.bar(
            comparison_df,
            x='series_name',
            y=y_column,
            title=chart_title,
            labels={'series_name': 'Demographic Group', y_column: y_axis_label},
            color='series_name',
            text_auto=text_auto_format if text_auto_format else False
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

# --- New: Logit Regression and Sigmoid Plotting Functions ---
def perform_logit_regression(industry_data_df, industry_title, labor_force_df):
    if industry_data_df.empty or labor_force_df.empty:
        return None, None, None, None, "Insufficient data for Logit Regression. No data available for the selected industry or labor force."

    # Filter for the relevant industry employment data (Men/Women)
    men_employment_value = industry_data_df[industry_data_df['series_name'].str.contains(' - Men')]['value'].mean()
    women_employment_value = industry_data_df[industry_data_df['series_name'].str.contains(' - Women')]['value'].mean()

    if pd.isna(men_employment_value) or pd.isna(women_employment_value):
        return None, None, None, None, "Insufficient employment data for men or women in this industry."

    # Get total labor force for men and women from the labor_force_df
    total_labor_force_men = labor_force_df[labor_force_df['series_name'] == 'Labor Force - Men']['value'].mean()
    total_labor_force_women = labor_force_df[labor_force_df['series_name'] == 'Labor Force - Women']['value'].mean()

    if pd.isna(total_labor_force_men) or pd.isna(total_labor_force_women):
        return None, None, None, None, "Insufficient total labor force data for men or women."

    simulated_data = []

    # Add 'employed' individuals, scaled up for more observations
    scale_factor = 100 # Increase this for more 'individuals' for better regression fitting
    num_employed_men = int(men_employment_value * scale_factor)
    num_employed_women = int(women_employment_value * scale_factor)

    for _ in range(num_employed_men):
        simulated_data.append({'is_female': 0, 'is_employed_in_industry': 1})
    for _ in range(num_employed_women):
        simulated_data.append({'is_female': 1, 'is_employed_in_industry': 1})

    # Calculate 'not employed' individuals
    num_not_employed_men = int(max(0, (total_labor_force_men - men_employment_value) * scale_factor))
    num_not_employed_women = int(max(0, (total_labor_force_women - women_employment_value) * scale_factor))

    for _ in range(num_not_employed_men):
        simulated_data.append({'is_female': 0, 'is_employed_in_industry': 0})
    for _ in range(num_not_employed_women):
        simulated_data.append({'is_female': 1, 'is_employed_in_industry': 0})

    simulated_df = pd.DataFrame(simulated_data)

    if len(simulated_df) == 0 or simulated_df['is_employed_in_industry'].nunique() < 2 or simulated_df['is_female'].nunique() < 2:
        return None, None, None, None, "Simulated data lacks variation for regression."

    y = simulated_df['is_employed_in_industry']
    X = simulated_df['is_female']
    X = sm.add_constant(X)

    try:
        logit_model = sm.Logit(y, X)
        result = logit_model.fit(disp=False) # disp=False to suppress verbose output in Streamlit

        # Odds ratio for 'is_female'
        odds_ratio_female = np.exp(result.params['is_female'])

        # Predicted probabilities
        prob_man = 1 / (1 + np.exp(-(result.params['const'] + result.params['is_female'] * 0)))
        prob_woman = 1 / (1 + np.exp(-(result.params['const'] + result.params['is_female'] * 1)))

        return result, prob_man, prob_woman, odds_ratio_female, None
    except Exception as e:
        return None, None, None, None, f"Logit Regression failed: {e}"

def plot_sigmoid_curve(result, prob_man, prob_woman, industry_title):
    if result is None:
        return None

    const = result.params['const']
    is_female_coeff = result.params['is_female']

    def sigmoid(x):
        return 1 / (1 + np.exp(-(const + is_female_coeff * x)))

    x_vals = np.linspace(-0.5, 1.5, 500) # Extend slightly beyond 0 and 1
    y_vals = sigmoid(x_vals)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label='Sigmoid Curve (Predicted Probability)', color='blue')

    # Mark the predicted probabilities
    ax.scatter(0, prob_man, color='red', s=100, zorder=5, label=f'Men (Prob: {prob_man:.2%})')
    ax.scatter(1, prob_woman, color='green', s=100, zorder=5, label=f'Women (Prob: {prob_woman:.2%})')

    # Add vertical and horizontal lines
    ax.vlines(0, 0, prob_man, linestyle='--', color='red', alpha=0.6)
    ax.hlines(prob_man, -0.5, 0, linestyle='--', color='red', alpha=0.6)
    ax.vlines(1, 0, prob_woman, linestyle='--', color='green', alpha=0.6)
    ax.hlines(prob_woman, -0.5, 1, linestyle='--', color='green', alpha=0.6)

    ax.set_title(f'Predicted Probabilities of Employment in {industry_title}')
    ax.set_xlabel('Is Female (0=Male, 1=Female)')
    ax.set_ylabel('Predicted Probability of Employment')
    ax.grid(True)
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0, 1], ['Male', 'Female'])
    plt.tight_layout()
    return fig


# --- Streamlit App ---
col_title_global, col_subtitle_global = st.columns([0.3, 0.7])
with col_title_global:
    st.markdown("<div style='background-color:red; padding: 2px; border-radius: 10px;'><h1 style='color:white; text-align:center; margin: 0; padding: 0;'>Mad Liberal</h1></div>", unsafe_allow_html=True)
with col_subtitle_global:
    st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 5px 0;'>
            <h4 style='color:blue; text-align:left; margin: 0; padding: 0;'>Python Programming by Casey Hallas for UNO Econ 8320 - May 2026</h4>
            <h4 style='color:black; text-align:left; margin: 0; padding: 0;'>Data collected from The US Bureau of Labor Statistics, www.bls.gov</h4>
        </div>
    """, unsafe_allow_html=True)


# Initialize session state to control app flow - directly set to industry visualizations
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 'industry_visualizations'

# Global layout: left sidebar (20%), main content (60%), right sidebar (20%)
left_sidebar, main_content, right_sidebar = st.columns([0.2, 0.6, 0.2])

with left_sidebar:
    # Only display 'The Real Story' in the left sidebar for visualization stages
    st.subheader("The Real Story:")
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From <b>{real_proper_noun_1}</b> to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

    st.markdown("-" * 3)

with main_content:
    # Force scroll to the top of the main content area when entering this stage
    st.components.v1.html("<script>window.top.scroll(0, 0);</script>", height=0, width=0)

    viz_col = st.columns([1]) # Use a single column for visualizations in main_content

    with viz_col[0]:
        st.subheader("Industry Visualizations about Sex")
        st.markdown("The US Census Bureau website provides statistics for race in the United States at the current levels: White Alone 74.8&, Black Alone 13.7%, Asian Alone 6.7%, Hispanic or Latino Alone 20%. To calculate our totals we applied data based on seasonal employment rates averaged and totaled - White, Asian, Black or African American and Hispanic or Latino based on the Civilian Labor Force Level. That is to create an active comparison to employment levels by industry against a measurable estimate provided by the BLS.")
        st.markdown("The Department of Labor presents a measure of data called Employed people by detailed occupation, sex, race, and Hispanic or Latino ethnicity (https://www.bls.gov/cps/cpsaat11.htm) that presents percentages of demographics employed in each of those occupations, grouped by industry. I’ve collected data for the primary Industries for gender and race to compare the distribution of demographics across the entire US job market, including the most popular occupations in all 4 categories.")

        df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, \
        industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, \
        industry_natural_resources_avg_df, industry_transportation_avg_df = load_and_process_bls_data()

        # Store data in session state for other pages
        st.session_state.df_cleaned_for_display = df_filtered.copy()
        st.session_state.latest_full_year = latest_full_year
        st.session_state.unemployment_avg_df = unemployment_avg_df
        st.session_state.labor_force_avg_df = labor_force_avg_df
        st.session_state.industry_management_avg_df = industry_management_avg_df
        st.session_state.industry_service_avg_df = industry_service_avg_df
        st.session_state.industry_sales_office_avg_df = industry_sales_office_avg_df
        st.session_state.industry_natural_resources_avg_df = industry_natural_resources_avg_df
        st.session_state.industry_transportation_avg_df = industry_transportation_avg_df

        if not labor_force_avg_df.empty:
            st.subheader("Average Labor Force by Sex and Race")
            st.plotly_chart(plot_rates_by_sex(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)
            st.plotly_chart(plot_rates_by_race(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)

            st.markdown("--- ")
            
            # --- Management, Professional, and Related Occupations ---
            industry_title_mp = 'Management, Professional, and Related Occupations'
            st.subheader(industry_title_mp)
            st.plotly_chart(plot_rates_by_sex(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional'), use_container_width=True)
            
            # Logit Regression and Sigmoid Plot for Management, Professional
            result_mp, prob_man_mp, prob_woman_mp, odds_ratio_female_mp, error_mp = perform_logit_regression(industry_management_avg_df, industry_title_mp, labor_force_avg_df)
            if result_mp is not None:
                st.write(f"### Logit Regression: Predicted Probabilities of Employment in {industry_title_mp}")
                st.text(result_mp.summary())
                st.write("### Interpretation")
                st.markdown("The coefficients from the logit model are in log-odds. To interpret them in terms of probability, we can calculate the odds ratios or predicted probabilities.")
                st.write(f"- Odds Ratio for Female (vs. Male): {odds_ratio_female_mp:.2f}")
                if odds_ratio_female_mp > 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_mp}' are approximately {odds_ratio_female_mp:.2f} times higher for women compared to men, holding other factors constant.")
                elif odds_ratio_female_mp < 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_mp}' are approximately {1/odds_ratio_female_mp:.2f} times lower for women compared to men, holding other factors constant.")
                else:
                    st.write("  - The odds of employment are similar for men and women.")
                st.write(f"- Predicted Probability of Employment for Men: {prob_man_mp:.2%}")
                st.write(f"- Predicted Probability of Employment for Women: {prob_woman_mp:.2%}")
                st.markdown("**Note:** This analysis uses a simulated dataset derived from aggregated BLS employment levels to fit the logit model. For a precise and robust analysis, individual-level survey data would be required.")

                fig_sigmoid_mp = plot_sigmoid_curve(result_mp, prob_man_mp, prob_woman_mp, industry_title_mp)
                if fig_sigmoid_mp is not None:
                    st.pyplot(fig_sigmoid_mp)
            else:
                st.warning(error_mp)


            st.markdown("--- ")
            
            # --- Service Occupations ---
            industry_title_service = 'Service Occupations'
            st.subheader(industry_title_service)
            st.plotly_chart(plot_rates_by_sex(industry_service_avg_df, latest_full_year, 'Employment Level - Service Occupations'), use_container_width=True)
            
            # Logit Regression and Sigmoid Plot for Service Occupations
            result_service, prob_man_service, prob_woman_service, odds_ratio_female_service, error_service = perform_logit_regression(industry_service_avg_df, industry_title_service, labor_force_avg_df)
            if result_service is not None:
                st.write(f"### Logit Regression: Predicted Probabilities of Employment in {industry_title_service}")
                st.text(result_service.summary())
                st.write("### Interpretation")
                st.markdown("The coefficients from the logit model are in log-odds. To interpret them in terms of probability, we can calculate the odds ratios or predicted probabilities.")
                st.write(f"- Odds Ratio for Female (vs. Male): {odds_ratio_female_service:.2f}")
                if odds_ratio_female_service > 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_service}' are approximately {odds_ratio_female_service:.2f} times higher for women compared to men, holding other factors constant.")
                elif odds_ratio_female_service < 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_service}' are approximately {1/odds_ratio_female_service:.2f} times lower for women compared to men, holding other factors constant.")
                else:
                    st.write("  - The odds of employment are similar for men and women.")
                st.write(f"- Predicted Probability of Employment for Men: {prob_man_service:.2%}")
                st.write(f"- Predicted Probability of Employment for Women: {prob_woman_service:.2%}")
                st.markdown("**Note:** This analysis uses a simulated dataset derived from aggregated BLS employment levels to fit the logit model. For a precise and robust analysis, individual-level survey data would be required.")

                fig_sigmoid_service = plot_sigmoid_curve(result_service, prob_man_service, prob_woman_service, industry_title_service)
                if fig_sigmoid_service is not None:
                    st.pyplot(fig_sigmoid_service)
            else:
                st.warning(error_service)


            st.markdown("--- ")
            
            # --- Sales and Office Occupations ---
            industry_title_sales_office = 'Sales and Office Occupations'
            st.subheader(industry_title_sales_office)
            st.plotly_chart(plot_rates_by_sex(industry_sales_office_avg_df, latest_full_year, 'Employment Level - Sales and Office Occupations'), use_container_width=True)

            # Logit Regression and Sigmoid Plot for Sales and Office Occupations
            result_sales_office, prob_man_sales_office, prob_woman_sales_office, odds_ratio_female_sales_office, error_sales_office = perform_logit_regression(industry_sales_office_avg_df, industry_title_sales_office, labor_force_avg_df)
            if result_sales_office is not None:
                st.write(f"### Logit Regression: Predicted Probabilities of Employment in {industry_title_sales_office}")
                st.text(result_sales_office.summary())
                st.write("### Interpretation")
                st.markdown("The coefficients from the logit model are in log-odds. To interpret them in terms of probability, we can calculate the odds ratios or predicted probabilities.")
                st.write(f"- Odds Ratio for Female (vs. Male): {odds_ratio_female_sales_office:.2f}")
                if odds_ratio_female_sales_office > 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_sales_office}' are approximately {odds_ratio_female_sales_office:.2f} times higher for women compared to men, holding other factors constant.")
                elif odds_ratio_female_sales_office < 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_sales_office}' are approximately {1/odds_ratio_female_sales_office:.2f} times lower for women compared to men, holding other factors constant.")
                else:
                    st.write("  - The odds of employment are similar for men and women.")
                st.write(f"- Predicted Probability of Employment for Men: {prob_man_sales_office:.2%}")
                st.write(f"- Predicted Probability of Employment for Women: {prob_woman_sales_office:.2%}")
                st.markdown("**Note:** This analysis uses a simulated dataset derived from aggregated BLS employment levels to fit the logit model. For a precise and robust analysis, individual-level survey data would be required.")

                fig_sigmoid_sales_office = plot_sigmoid_curve(result_sales_office, prob_man_sales_office, prob_woman_sales_office, industry_title_sales_office)
                if fig_sigmoid_sales_office is not None:
                    st.pyplot(fig_sigmoid_sales_office)
            else:
                st.warning(error_sales_office)

            st.markdown("--- ")
            
            # --- Natural resources, construction, and maintenance occupations ---
            industry_title_natural_resources = 'Natural resources, construction, and maintenance occupations'
            st.subheader(industry_title_natural_resources)
            st.plotly_chart(plot_rates_by_sex(industry_natural_resources_avg_df, latest_full_year, 'Employment Level - Natural Resources, Construction, and Maintenance'), use_container_width=True)
            
            # Logit Regression and Sigmoid Plot for Natural resources, construction, and maintenance occupations
            result_natural_resources, prob_man_natural_resources, prob_woman_natural_resources, odds_ratio_female_natural_resources, error_natural_resources = perform_logit_regression(industry_natural_resources_avg_df, industry_title_natural_resources, labor_force_avg_df)
            if result_natural_resources is not None:
                st.write(f"### Logit Regression: Predicted Probabilities of Employment in {industry_title_natural_resources}")
                st.text(result_natural_resources.summary())
                st.write("### Interpretation")
                st.markdown("The coefficients from the logit model are in log-odds. To interpret them in terms of probability, we can calculate the odds ratios or predicted probabilities.")
                st.write(f"- Odds Ratio for Female (vs. Male): {odds_ratio_female_natural_resources:.2f}")
                if odds_ratio_female_natural_resources > 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_natural_resources}' are approximately {odds_ratio_female_natural_resources:.2f} times higher for women compared to men, holding other factors constant.")
                elif odds_ratio_female_natural_resources < 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_natural_resources}' are approximately {1/odds_ratio_female_natural_resources:.2f} times lower for women compared to men, holding other factors constant.")
                else:
                    st.write("  - The odds of employment are similar for men and women.")
                st.write(f"- Predicted Probability of Employment for Men: {prob_man_natural_resources:.2%}")
                st.write(f"- Predicted Probability of Employment for Women: {prob_woman_natural_resources:.2%}")
                st.markdown("**Note:** This analysis uses a simulated dataset derived from aggregated BLS employment levels to fit the logit model. For a precise and robust analysis, individual-level survey data would be required.")

                fig_sigmoid_natural_resources = plot_sigmoid_curve(result_natural_resources, prob_man_natural_resources, prob_woman_natural_resources, industry_title_natural_resources)
                if fig_sigmoid_natural_resources is not None:
                    st.pyplot(fig_sigmoid_natural_resources)
            else:
                st.warning(error_natural_resources)

            st.markdown("--- ")
            
            # --- Production, transportation, and material moving occupations ---
            industry_title_transportation = 'Production, transportation, and material moving occupations'
            st.subheader(industry_title_transportation)
            st.plotly_chart(plot_rates_by_sex(industry_transportation_avg_df, latest_full_year, 'Employment Level - Transportation and Material Moving'), use_container_width=True)

            # Logit Regression and Sigmoid Plot for Production, transportation, and material moving occupations
            result_transportation, prob_man_transportation, prob_woman_transportation, odds_ratio_female_transportation, error_transportation = perform_logit_regression(industry_transportation_avg_df, industry_title_transportation, labor_force_avg_df)
            if result_transportation is not None:
                st.write(f"### Logit Regression: Predicted Probabilities of Employment in {industry_title_transportation}")
                st.text(result_transportation.summary())
                st.write("### Interpretation")
                st.markdown("The coefficients from the logit model are in log-odds. To interpret them in terms of probability, we can calculate the odds ratios or predicted probabilities.")
                st.write(f"- Odds Ratio for Female (vs. Male): {odds_ratio_female_transportation:.2f}")
                if odds_ratio_female_transportation > 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_transportation}' are approximately {odds_ratio_female_transportation:.2f} times higher for women compared to men, holding other factors constant.")
                elif odds_ratio_female_transportation < 1:
                    st.write(f"  - This means that the odds of being employed in '{industry_title_transportation}' are approximately {1/odds_ratio_female_transportation:.2f} times lower for women compared to men, holding other factors constant.")
                else:
                    st.write("  - The odds of employment are similar for men and women.")
                st.write(f"- Predicted Probability of Employment for Men: {prob_man_transportation:.2%}")
                st.write(f"- Predicted Probability of Employment for Women: {prob_woman_transportation:.2%}")
                st.markdown("**Note:** This analysis uses a simulated dataset derived from aggregated BLS employment levels to fit the logit model. For a precise and robust analysis, individual-level survey data would be required.")

                fig_sigmoid_transportation = plot_sigmoid_curve(result_transportation, prob_man_transportation, prob_woman_transportation, industry_title_transportation)
                if fig_sigmoid_transportation is not None:
                    st.pyplot(fig_sigmoid_transportation)
            else:
                st.warning(error_transportation)

        else:
            st.warning("Cannot generate labor force visualizations, data not available.")


# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
