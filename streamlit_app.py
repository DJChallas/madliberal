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
    data = json.dumps({
        "seriesid": [
            'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004', # Existing Unemployment IDs
            'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001', 'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',  # Existing Labor Force IDs
            # New Employment Level IDs for Occupations
            'LNU02032526', 'LNU02032468', # Management, Professional, and Related Occupations, Women and Men
            'LNU02032539', 'LNU02032481', # Service Occupations, Women and Men
            'LNU02032545', 'LNU02032487', # Sales and Office Occupations, Women and Men
            'LNU02032490', 'LNU02032548', # Natural Resources, Construction, and Maintenance Occupations, Men and Women
            'LNU02032554', 'LNU02032496'  # Transportation and Material Moving Occupations, Women and Men
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
            # New Employment Level Series for Occupations
            'LNU02032526': 'Management, Professional, and Related Occupations - Women',
            'LNU02032468': 'Management, Professional, and Related Occupations - Men',
            'LNU02032539': 'Service Occupations - Women',
            'LNU02032481': 'Service Occupations - Men',
            'LNU02032545': 'Sales and Office Occupations - Women',
            'LNU02032487': 'Sales and Office Occupations - Men',
            'LNU02032490': 'Natural Resources, Construction, and Maintenance Occupations - Men',
            'LNU02032548': 'Natural Resources, Construction, and Maintenance Occupations - Women',
            'LNU02032554': 'Transportation and Material Moving Occupations - Women',
            'LNU02032496': 'Transportation and Material Moving Occupations - Men'
        }
        series_name_mapping = sn_map

        # Add series_name to df_filtered
        df_filtered['series_name'] = df_filtered['series_id'].map(series_name_mapping)

        # The following calculations will now be done where the data is used in the Streamlit app
        latest_full_year = df_filtered['year'].astype(int).max()
        if latest_full_year == datetime.now().year:
            latest_full_year -= 1 # Use the last full year if current year is not complete

        return df_filtered, latest_full_year, series_name_mapping
    return pd.DataFrame(), None, {}

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

    # Create a new column for simplified display names
    df_race['display_name'] = df_race['series_name'].apply(lambda x: x.replace(f'{chart_type_prefix} - ', ''))

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

    df_race = df_race.sort_values(by=y_column, ascending=False)

    fig = px.bar(
        df_race,
        x='display_name', # Use the new display_name column for x-axis
        y=y_column,
        title=f'Average {chart_type_prefix} by Race in {year}',
        labels={'display_name': 'Demographic Group', y_column: y_axis_label}, # Update label key
        color='display_name',
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
    comparison_order = comparison_order_unemployment if chart_type_prefix == 'Unemployment' else comparison_order_labor_force

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
        'Labor Force - Black or African American': 'Black or African American, Men/Women'
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
        elif chart_type_prefix == 'Labor Force':
            # For labor force comparisons, we want proportion of overall total if not specified otherwise
            # This requires recalculating the overall total if not already done
            total_lf_value = avg_df['value'].sum()
            if total_lf_value > 0:
                # Ensure we are using the 'value' column from avg_df for proportions here
                white_women_proportion = white_women_avg['value'] / total_lf_value
                row_proportion = row['value'] / total_lf_value
            else:
                white_women_proportion = 0
                row_proportion = 0

            y_column = 'proportion'
            y_axis_label = 'Proportion of Total Labor Force'
            chart_title = f"Average {chart_type_prefix}: White Women vs. {display_comparison_group_name} in {year}"
            tick_format = '.1%'
            text_auto_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name, display_comparison_group_name],
                'proportion': [white_women_proportion, row_proportion]
            })
        # The `else` block for `comparison_df` was removed as it's now explicitly handled.

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

def plot_employment_by_occupation_and_sex(df_filtered, latest_full_year, category_name, series_ids_women, series_ids_men, series_name_mapping):
    # Filter data for the specific category and latest full year
    category_df = df_filtered[
        (df_filtered['series_id'].isin(series_ids_women + series_ids_men)) &
        (df_filtered['year'].astype(int) == latest_full_year)
    ].copy()

    if category_df.empty:
        st.warning(f"No data available for {category_name} in {latest_full_year}.")
        return

    # Calculate the average value for the latest full year for each series
    avg_employment_df = category_df.groupby('series_id')['value'].mean().reset_index()
    avg_employment_df['series_name'] = avg_employment_df['series_id'].map(series_name_mapping)

    # Determine the gender based on series_name (assuming 'Women' or 'Men' in name)
    avg_employment_df['gender'] = avg_employment_df['series_name'].apply(lambda x: 'Women' if 'Women' in x else 'Men')

    # Create the bar chart
    fig = px.bar(
        avg_employment_df,
        x='gender',
        y='value',
        color='gender',
        title=f'Average Employment Level in {category_name} by Sex ({latest_full_year})',
        labels={'gender': 'Sex', 'value': 'Average Employment Level (in thousands)'},
        text='value',
        category_orders={'gender': ['Men', 'Women']}
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(yaxis_title='Average Employment Level (in thousands)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


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


# Initialize session state to control app flow
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 'madlib_input'

# Global layout: left sidebar (20%), main content (60%), right sidebar (20%)
left_sidebar, main_content, right_sidebar = st.columns([0.2, 0.6, 0.2])

with left_sidebar:
    # "Proceed to Visualizations" button, only for 'madlib_reveal' stage, at the very top of the left sidebar
    if st.session_state.game_stage == 'madlib_reveal':
        if st.button("Proceed to Visualizations", key="proceed_from_left_sidebar", use_container_width=True):
            st.session_state.game_stage = 'visualizations'
            st.rerun()

    # Regular navigation buttons, only displayed when NOT in madlib input/reveal stages
    if st.session_state.game_stage not in ['madlib_input', 'madlib_reveal']:
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center; justify: space-around; height: 100%;'>", unsafe_allow_html=True)
        if st.button("Unemployment Visualizations", key="unemployment_viz_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'visualizations'
            st.rerun()
        if st.button("Industry Visualizations", key="industry_viz_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'industry_visualizations'
            st.rerun()
        if st.button("About this Project", key="about_project_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'about_project'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Content that appears during madlib_input or madlib_reveal (stripes and collage)
    if st.session_state.game_stage == 'madlib_input' or st.session_state.game_stage == 'madlib_reveal': # Show stripes and collage in input/reveal stages
        # Add alternating red and white stripes
        for i in range(45):
            color = "red" if i % 2 == 0 else "#FFFFFF"
            st.markdown(f'<div style="height: 20px; background-color: {color}; width: 100%; margin: 0; padding: 0;"></div>', unsafe_allow_html=True)

        # Only display collage in madlib_input stage, not madlib_reveal
        if st.session_state.game_stage == 'madlib_input':
            display_text_collage()


    elif st.session_state.game_stage == 'visualizations' or st.session_state.game_stage == 'industry_visualizations': # Show 'The Real Story' and navigation in left sidebar for visualization stages
        st.subheader("The Real Story:")
        st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From <b>{real_proper_noun_1}</b> to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

        st.markdown("-" * 3)

    # REMOVED: elif st.session_state.game_stage == 'about_project': # Show 'Collage' and navigation in left sidebar
    # REMOVED:     display_text_collage()
    # REMOVED:     st.markdown("-" * 3) # Separator

with main_content:
    # --- Mad Lib Input Stage ---
    if st.session_state.game_stage == 'madlib_input':
        with st.form("madlib_form"):
            input_fields_all = [
                ("Noun 1", "noun_1"),
                ("Noun 2", "noun_2"),
                ("Noun 3", "noun_3"),
                ("Noun 4", "noun_4"),
                ("Plural Noun 1", "noun_resource"),
                ("Plural Noun 2", "noun_society_plural"),

                ("Proper Noun 2", "proper_noun_2"),
                ("Plural Noun 3", "plural_noun_3"),
                ("Adjective 1", "adjective_1"),
                ("Noun 5", "noun_5"),
                ("Noun 6", "noun_6"),
                ("Plural Noun 4", "plural_noun_4"),
                ("Plural Noun 5", "plural_noun_5"),
                ("Noun 7", "noun_7"),

                ("Adjective 2", "adjective_2"),
                ("Noun 8", "noun_8"),
                ("Noun 9", "noun_9"),
                ("Proper Noun 3", "proper_noun_3"),
                ("Noun 10", "noun_10"),
                ("Noun 11", "noun_11"),
                ("Noun 12", "noun_12"),

                ("Adjective 3", "adjective_3"),
                ("Noun 13", "noun_13"),
                ("Noun 14", "noun_14"),
                ("Noun 15", "noun_15"),
                ("Adverb 1", "adverb_1"),
                ("Noun 16", "noun_16"),
                ("Noun 17", "noun_17"),
                ("Verb 1", "verb_2"),
                ("Adjective 4", "adjective_4"),
                ("Noun 18", "noun_18"),
                ("Verb 2", "verb_3"),
                ("Noun 19", "noun_19"),
                ("Noun 20", "noun_20"),
                ("Noun 21", "noun_21"),
                ("Noun 22", "noun_22"),
                ("Noun 23", "noun_23"),
                ("Noun 24", "noun_24"),
                ("Adjective 5", "adjective_5"),
                ("Noun 25", "noun_25"),
                ("Proper Noun 4", "proper_noun_4"),
                ("Noun 26", "noun_26"),
                ("Noun 27", "noun_27"),
                ("Noun 28", "noun_28"),
                ("Verb 3", "verb_4"),
                ("Noun 29", "noun_29"),
                ("Noun 30", "noun_30"),
                ("Noun 31", "noun_31"),
            ]

            # Define default values for the Mad Lib form
            default_madlib_values = {
                "noun_1": "lipstick",
                "noun_2": "mallspace",
                "noun_3": "groupthink",
                "noun_4": "DM's",
                "noun_resource": "donations",
                "noun_society_plural": "Onlyfans pages",
                "proper_noun_2": "2010's",
                "plural_noun_3": "nightclubs",
                "adjective_1": "super",
                "noun_5": "discount",
                "noun_6": "Lady's Night",
                "plural_noun_4": "sidepieces",
                "plural_noun_5": "attractive",
                "noun_7": "divas",
                "adjective_2": "guestlist",
                "noun_8": "vodka",
                "noun_9": "vodka",
                "proper_noun_3": "potatoes",
                "noun_10": "money",
                "noun_11": "us",
                "noun_12": "Onlyfans pages",
                "adjective_3": "unacceptable",
                "noun_13": "mine",
                "noun_14": "yours",
                "noun_15": "Saturday",
                "adverb_1": "unbelievably",
                "noun_16": "comments",
                "noun_17": "thumbs down",
                "verb_2": "fallen",
                "adjective_4": "boring",
                "noun_18": "DM's",
                "verb_3": "text",
                "noun_19": "cellular",
                "noun_20": "bestie",
                "noun_21": "whatever",
                "noun_22": "money",
                "noun_23": "coverage",
                "noun_24": "lip gloss",
                "adjective_5": "Downtown",
                "noun_25": "dude",
                "proper_noun_4": "scrubs",
                "noun_26": "digits",
                "noun_27": "a bank account",
                "noun_28": "symbol",
                "verb_4": "desired",
                "noun_29": "bachelor",
                "noun_30": "stoppage",
                "noun_31": "booty calls"
            }

            input_values = {}

            # Paragraph 1 - at the start
            st.markdown("While the history of <span style='color:red;'>NOUN 1</span> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <span style='color:red;'>NOUN 2</span>, the themes of our <span style='color:red;'>NOUN 3</span> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <span style='color:red;'>NOUN 4</span>. Perhaps the predominant theme throughout is the competition for and allocation of <span style='color:red;'>PLURAL NOUN 1</span> within <span style='color:red;'>PLURAL NOUN 2</span> across the globe.", unsafe_allow_html=True)

            # Input fields 0-5 (Noun 1 through Plural Noun 2)
            cols = st.columns(3)
            for i in range(6):
                label, key = input_fields_all[i]
                with cols[(i - 0) % 3]:
                    input_values[key] = st.text_input(label, key=key, value=default_madlib_values.get(key, ''))

            # Paragraph 2 - after Plural Noun 2
            st.markdown("From Mesopotamia to ancient Mexico and Rome to ancient <span style='color:red;'>PROPER NOUN 2</span>, we find <span style='color:red;'>PLURAL NOUN 3</span> that create a <span style='color:red;'>ADJECTIVE 1</span><span style='color:black;'> | </span><span style='color:red;'>NOUN 5</span> that assigns greater value to their own <span style='color:red;'>NOUN 6</span>, and greater resources to themselves and their <span style='color:red;'>PLURAL NOUN 4</span>. This comes, of course, at the expense of the <span style='color:red;'>PLURAL NOUN 5</span>, the <span style='color:red;'>NOUN 7</span> who have toiled in the service of others of <span style='color:red;'>ADJECTIVE 2</span> standing. From prehistory through the modern era, <span style='color:red;'>NOUN 8</span> has existed in various forms and under various names. This includes the <span style='color:red;'>NOUN 9</span> of medieval <span style='color:red;'>PROPER NOUN 3</span> to the chattel <span style='color:red;'>NOUN 8</span> of the early United States, and it persists to this day as wage <span style='color:red;'>NOUN 10</span> where huge swaths of <span style='color:red;'>NOUN 11</span> are unable to reap the full benefit of their own <span style='color:red;'>NOUN 12</span>.", unsafe_allow_html=True)

            # Input fields 6-21 (Proper Noun 2 through Noun 12, 'verb_1' is skipped, so 15 fields)
            cols = st.columns(3)
            for i in range(6, 21):
                label, key = input_fields_all[i]
                with cols[(i - 6) % 3]:
                    input_values[key] = st.text_input(label, key=key, value=default_madlib_values.get(key, ''))

            # Paragraph 3 - after Noun 12
            st.markdown("While this <span style='color:red;'>ADJECTIVE 3</span> stratification of <span style='color:red;'>NOUN 13</span> and <span style='color:red;'>NOUN 14</span> has persisted across <span style='color:red;'>NOUN 15</span> and, <span style='color:red;'>ADVERB 1</span>, across the globe, it is not naturally self sustaining. Indeed, <span style='color:red;'>NOUN 16</span> have risen and <span style='color:red;'>NOUN 17</span> have <span style='color:red;'>VERB 1</span> as <span style='color:red;'>ADJECTIVE 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 18</span> have reached across the globe seeking to <span style='color:red;'>VERB 2</span> the <span style='color:red;'>NOUN 19</span> of the <span style='color:red;'>NOUN 20</span> and <span style='color:red;'>NOUN 21</span>. At the local level, <span style='color:red;'>NOUN 22</span> has always been necessary to maintain <span style='color:red;'>NOUN 23</span> of <span style='color:red;'>NOUN 24</span>, from the <span style='color:red;'>NOUN 25</span> patrols of <span style='color:red;'>ADJECTIVE 5</span> America to the targeting of <span style='color:red;'>NOUN 26</span> by <span style='color:red;'>PROPER NOUN 4</span> today. Even on the individual level, <span style='color:red;'>NOUN 27</span> has been a <span style='color:red;'>NOUN 28</span> of the <b>{answers['verb_4']}</b> <b>{answers['noun_29']}</b> to compel the <b>{answers['noun_30']}</b> of the <b>{answers['noun_31']}</b>.</div>", unsafe_allow_html=True)
