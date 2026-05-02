import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import json
from datetime import datetime

# --- Global Streamlit Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Data Loading and Processing Function ---
@st.cache_data
def load_and_process_bls_data():
    headers = {'Content-type': 'application/json'}
    current_year = datetime.now().year
    data = json.dumps({
        "seriesid": [
            'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004', # Existing Unemployment IDs
            'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001', 'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',  # New Labor Force IDs
            'LNU02032526', 'LNU02032468', 'LNU02035886', 'LNU02035918', 'LNU02035957', 'LNU02035874' # New Industry Series IDs
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
            'LNU02035874': 'Employment Level - Management, Professional, Black or African American'
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
            'Employment Level - Management, Professional, Women',
            'Employment Level - Management, Professional, Men',
            'Employment Level - Management, Professional, Asian',
            'Employment Level - Management, Professional, White',
            'Employment Level - Management, Professional, Hispanic or Latino',
            'Employment Level - Management, Professional, Black or African American'
        ]
        # Only apply to unemployment df for consistency as labor_force_avg_df is separate
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

        return df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, industry_management_avg_df
    return pd.DataFrame(), None, pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- Visualization Functions ---
def plot_rates_by_sex(avg_df, year, chart_type_prefix):
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
        base_sex_groups = ['Employment Level - Management, Professional, Men', 'Employment Level - Management, Professional, Women']
        total_men_women_mp = avg_df[avg_df['series_name'].isin(base_sex_groups)]['value'].sum()

        if total_men_women_mp > 0:
            df_sex['proportion'] = df_sex['value'] / total_men_women_mp
        else:
            df_sex['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = 'Proportion of Management, Professional Employment'
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
        base_race_groups = [
            'Employment Level - Management, Professional, White',
            'Employment Level - Management, Professional, Black or African American',
            'Employment Level - Management, Professional, Asian',
            'Employment Level - Management, Professional, Hispanic or Latino'
        ]
        total_race_mp = avg_df[avg_df['series_name'].isin(base_race_groups)]['value'].sum()

        if total_race_mp > 0:
            df_race['proportion'] = df_race['value'] / total_race_mp
        else:
            df_race['proportion'] = 0

        y_column = 'proportion'
        y_axis_label = 'Proportion of Management, Professional Employment'
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
    comparison_order_industry_management = [
        'Employment Level - Management, Professional, Asian',
        'Employment Level - Management, Professional, Men',
        'Employment Level - Management, Professional, Hispanic or Latino',
        'Employment Level - Management, Professional, Black or African American'
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
        'Employment Level - Management, Professional, Asian': 'Management, Professional, Asian',
        'Employment Level - Management, Professional, Men': 'Management, Professional, Men',
        'Employment Level - Management, Professional, Hispanic or Latino': 'Management, Professional, Hispanic or Latino',
        'Employment Level - Management, Professional, Black or African American': 'Management, Professional, Black or African American'
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
            # Update title for unemployment comparisons
            chart_title = f"Average Unemployment: White Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'
            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name, display_comparison_group_name],
                'value': [white_women_avg[y_column], row[y_column]]
            })
        elif chart_type_prefix == 'Labor Force' or chart_type_prefix == 'Employment Level - Management, Professional':
            # For labor force and industry comparisons, we want proportion of overall total if not specified otherwise
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


# Initialize session state to control app flow - always set to industry_visualizations for this isolated app
st.session_state.game_stage = 'industry_visualizations'

# Global layout: left sidebar (20%), main content (60%), right sidebar (20%)
left_sidebar, main_content, right_sidebar = st.columns([0.2, 0.6, 0.2])

with left_sidebar:
    # Navigation buttons (non-functional in this isolated view)
    st.markdown("<div style='display: flex; flex-direction: column; align-items: center; justify-content: space-around; height: 100%;'>", unsafe_allow_html=True)
    st.button("Unemployment Visualizations", key="unemployment_viz_btn_sidebar", use_container_width=True)
    st.button("Industry Visualizations", key="industry_viz_btn_sidebar", use_container_width=True)
    st.button("About this Project", key="about_project_btn_sidebar", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("-" * 3)

with main_content:
    # --- Industry Visualizations Stage ---
    if st.session_state.game_stage == 'industry_visualizations':
        # Force scroll to the top of the main content area when entering this stage
        st.components.v1.html("<script>window.top.scroll(0, 0);</script>", height=0, width=0)

        viz_col = st.columns([1]) # Use a single column for visualizations in main_content

        with viz_col[0]:
            df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, industry_management_avg_df = load_and_process_bls_data()

            # Store data in session state for other pages (if this were a multi-page app)
            st.session_state.df_cleaned_for_display = df_filtered.copy()
            st.session_state.latest_full_year = latest_full_year
            st.session_state.unemployment_avg_df = unemployment_avg_df
            st.session_state.labor_force_avg_df = labor_force_avg_df
            st.session_state.industry_management_avg_df = industry_management_avg_df

            if not labor_force_avg_df.empty:
                st.subheader("Average Labor Force by Sex and Race")
                st.plotly_chart(plot_rates_by_sex(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)
                st.plotly_chart(plot_rates_by_race(labor_force_avg_df, latest_full_year, 'Labor Force'), use_container_width=True)

                st.markdown("--- ")
                st.subheader("Management, professional and related occupations")
                if not industry_management_avg_df.empty:
                    st.plotly_chart(plot_rates_by_sex(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional'), use_container_width=True)
                    st.plotly_chart(plot_rates_by_race(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional'), use_container_width=True)
                    st.subheader("Mad Liberal Comparisons for Management, Professional, and Related Occupations")
                    industry_comparison_charts = plot_rate_comparisons(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional')
                    for chart in industry_comparison_charts:
                        st.plotly_chart(chart, use_container_width=True)
                else:
                    st.warning("Cannot generate management, professional, and related occupations visualizations, data not available.")

                st.markdown("--- ")
                st.subheader("Service Occupations")

                st.markdown("--- ")
                st.subheader("Sales and Office Occupations")

                st.markdown("--- ")
                st.subheader("Natural resources, construction, and maintenance occupations")

                st.markdown("--- ")
                st.subheader("Production, transportation, and material moving occupations")

            else:
                st.warning("Cannot generate labor force visualizations, data not available.")

# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
