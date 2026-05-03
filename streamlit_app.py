# Streamlit app code (continuation of 8b3b3c5d)
# ... (previous Streamlit app code)

# --- Streamlit App (main_content for industry_visualizations stage) ---
# The existing Streamlit app code from 8b3b3c5d will be wrapped and modified here.
# This modification is for clarity and to simulate changes within the existing cell.

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


if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 'industry_visualizations'

left_sidebar, main_content, right_sidebar = st.columns([0.2, 0.6, 0.2])

with left_sidebar:
    st.subheader("The Real Story:")
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From <b>{real_proper_noun_1}</b> to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

    st.markdown("-" * 3)

with main_content:
    st.components.v1.html("<script>window.top.scroll(0, 0);</script>", height=0, width=0)

    viz_col = st.columns([1])

    with viz_col[0]:
        st.subheader("Industry Visualizations about Sex and Race")
        st.markdown("The US Census Bureau website provides statistics for race in the United States at the current levels: White Alone 74.8&, Black Alone 13.7%, Asian Alone 6.7%, Hispanic or Latino Alone 20%. To calculate our totals we applied data based on seasonal employment rates averaged and totaled - White, Asian, Black or African American and Hispanic or Latino based on the Civilian Labor Force Level. That is to create an active comparison to employment levels by industry against a measurable estimate provided by the BLS.")
        st.markdown("The Department of Labor presents a measure of data called Employed people by detailed occupation, sex, race, and Hispanic or Latino ethnicity (https://www.bls.gov/cps/cpsaat11.htm) that presents percentages of demographics employed in each of those occupations, grouped by industry. I’ve collected data for the primary Industries for gender and race to compare distribution of demographics across the US job market for the 5 main industry divisions.")

        df_filtered, latest_full_year, unemployment_avg_df, labor_force_avg_df, \
        industry_management_avg_df, industry_service_avg_df, industry_sales_office_avg_df, \
        industry_natural_resources_avg_df, industry_transportation_avg_df = load_and_process_bls_data()

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
            st.plotly_chart(plot_rates_by_race(industry_management_avg_df, latest_full_year, 'Employment Level - Management, Professional'), use_container_width=True)

            st.markdown("--- ")

            # --- Service Occupations ---
            industry_title_service = 'Service Occupations'
            st.subheader(industry_title_service)
            st.plotly_chart(plot_rates_by_sex(industry_service_avg_df, latest_full_year, 'Employment Level - Service Occupations'), use_container_width=True)
            st.plotly_chart(plot_rates_by_race(industry_service_avg_df, latest_full_year, 'Employment Level - Service Occupations'), use_container_width=True)

            st.markdown("--- ")

            # --- Sales and Office Occupations ---
            industry_title_sales_office = 'Sales and Office Occupations'
            st.subheader(industry_title_sales_office)
            st.plotly_chart(plot_rates_by_sex(industry_sales_office_avg_df, latest_full_year, 'Employment Level - Sales and Office Occupations'), use_container_width=True)
            st.plotly_chart(plot_rates_by_race(industry_sales_office_avg_df, latest_full_year, 'Employment Level - Sales and Office Occupations'), use_container_width=True)

            st.markdown("--- ")

            # --- Natural resources, construction, and maintenance occupations ---
            industry_title_natural_resources = 'Natural resources, construction, and maintenance occupations'
            st.subheader(industry_title_natural_resources)
            st.plotly_chart(plot_rates_by_sex(industry_natural_resources_avg_df, latest_full_year, 'Employment Level - Natural Resources, Construction, and Maintenance'), use_container_width=True)
            st.plotly_chart(plot_rates_by_race(industry_natural_resources_avg_df, latest_full_year, 'Employment Level - Natural Resources, Construction, and Maintenance'), use_container_width=True)

            st.markdown("--- ")

            # --- Production, transportation, and material moving occupations ---
            industry_title_transportation = 'Production, transportation, and material moving occupations'
            st.subheader(industry_title_transportation)
            st.plotly_chart(plot_rates_by_sex(industry_transportation_avg_df, latest_full_year, 'Employment Level - Transportation and Material Moving'), use_container_width=True)
            st.plotly_chart(plot_rates_by_race(industry_transportation_avg_df, latest_full_year, 'Employment Level - Transportation and Material Moving'), use_container_width=True)

            st.markdown("--- ")

            # --- NEW: Logit Regression Analysis for Sex by Industry ---
            st.subheader("Logit Regression Analysis for Sex by Industry")
            st.markdown("This section presents the results of binary logit regression models predicting the probability of employment in each industry based on an individual's sex (Female vs. Male).")

            industry_dfs = {
                'Management, Professional, and Related Occupations': {
                    'df': industry_management_avg_df,
                    'prefix': 'Employment Level - Management, Professional'
                },
                'Service Occupations': {
                    'df': industry_service_avg_df,
                    'prefix': 'Employment Level - Service Occupations'
                },
                'Sales and Office Occupations': {
                    'df': industry_sales_office_avg_df,
                    'prefix': 'Employment Level - Sales and Office Occupations'
                },
                'Natural Resources, Construction, and Maintenance Occupations': {
                    'df': industry_natural_resources_avg_df,
                    'prefix': 'Employment Level - Natural Resources, Construction, and Maintenance'
                },
                'Production, Transportation, and Material Moving Occupations': {
                    'df': industry_transportation_avg_df,
                    'prefix': 'Employment Level - Transportation and Material Moving'
                }
            }

            all_sex_regression_results = []

            for industry_title, data in industry_dfs.items():
                results = perform_logit_regression_for_sex(data['df'], data['prefix'], labor_force_avg_df)
                if results:
                    all_sex_regression_results.append(results)

            if all_sex_regression_results:
                sex_results_df = pd.DataFrame(all_sex_regression_results)
                st.dataframe(sex_results_df.set_index('Industry'))

                st.markdown("**Interpretation Notes:**")
                st.markdown("- **Odds Ratio (Female vs. Male):** An odds ratio greater than 1 indicates that female individuals have higher odds of employment in that industry compared to male individuals, all else being equal. An odds ratio less than 1 indicates lower odds.")
                st.markdown("- **P-value (is_female):** A p-value less than a chosen significance level (e.g., 0.05) suggests a statistically significant difference in employment probability between female and male individuals.")
                st.markdown("- **Predicted Probability:** The estimated probability of employment for male and female individuals in that industry, based on the model.")
                st.markdown("**Disclaimer:** This analysis uses a simulated dataset derived from aggregated BLS employment levels. For a precise and robust analysis, individual-level survey data would be required.")
            else:
                st.warning("No logit regression results could be generated for the industries based on sex data.")

        else:
            st.warning("Cannot generate labor force visualizations, data not available.")


st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
