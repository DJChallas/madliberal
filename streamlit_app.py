import numpy as np # Ensure numpy is imported
import statsmodels.api as sm # Ensure statsmodels is imported
import plotly.express as px # Ensure plotly.express is imported

if 'df' in locals() and not df.empty: # Ensure df exists from previous step
    df['value'] = df['value'].astype(str).str.replace(r'\s+\(\d+\)', '', regex=True)
    df['value'] = pd.to_numeric(df['value'], errors='coerce') / 100
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
        # Civilian Labor Force Level Series
        'LNS11000004': 'Labor Force - White Men',
        'LNS11000005': 'Labor Force - White Women',
        'LNS11032183': 'Labor Force - Asian',
        'LNS11000001': 'Labor Force - Men',
        'LNS11000002': 'Labor Force - Women',
        'LNS11000003': 'Labor Force - White',
        'LNS11000006': 'Labor Force - Black or African American',
        'LNS11000009': 'Labor Force - Hispanic or Latino'
    }
    series_name_mapping = sn_map

    latest_full_year = df['year'].astype(int).max()
    if latest_full_year == datetime.now().year:
        latest_full_year -= 1

    df_seasonal = df_filtered[df_filtered['year'].astype(int) == latest_full_year].copy()
    df_seasonal['series_name'] = df_seasonal['series_id'].map(series_name_mapping)

    avg_unemployment_latest_year = df_seasonal.groupby('series_id')['value'].mean().reset_index()
    avg_unemployment_latest_year['series_name'] = avg_unemployment_latest_year['series_id'].map(series_name_mapping)

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
        'Labor Force - White'
    ]
    avg_unemployment_latest_year['series_name'] = pd.Categorical(
        avg_unemployment_latest_year['series_name'],
        categories=desired_order,
        ordered=True
    )
    avg_unemployment_latest_year = avg_unemployment_latest_year.sort_values('series_name')

    print("Filtered data (df_filtered) head:")
    display(df_filtered.head())
    print("Seasonal data (df_seasonal) head for latest full year:")
    display(df_seasonal.head())
    print("Average rates for latest full year:")
    display(avg_unemployment_latest_year)

    # OLS Regression Analysis
    regression_results_summary = {}
    ols_year_coefs = {}
    ols_rsquared_values = {}
    epsilon = 1e-6

    # Use all series_ids now present in the sn_map for regression
    for series_id in sn_map.keys():
        df_series = df_filtered[df_filtered['series_id'] == series_id].copy()
        df_series['year_numeric'] = df_series['year'].astype(int)
        # For Unemployment, values are proportions (0-1). For Labor Force, values are in thousands.
        # Only apply clipping for Unemployment values if they are proportions.
        if 'Unemployment' in sn_map[series_id]:
            df_series['value_adjusted'] = df_series['value'].clip(lower=epsilon, upper=1 - epsilon)
        else:
            # For Labor Force, values are already in thousands, no need to adjust or clip like proportions.
            df_series['value_adjusted'] = df_series['value']

        if not df_series.empty and len(df_series['year_numeric'].unique()) > 1:
            X = sm.add_constant(df_series['year_numeric'])
            y = df_series['value_adjusted']

            ols_model = sm.OLS(y, X)
            ols_results = ols_model.fit()

            regression_results_summary[series_id] = ols_results.summary()
            ols_year_coefs[series_id] = ols_results.params['year_numeric']
            ols_rsquared_values[series_id] = ols_results.rsquared
        else:
            regression_results_summary[series_id] = f"Not enough data to run OLS regression for {sn_map.get(series_id, series_id)}."
            ols_year_coefs[series_id] = np.nan
            ols_rsquared_values[series_id] = np.nan

    print("OLS Year Coefficients:")
    display(pd.Series(ols_year_coefs).rename('year_coefficient'))
    print("OLS R-squared Values:")
    display(pd.Series(ols_rsquared_values).rename('R-squared'))

    # --- Visualization Functions (now embedded for consolidation) ---
    def plot_rates_by_sex(avg_df, year, chart_type_prefix):
        sex_groups = [f'{chart_type_prefix} - Men', f'{chart_type_prefix} - Women', f'{chart_type_prefix} - White Men', f'{chart_type_prefix} - White Women']
        df_sex = avg_df[avg_df['series_name'].isin(sex_groups)].copy()
        df_sex = df_sex.sort_values(by='value', ascending=False)

        y_column = 'value'
        y_axis_label = ''
        tick_format = None

        if chart_type_prefix == 'Unemployment':
            y_axis_label = 'Average Unemployment Rate (Proportion)'
            tick_format = '.1%'
        elif chart_type_prefix == 'Labor Force':
            y_column = 'proportion'
            y_axis_label = 'Proportion of Total Labor Force'
            tick_format = '.1%'

        fig_sex = px.bar(
            df_sex,
            x='series_name',
            y=y_column,
            title=f'Average {chart_type_prefix} by Sex in {year}',
            labels={'series_name': 'Demographic Group', y_column: y_axis_label},
            color='series_name'
        )
        fig_sex.update_layout(
            xaxis_title='Demographic Group',
            yaxis_title=y_axis_label,
            showlegend=False
        )
        if tick_format:
            fig_sex.update_yaxes(tickformat=tick_format)
        return fig_sex

    def plot_rates_by_race(avg_df, year, chart_type_prefix):
        race_groups = [f'{chart_type_prefix} - Black or African American', f'{chart_type_prefix} - Hispanic or Latino', f'{chart_type_prefix} - Asian', f'{chart_type_prefix} - White']
        df_race = avg_df[avg_df['series_name'].isin(race_groups)].copy()
        df_race = df_race.sort_values(by='value', ascending=False)

        y_column = 'value'
        y_axis_label = ''
        tick_format = None

        if chart_type_prefix == 'Unemployment':
            y_axis_label = 'Average Unemployment Rate (Proportion)'
            tick_format = '.1%'
        elif chart_type_prefix == 'Labor Force':
            y_column = 'proportion'
            y_axis_label = 'Proportion of Total Labor Force'
            tick_format = '.1%'

        fig_race = px.bar(
            df_race,
            x='series_name',
            y=y_column,
            title=f'Average {chart_type_prefix} by Race in {year}',
            labels={'series_name': 'Demographic Group', y_column: y_axis_label},
            color='series_name'
        )
        fig_race.update_layout(
            xaxis_title='Demographic Group',
            yaxis_title=y_axis_label,
            showlegend=False
        )
        if tick_format:
            fig_race.update_yaxes(tickformat=tick_format)
        return fig_race

    def plot_white_women_comparisons(avg_df, year, chart_type_prefix):
        white_women_avg_series_name = f'{chart_type_prefix} - White Women'
        if white_women_avg_series_name not in avg_df['series_name'].values:
            print(f"'{white_women_avg_series_name}' not found in data for comparisons.")
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

            if chart_type_prefix == 'Unemployment':
                y_axis_label = 'Average Unemployment Rate (Proportion)'
                tick_format = '.1%'
            elif chart_type_prefix == 'Labor Force':
                y_column = 'proportion'
                y_axis_label = 'Proportion of Total Labor Force'
                tick_format = '.1%'

            comparison_df = pd.DataFrame({
                'series_name': [white_women_avg_series_name, display_comparison_group_name],
                'value': [white_women_avg[y_column], row[y_column]]
            })

            fig = px.bar(
                comparison_df,
                x='series_name',
                y='value',
                title=f"Average {chart_type_prefix}: White Women vs. {display_comparison_group_name} in {year}",
                labels={'series_name': 'Demographic Group', 'value': y_axis_label},
                color='series_name'
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

    # --- Display Visualizations for Unemployment ---
    unemployment_avg_df = avg_unemployment_latest_year[avg_unemployment_latest_year['series_name'].str.contains('Unemployment')].copy()
    if not unemployment_avg_df.empty:
        print("\n--- Unemployment Visualizations ---")
        print("Average Unemployment Rates")
        print("The current calculations for unemployment are generated by averaging the seasonal unemployment percentages for all of the listed categories for a period of one year starting from the most recent release by the US Bureau of Labor Statistics: Men, Women, White Men, White Women, Black or African American, Hispanic or Latino and Asian. The data used for Hispanic or Latino is from a subcategory for unemployment statistics independent of the White, Black and Asian datasets.")

        fig_sex_unemployment = plot_rates_by_sex(unemployment_avg_df, latest_full_year, 'Unemployment')
        fig_sex_unemployment.show()

        fig_race_unemployment = plot_rates_by_race(unemployment_avg_df, latest_full_year, 'Unemployment')
        fig_race_unemployment.show()

        print("Mad Liberal Comparisons (Unemployment):")
        unemployment_comparison_charts = plot_white_women_comparisons(unemployment_avg_df, latest_full_year, 'Unemployment')
        for chart in unemployment_comparison_charts:
            chart.show()
    else:
        print("No unemployment data available for visualization.")

    # --- Display Visualizations for Civilian Labor Force Level ---
    labor_force_avg_df = avg_unemployment_latest_year[avg_unemployment_latest_year['series_name'].str.contains('Labor Force')].copy()

    # Calculate total labor force and proportions before plotting
    if not labor_force_avg_df.empty:
        total_labor_force_overall = labor_force_avg_df['value'].sum()
        if total_labor_force_overall > 0:
            labor_force_avg_df['proportion'] = labor_force_avg_df['value'] / total_labor_force_overall
        else:
            labor_force_avg_df['proportion'] = 0 # Avoid division by zero

    if not labor_force_avg_df.empty:
        print("\n--- Civilian Labor Force Level Visualizations ---")
        print("Average Civilian Labor Force Levels (Displayed as Proportions)") # Updated description
        print("These visualizations show the proportion of each demographic group within the total civilian labor force.")

        fig_sex_labor_force = plot_rates_by_sex(labor_force_avg_df, latest_full_year, 'Labor Force')
        fig_sex_labor_force.show()

        fig_race_labor_force = plot_rates_by_race(labor_force_avg_df, latest_full_year, 'Labor Force')
        fig_race_labor_force.show()

        print("Comparisons (Labor Force):")
        labor_force_comparison_charts = plot_white_women_comparisons(labor_force_avg_df, latest_full_year, 'Labor Force')
        for chart in labor_force_comparison_charts:
            chart.show()
    else:
        print("No civilian labor force level data available for visualization.")

else:
    print("DataFrame 'df' not available for cleaning/regression/plotting. Please ensure the data import cell ran successfully.")
