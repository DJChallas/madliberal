import streamlit as st
import pandas as pd
import numpy as np
# import subprocess # Removed as per previous instruction
# import sys # Removed as per previous instruction
import plotly.express as px # Added for regression visualization
import statsmodels.api as sm # Changed to statsmodels for regression

# --- Global Streamlit Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Streamlit App ---
# New global header (left-aligned) as requested
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
    # Add alternating red and white stripes like the US flag (78 stripes)
    for i in range(50):
        color = "red" if i % 2 == 0 else "#FFFFFF"
        st.markdown(f'<div style="height: 20px; background-color: {color}; width: 100%; margin: 0; padding: 0;"></div>', unsafe_allow_html=True)


with main_content:
    # --- Mad Lib Input Stage ---
    if st.session_state.game_stage == 'madlib_input':
        with st.form("madlib_form"):
            input_fields_all = [
                ("Noun 1", "noun_1"),
                ("Noun 2", "noun_2"),
                ("Noun 3", "noun_3"),
                ("Noun 4", "noun_4"), # Was Noun 1X
                ("Plural Noun 1", "noun_resource"),
                ("Plural Noun 2", "noun_society_plural"),

                ("Proper Noun 2", "proper_noun_2"),
                ("Plural Noun 3", "plural_noun_3"),
                ("Adjective 1", "adjective_1"),
                ("Noun 5", "noun_5"), # Was Noun 4
                ("Noun 6", "noun_6"), # Was Noun 5
                ("Plural Noun 4", "plural_noun_4"),
                ("Plural Noun 5", "plural_noun_5"),
                ("Noun 7", "noun_7"), # Was Noun 6
                ("Verb 1", "verb_1"),
                ("Adjective 2", "adjective_2"),
                ("Noun 8", "noun_8"), # Was Noun 7
                ("Noun 9", "noun_9"), # Was Noun 8
                ("Proper Noun 3", "proper_noun_3"),
                ("Noun 10", "noun_10"), # Was Noun 9
                ("Noun 11", "noun_11"), # Was Noun 10

                ("Adjective 3", "adjective_3"),
                ("Noun 12", "noun_12"), # Was Noun 11
                ("Noun 13", "noun_13"), # Was Noun 12
                ("Noun 14", "noun_14"), # Was Noun 13
                ("Adverb 1", "adverb_1"),
                ("Noun 15", "noun_15"), # Was Noun 14
                ("Noun 16", "noun_16"), # Was Noun 15
                ("Verb 2", "verb_2"),
                ("Adjective 4", "adjective_4"),
                ("Noun 17", "noun_17"), # Was Noun 16
                ("Verb 3", "verb_3"),
                ("Noun 18", "noun_18"), # Was Noun 17
                ("Noun 19", "noun_19"), # Was Noun 18
                ("Noun 20", "noun_20"), # Was Noun 19
                ("Noun 21", "noun_21"), # Was Noun 20
                ("Noun 22", "noun_22"), # Was Noun 21
                ("Noun 23", "noun_23"), # Was Noun 22
                ("Adjective 5", "adjective_5"),
                ("Noun 24", "noun_24"), # Was Noun 23
                ("Proper Noun 4", "proper_noun_4"),
                ("Noun 25", "noun_25"), # Was Noun 24
                ("Noun 26", "noun_26"), # Was Noun 25
                ("Noun 27", "noun_27"), # Was Noun 26
                ("Verb 4", "verb_4"),
                ("Noun 28", "noun_28"), # Was Noun 27
                ("Noun 29", "noun_29"), # Was Noun 28
                ("Noun 30", "noun_30"), # Was Noun 29
            ]

            input_values = {}

            # Paragraph 1 - at the start
            st.markdown("While the history of <span style='color:red;'>NOUN 1</span> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <span style='color:red;'>NOUN 2</span>, the themes of our <span style='color:red;'>NOUN 3</span> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <span style='color:red;'>NOUN 4</span>. Perhaps the predominant theme throughout is the competition for and allocation of <span style='color:red;'>PLURAL NOUN 1</span> within <span style='color:red;'>PLURAL NOUN 2</span> across the globe.", unsafe_allow_html=True)

            # Input fields 0-5 (Noun 1 through Plural Noun 2)
            cols = st.columns(3)
            for i in range(6):
                label, key = input_fields_all[i]
                with cols[i % 3]:
                    input_values[key] = st.text_input(label, key=key)

            # Paragraph 2 - after Plural Noun 2
            st.markdown("From Mesopotamia to ancient Mexico and Rome to ancient <span style='color:red;'>PROPER NOUN 2</span>, we find <span style='color:red;'>PLURAL NOUN 3</span> that create a <span style='color:red;'>ADJECTIVE 1</span><span style='color:black;'> | </span><span style='color:red;'>NOUN 5</span> that assigns greater value to their own <span style='color:red;'>NOUN 6</span>, and greater resources to themselves and their <span style='color:red;'>PLURAL NOUN 4</span>. This comes, of course, at the expense of the <span style='color:red;'>PLURAL NOUN 5</span>, the <span style='color:red;'>NOUN 7</span> who have <span style='color:red;'>VERB 1</span> in the service of others of <span style='color:red;'>ADJECTIVE 2</span> standing. From prehistory through the modern era, <span style='color:red;'>NOUN 8</span> has existed in various forms and under various names. This includes the <span style='color:red;'>NOUN 9</span> of medieval <span style='color:red;'>PROPER NOUN 3</span> to the chattel <span style='color:red;'>NOUN 8</span> of the early United States, and it persists to this day as wage <span style='color:red;'>NOUN 9</span> where huge swaths of <span style='color:red;'>NOUN 10</span> are unable to reap the full benefit of their own <span style='color:red;'>NOUN 11</span>.", unsafe_allow_html=True)

            # Input fields 6-20 (Proper Noun 2 through Noun 11)
            cols = st.columns(3)
            for i in range(6, 21):
                label, key = input_fields_all[i]
                with cols[(i - 6) % 3]:
                    input_values[key] = st.text_input(label, key=key)

            # Paragraph 3 - after Noun 11
            st.markdown("While this <span style='color:red;'>ADJECTIVE 3</span> stratification of <span style='color:red;'>NOUN 12</span> and <span style='color:red;'>NOUN 13</span> has persisted across <span style='color:red;'>NOUN 14</span> and, <span style='color:red;'>ADVERB 1</span>, across the globe, it is not naturally self sustaining. Indeed, <span style='color:red;'>NOUN 15</span> have risen and <span style='color:red;'>NOUN 16</span> have <span style='color:red;'>VERB 2</span> as <span style='color:red;'>ADJECTIVE 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 17</span> have reached across the globe seeking to <span style='color:red;'>VERB 3</span> the <span style='color:red;'>NOUN 18</span> of the <span style='color:red;'>NOUN 19</span> and <span style='color:red;'>NOUN 20</span>. At the local level, <span style='color:red;'>NOUN 21</span> has always been necessary to maintain <span style='color:red;'>NOUN 22</span> of <span style='color:red;'>NOUN 23</span>, from the <span style='color:red;'>NOUN 24</span> patrols of <span style='color:red;'>ADJECTIVE 5</span> America to the targeting of <span style='color:red;'>NOUN 25</span> by <span style='color:red;'>PROPER NOUN 4</span> today. Even on the individual level, <span style='color:red;'>NOUN 26</span> has been a <span style='color:red;'>NOUN 27</span> of the <span style='color:red;'>VERB 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 28</span> to compel the <span style='color:red;'>NOUN 29</span> of the <span style='color:red;'>NOUN 30</span>.", unsafe_allow_html=True)

            # Input fields 21+ (Adjective 3 through Noun 30)
            cols = st.columns(3)
            for i in range(21, len(input_fields_all)):
                label, key = input_fields_all[i]
                with cols[(i - 21) % 3]:
                    input_values[key] = st.text_input(label, key=key)

            # Add some spacing after the input fields
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            # Center the button
            _, center_col, _ = st.columns(3)
            with center_col:
                submitted = st.form_submit_button("Submit Your Mad Lib!", use_container_width=True)

        if submitted:
            if all(input_values.values()):
                st.session_state.madlib_answers = input_values
                st.session_state.game_stage = 'madlib_reveal'
                st.rerun() # Rerun to switch stage
            else:
                st.warning("Please fill in all the blanks!")

    # --- Mad Lib Reveal Stage ---
    elif st.session_state.game_stage == 'madlib_reveal':
        st.markdown("<div style='border: 2px solid #f0f2f6; border-radius: 5px; padding: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True) # Custom frame
        st.subheader("Your Story:")
        answers = st.session_state.madlib_answers
        st.write(f"While the history of **{answers['noun_1']}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{answers['noun_2']}**, the themes of our **{answers['noun_3']}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{answers['noun_4']}**. Perhaps the predominant theme throughout is the competition for and allocation of **{answers['noun_resource']}** within **{answers['noun_society_plural']}** across the globe.")
        st.write(f"From Mesopotamia to ancient Mexico and Rome to ancient **{answers['proper_noun_2']}**, we find **{answers['plural_noun_3']}** that create a **{answers['adjective_1']}** **{answers['noun_5']}** that assigns greater value to their own **{answers['noun_6']}**, and greater resources to themselves and their **{answers['plural_noun_4']}**. This comes, of course, at the expense of the **{answers['plural_noun_5']}**, the **{answers['noun_7']}** who have **{answers['verb_1']}** in the service of others of **{answers['adjective_2']}** standing. From prehistory through the modern era, **{answers['noun_8']}** has existed in various forms and under various names. This includes the **{answers['noun_9']}** of medieval **{answers['proper_noun_3']}** to the chattel **{answers['noun_8']}** of the early United States, and it persists to this day as wage **{answers['noun_9']}** where huge swaths of **{answers['noun_10']}** are unable to reap the full benefit of their own **{answers['noun_11']}**.")
        st.write(f"While this **{answers['adjective_3']}** stratification of **{answers['noun_12']}** and **{answers['noun_13']}** has persisted across **{answers['noun_14']}** and, **{answers['adverb_1']}**, across the globe, it is not naturally self sustaining. Indeed, **{answers['noun_15']}** have risen and **{answers['noun_16']}** have **{answers['verb_2']}** as **{answers['adjective_4']}** **{answers['noun_17']}** have reached across the globe seeking to **{answers['verb_3']}** the **{answers['noun_18']}** of the **{answers['noun_19']}** and **{answers['noun_20']}**. At the local level, **{answers['noun_21']}** has always been necessary to maintain **{answers['noun_22']}** of **{answers['noun_23']}**, from the **{answers['noun_24']}** patrols of **{answers['adjective_5']}** America to the targeting of **{answers['noun_25']}** by **{answers['proper_noun_4']}** today. Even on the individual level, **{answers['noun_26']}** has been a **{answers['noun_27']}** of the **{answers['verb_4']}** **{answers['noun_28']}** to compel the **{answers['noun_29']}** of the **{answers['noun_30']}**.")

        st.subheader("The Real Story:")
        real_noun_1 = "humanity"
        real_noun_2 = "present"
        real_noun_3 = "past"
        real_noun_4 = "evidence" # New real noun value
        real_noun_resource = "resources"
        real_noun_society_plural = "societies"
        real_proper_noun_1 = "Mesopotamia"
        real_proper_noun_2 = "Japan"
        real_plural_noun_3 = "hierarchies"
        real_adjective_1 = "dominant"
        real_noun_5 = "class" # Was Noun 4
        real_noun_6 = "existence" # Was Noun 5
        real_plural_noun_4 = "cohorts"
        real_plural_noun_5 = "underclasses"
        real_noun_7 = "poor" # Was Noun 6
        real_verb_1 = "toiled"
        real_adjective_2 = "higher"
        real_noun_8 = "slavery" # Was Noun 7
        real_noun_9 = "serfdom" # Was Noun 8
        real_proper_noun_3 = "Europe"
        real_noun_10 = "humanity" # Was Noun 9
        real_noun_11 = "labor" # Was Noun 10

        real_adjective_3 = "extreme"
        real_noun_12 = "wealth" # Was Noun 11
        real_noun_13 = "status" # Was Noun 12
        real_noun_14 = "millennia" # Was Noun 13
        real_adverb_1 = "indeed" # New real adverb value
        real_noun_15 = "empires" # Was Noun 14
        real_noun_16 = "empires" # Was Noun 15
        real_verb_2 = "fallen"
        real_adjective_4 = "invading"
        real_noun_17 = "forces" # Was Noun 16
        real_verb_3 = "hoard"
        real_noun_18 = "wealth" # Was Noun 17
        real_noun_19 = "land" # Was Noun 18
        real_noun_20 = "labor" # Was Noun 19
        real_noun_21 = "violence" # Was Noun 20
        real_noun_22 = "systems" # Was Noun 21
        real_noun_23 = "inequality" # Was Noun 22
        real_noun_24 = "slave" # Was Noun 23
        real_adjective_5 = "antebellum"
        real_noun_25 = "immigrants" # Was Noun 24
        real_proper_noun_4 = "ICE"
        real_noun_26 = "violence" # Was Noun 25
        real_noun_27 = "tool" # Was Noun 26
        real_verb_4 = "favored"
        real_noun_28 = "elites" # Was Noun 27
        real_noun_29 = "compliance" # Was Noun 28
        real_noun_30 = "poor" # Was Noun 29

        st.write(f"While the history of **{real_noun_1}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{real_noun_2}**, the themes of our **{real_noun_3}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{real_noun_4}**. Perhaps the predominant theme throughout is the competition for and allocation of **{real_noun_resource}** within **{real_noun_society_plural}** across the globe.")
        st.write(f"From **{real_proper_noun_1}** to ancient Mexico and Rome to ancient **{real_proper_noun_2}**, we find **{real_plural_noun_3}** that create a **{real_adjective_1}** **{real_noun_5}** that assigns greater value to their own **{real_noun_6}**, and greater resources to themselves and their **{real_plural_noun_4}**. This comes, of course, at the expense of the **{real_plural_noun_5}**, the **{real_noun_7}** who have **{real_verb_1}** in the service of others of **{real_adjective_2}** standing. From prehistory through the modern era, **{real_noun_8}** has existed in various forms and under various names. This includes the **{real_noun_9}** of medieval **{real_proper_noun_3}** to the chattel **{real_noun_8}** of the early United States, and it persists to this day as wage **{real_noun_9}** where huge swaths of **{real_noun_10}** are unable to reap the full benefit of their own **{real_noun_11}**.")
        st.write(f"While this **{real_adjective_3}** stratification of **{real_noun_12}** and **{real_noun_13}** has persisted across **{real_noun_14}** and, **{real_adverb_1}**, across the globe, it is not naturally self sustaining. Indeed, **{real_noun_15}** have risen and **{real_noun_16}** have **{real_verb_2}** as **{real_adjective_4}** **{real_noun_17}** have reached across the globe seeking to **{real_verb_3}** the **{real_noun_18}** of the **{real_noun_19}** and **{real_noun_20}**. At the local level, **{real_noun_21}** has always been necessary to maintain **{real_noun_22}** of **{real_noun_23}**, from the **{real_noun_24}** patrols of **{real_adjective_5}** America to the targeting of **{real_noun_25}** by **{real_proper_noun_4}** today. Even on the individual level, **{real_noun_26}** has been a **{real_noun_27}** of the **{real_verb_4}** **{real_noun_28}** to compel the **{real_noun_29}** of the **{real_noun_30}**.")


        col1_viz, col2_viz, col3_viz = st.columns([1,1,1])
        with col2_viz:
            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
            if st.button("Proceed to Visualizations"):
                st.session_state.game_stage = 'visualizations'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True) # Close custom frame

# --- Visualizations Stage ---
    elif st.session_state.game_stage == 'visualizations':
        st.markdown("<div style='border: 2px solid #f0f2f6; border-radius: 5px; padding: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True) # Custom frame
        # The global header now handles the title/subtitle, so no need for these here.
        col_left_viz, col_right_viz = st.columns([0.2, 0.8]) # Narrow left, wider right

        with col_left_viz:
            # Define real story variables for this stage
            real_noun_1 = "humanity"
            real_noun_2 = "present"
            real_noun_3 = "past"
            real_noun_4 = "evidence" # New real noun value
            real_noun_resource = "resources"
            real_noun_society_plural = "societies"
            real_proper_noun_1 = "Mesopotamia"
            real_proper_noun_2 = "Japan"
            real_plural_noun_3 = "hierarchies"
            real_adjective_1 = "dominant"
            real_noun_5 = "class" # Was Noun 4
            real_noun_6 = "existence" # Was Noun 5
            real_plural_noun_4 = "cohorts"
            real_plural_noun_5 = "underclasses"
            real_noun_7 = "poor" # Was Noun 6
            real_verb_1 = "toiled"
            real_adjective_2 = "higher"
            real_noun_8 = "slavery" # Was Noun 7
            real_noun_9 = "serfdom" # Was Noun 8
            real_proper_noun_3 = "Europe"
            real_noun_10 = "humanity" # Was Noun 9
            real_noun_11 = "labor" # Was Noun 10

            real_adjective_3 = "extreme"
            real_noun_12 = "wealth" # Was Noun 11
            real_noun_13 = "status" # Was Noun 12
            real_noun_14 = "millennia" # Was Noun 13
            real_adverb_1 = "indeed"
            real_noun_15 = "empires" # Was Noun 14
            real_noun_16 = "empires" # Was Noun 15
            real_verb_2 = "fallen"
            real_adjective_4 = "invading"
            real_noun_17 = "forces" # Was Noun 16
            real_verb_3 = "hoard"
            real_noun_18 = "wealth" # Was Noun 17
            real_noun_19 = "land" # Was Noun 18
            real_noun_20 = "labor" # Was Noun 19
            real_noun_21 = "violence" # Was Noun 20
            real_noun_22 = "systems" # Was Noun 21
            real_noun_23 = "inequality" # Was Noun 22
            real_noun_24 = "slave" # Was Noun 23
            real_adjective_5 = "antebellum"
            real_noun_25 = "immigrants" # Was Noun 24
            real_proper_noun_4 = "ICE"
            real_noun_26 = "violence" # Was Noun 25
            real_noun_27 = "tool" # Was Noun 26
            real_verb_4 = "favored"
            real_noun_28 = "elites" # Was Noun 27
            real_noun_29 = "compliance" # Was Noun 28
            real_noun_30 = "poor" # Was Noun 29

            st.subheader("The Real Story:")
            st.write(f"While the history of **{real_noun_1}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{real_noun_2}**, the themes of our **{real_noun_3}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{real_noun_4}**. Perhaps the predominant theme throughout is the competition for and allocation of **{real_noun_resource}** within **{real_noun_society_plural}** across the globe.")
            st.write(f"From **{real_proper_noun_1}** to ancient Mexico and Rome to ancient **{real_proper_noun_2}**, we find **{real_plural_noun_3}** that create a **{real_adjective_1}** **{real_noun_5}** that assigns greater value to their own **{real_noun_6}**, and greater resources to themselves and their **{real_plural_noun_4}**. This comes, of course, at the expense of the **{real_plural_noun_5}**, the **{real_noun_7}** who have **{real_verb_1}** in the service of others of **{real_adjective_2}** standing. From prehistory through the modern era, **{real_noun_8}** has existed in various forms and under various names. This includes the **{real_noun_9}** of medieval **{real_proper_noun_3}** to the chattel **{real_noun_8}** of the early United States, and it persists to this day as wage **{real_noun_9}** where huge swaths of **{real_noun_10}** are unable to reap the full benefit of their own **{real_noun_11}**.")
            st.write(f"While this **{real_adjective_3}** stratification of **{real_noun_12}** and **{real_noun_13}** has persisted across **{real_noun_14}** and, **{real_adverb_1}**, across the globe, it is not naturally self sustaining. Indeed, **{real_noun_15}** have risen and **{real_noun_16}** have **{real_verb_2}** as **{real_adjective_4}** **{real_noun_17}** have reached across the globe seeking to **{real_verb_3}** the **{real_noun_18}** of the **{real_noun_19}** and **{real_noun_20}**. At the local level, **{real_noun_21}** has always been necessary to maintain **{real_noun_22}** of **{real_noun_23}**, from the **{real_noun_24}** patrols of **{real_adjective_5}** America to the targeting of **{real_noun_25}** by **{real_proper_noun_4}** today. Even on the individual level, **{real_noun_26}** has been a **{real_noun_27}** of the **{real_verb_4}** **{real_noun_28}** to compel the **{real_noun_29}** of the **{real_noun_30}**.")


        with col_right_viz:
            st.subheader("Visualizations of Important Data")
            st.write("Here you would integrate your actual data visualizations, potentially related to the BLS data we loaded earlier, or other relevant datasets.")

            st.write("### Sample Data Visualization (Random Data)")
            chart_data = pd.DataFrame(
                np.random.randn(50, 3),
                columns=['a', 'b', 'c']
            )
            st.line_chart(chart_data) # Streamlit's line_chart uses Altair, which is fine to keep.

            st.write("### Another Placeholder Chart")
            # Note: For a real app, you'd load/process this data within the Streamlit app itself.
            if 'df' in globals(): # Check if 'df' from previous cell exists (for demonstration)
                st.write("Here's a look at the BLS data you fetched:")
                st.dataframe(df.head())
            else:
                st.info("BLS data DataFrame 'df' not found. Please ensure previous data loading cells were run.")

            # Example: histogram with Plotly
            st.write("### Distribution of a Random Variable (Plotly)")
            arr = np.random.normal(1, 1, size=100) # Example data
            fig_plotly = px.histogram(x=arr, nbins=20, title="Random Variable Distribution")
            st.plotly_chart(fig_plotly)
        st.markdown("</div>", unsafe_allow_html=True) # Close custom frame

# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
