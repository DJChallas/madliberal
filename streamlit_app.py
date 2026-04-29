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
    if st.session_state.game_stage == 'madlib_input' or st.session_state.game_stage == 'madlib_reveal': # Show stripes only in input/reveal stages
        # Add alternating red and white stripes like the US flag (47 stripes)
        for i in range(47):
            color = "red" if i % 2 == 0 else "#FFFFFF"
            st.markdown(f'<div style="height: 20px; background-color: {color}; width: 100%; margin: 0; padding: 0;"></div>', unsafe_allow_html=True)

    elif st.session_state.game_stage == 'visualizations': # Show 'The Real Story' and navigation in left sidebar for visualizations stage
        st.subheader("The Real Story:")
        st.markdown(f"While the history of **{real_noun_1}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{real_noun_2}**, the themes of our **{real_noun_3}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{real_noun_4}**. Perhaps the predominant theme throughout is the competition for and allocation of **{real_noun_resource}** within **{real_noun_society_plural}** across the globe.", unsafe_allow_html=True)
        st.markdown(f"From Mesopotamia to ancient Mexico and Rome to ancient **{real_proper_noun_2}**, we find **{real_plural_noun_3}** that create a **{real_adjective_1}** **{real_noun_5}** that assigns greater value to their own **{real_noun_6}**, and greater resources to themselves and their **{real_plural_noun_4}**. This comes, of course, at the expense of the **{real_plural_noun_5}**, the **{real_noun_7}** who have **{real_verb_1}** in the service of others of **{real_adjective_2}** standing. From prehistory through the modern era, **{real_noun_8}** has existed in various forms and under various names. This includes the **{real_noun_9}** of medieval **{real_proper_noun_3}** to the chattel **{real_noun_8}** of the early United States, and it persists to this day as wage **{real_noun_9}** where huge swaths of **{real_noun_10}** are unable to reap the full benefit of their own **{real_noun_11}**.", unsafe_allow_html=True)
        st.markdown(f"While this **{real_adjective_3}** stratification of **{real_noun_12}** and **{real_noun_13}** has persisted across **{real_noun_14}** and, **{real_adverb_1}**, across the globe, it is not naturally self sustaining. Indeed, **{real_noun_15}** have risen and **{real_noun_16}** have **{real_verb_2}** as **{real_adjective_4}** **{real_noun_17}** have reached across the globe seeking to **{real_verb_3}** the **{real_noun_18}** of the **{real_noun_19}** and **{real_noun_20}**. At the local level, **{real_noun_21}** has always been necessary to maintain **{real_noun_22}** of **{real_noun_23}**, from the **{real_noun_24}** patrols of **{real_adjective_5}** America to the targeting of **{real_noun_25}** by **{real_proper_noun_4}** today. Even on the individual level, **{real_noun_26}** has been a **{real_noun_27}** of the **{real_verb_4}** **{real_noun_28}** to compel the **{real_noun_29}** of the **{real_noun_30}**.", unsafe_allow_html=True)

        st.markdown("---") # Separator

        if st.button("About this Project", key="about_project_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'about_project'
            st.rerun()

    elif st.session_state.game_stage == 'about_project': # Show 'The Real Story' and 'Back to Visualizations' button in left sidebar for this stage
        st.subheader("The Real Story:")
        st.markdown(f"While the history of **{real_noun_1}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{real_noun_2}**, the themes of our **{real_noun_3}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{real_noun_4}**. Perhaps the predominant theme throughout is the competition for and allocation of **{real_noun_resource}** within **{real_noun_society_plural}** across the globe.", unsafe_allow_html=True)
        st.markdown(f"From Mesopotamia to ancient Mexico and Rome to ancient **{real_proper_noun_2}**, we find **{real_plural_noun_3}** that create a **{real_adjective_1}** **{real_noun_5}** that assigns greater value to their own **{real_noun_6}**, and greater resources to themselves and their **{real_plural_noun_4}**. This comes, of course, at the expense of the **{real_plural_noun_5}**, the **{real_noun_7}** who have **{real_verb_1}** in the service of others of **{real_adjective_2}** standing. From prehistory through the modern era, **{real_noun_8}** has existed in various forms and under various names. This includes the **{real_noun_9}** of medieval **{real_proper_noun_3}** to the chattel **{real_noun_8}** of the early United States, and it persists to this day as wage **{real_noun_9}** where huge swaths of **{real_noun_10}** are unable to reap the full benefit of their own **{real_noun_11}**.", unsafe_allow_html=True)
        st.markdown(f"While this **{real_adjective_3}** stratification of **{real_noun_12}** and **{real_noun_13}** has persisted across **{real_noun_14}** and, **{real_adverb_1}**, across the globe, it is not naturally self sustaining. Indeed, **{real_noun_15}** have risen and **{real_noun_16}** have **{real_verb_2}** as **{real_adjective_4}** **{real_noun_17}** have reached across the globe seeking to **{real_verb_3}** the **{real_noun_18}** of the **{real_noun_19}** and **{real_noun_20}**. At the local level, **{real_noun_21}** has always been necessary to maintain **{real_noun_22}** of **{real_noun_23}**, from the **{real_noun_24}** patrols of **{real_adjective_5}** America to the targeting of **{real_noun_25}** by **{real_proper_noun_4}** today. Even on the individual level, **{real_noun_26}** has been a **{real_noun_27}** of the **{real_verb_4}** **{real_noun_28}** to compel the **{real_noun_29}** of the **{real_noun_30}**.", unsafe_allow_html=True)
        st.markdown("---") # Separator
        if st.button("Back to Visualizations", key="back_to_viz_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'visualizations'
            st.rerun()


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
                with cols[(i - 0) % 3]: # Adjusted for 0-based indexing
                    input_values[key] = st.text_input(label, key=key)

            # Paragraph 2 - after Plural Noun 2
            st.markdown("From Mesopotamia to ancient Mexico and Rome to ancient <span style='color:red;'>PROPER NOUN 2</span>, we find <span style='color:red;'>PLURAL NOUN 3</span> that create a <span style='color:red;'>ADJECTIVE 1</span><span style='color:black;'> | </span><span style='color:red;'>NOUN 5</span> that assigns greater value to their own <span style='color:red;'>NOUN 6</span>, and greater resources to themselves and their <span style='color:red;'>PLURAL NOUN 4</span>. This comes, of course, at the expense of the <span style='color:red;'>PLURAL NOUN 5</span>, the <span style='color:red;'>NOUN 7</span> who have <span style='color:red;'>VERB 1</span> in the service of others of <span style='color:red;'>ADJECTIVE 2</span> standing. From prehistory through the modern era, <span style='color:red;'>NOUN 8</span> has existed in various forms and under various names. This includes the <span style='color:red;'>NOUN 9</span> of medieval <span style='color:red;'>PROPER NOUN 3</span> to the chattel <span style='color:red;'>NOUN 8</span> of the early United States, and it persists to this day as wage <span style='color:red;'>NOUN 9</span> where huge swaths of **{real_noun_10}** are unable to reap the full benefit of their own <span style='color:red;'>NOUN 11</span>.", unsafe_allow_html=True)

            # Input fields 6-20 (Proper Noun 2 through Noun 11)
            cols = st.columns(3)
            for i in range(6, 21):
                label, key = input_fields_all[i]
                with cols[(i - 6) % 3]:
                    input_values[key] = st.text_input(label, key=key)

            # Paragraph 3 - after Noun 11
            st.markdown("While this <span style='color:red;'>ADJECTIVE 3</span> stratification of <span style='color:red;'>NOUN 12</span> and <span style='color:red;'>NOUN 13</span> has persisted across <span style='color:red;'>NOUN 14</span> and, <span style='color:red;'>ADVERB 1</span>, across the globe, it is not naturally self sustaining. Indeed, <span style='color:red;'>NOUN 15</span> have risen and <span style='color:red;'>NOUN 16}</span> have <span style='color:red;'>VERB 2</span> as <span style='color:red;'>ADJECTIVE 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 17</span> have reached across the globe seeking to <span style='color:red;'>VERB 3</span> the <span style='color:red;'>NOUN 18}</span> of the <span style='color:red;'>NOUN 19</span> and <span style='color:red;'>NOUN 20</span>. At the local level, <span style='color:red;'>NOUN 21</span> has always been necessary to maintain <span style='color:red;'>NOUN 22</span> of <span style='color:red;'>NOUN 23}</span>, from the <span style='color:red;'>NOUN 24</span> patrols of <span style='color:red;'>ADJECTIVE 5</span> America to the targeting of <span style='color:red;'>NOUN 25</span> by **{real_proper_noun_4}** today. Even on the individual level, <span style='color:red;'>NOUN 26</span> has been a <span style='color:red;'>NOUN 27</span> of the <span style='color:red;'>VERB 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 28</span> to compel the <span style='color:red;'>NOUN 29</span> of the <span style='color:red;'>NOUN 30</span>.", unsafe_allow_html=True)

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
        st.subheader("Your Story:")
        answers = st.session_state.madlib_answers
        st.write(f"While the history of **{answers['noun_1']}** stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the **{answers['noun_2']}**, the themes of our **{answers['noun_3']}** grow louder, a cacophony of evidence from writings, recordings, and oral traditions, **{answers['noun_4']}**. Perhaps the predominant theme throughout is the competition for and allocation of **{answers['noun_resource']}** within **{answers['noun_society_plural']}** across the globe.")
        st.write(f"From Mesopotamia to ancient Mexico and Rome to ancient **{answers['proper_noun_2']}**, we find **{answers['plural_noun_3']}** that create a **{answers['adjective_1']}** **{answers['noun_5']}** that assigns greater value to their own **{answers['noun_6']}**, and greater resources to themselves and their **{answers['plural_noun_4']}**. This comes, of course, at the expense of the **{answers['plural_noun_5']}**, the **{answers['noun_7']}** who have **{answers['verb_1']}** in the service of others of **{answers['adjective_2']}** standing. From prehistory through the modern era, **{answers['noun_8']}** has existed in various forms and under various names. This includes the **{answers['noun_9']}** of medieval **{answers['proper_noun_3']}** to the chattel **{answers['noun_8']}** of the early United States, and it persists to this day as wage **{answers['noun_9']}** where huge swaths of **{answers['noun_10']}** are unable to reap the full benefit of their own **{answers['noun_11']}**.")
        st.write(f"While this **{answers['adjective_3']}** stratification of **{answers['noun_12']}** and **{answers['noun_13']}** has persisted across **{answers['noun_14']}** and, **{answers['adverb_1']}**, across the globe, it is not naturally self sustaining. Indeed, **{answers['noun_15']}** have risen and **{answers['noun_16']}** have **{answers['verb_2']}** as **{answers['adjective_4']}** **{answers['noun_17']}** have reached across the globe seeking to **{real_verb_3}** the **{answers['noun_18']}** of the **{answers['noun_19']}** and **{answers['noun_20']}**. At the local level, **{answers['noun_21']}** has always been necessary to maintain **{answers['noun_22']}** of **{answers['noun_23']}**, from the **{answers['noun_24']}** patrols of **{answers['adjective_5']}** America to the targeting of **{answers['noun_25']}** by **{real_proper_noun_4}** today. Even on the individual level, **{answers['noun_26']}** has been a **{answers['noun_27']}** of the **{answers['verb_4']}** **{answers['noun_28']}** to compel the **{answers['noun_29']}** of the **{answers['noun_30']}**.")

        st.subheader("The Real Story:")
        # The real story variables are now defined globally
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

        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing before collage
        all_real_words = [
            real_noun_1, real_noun_2, real_noun_3, real_noun_4, real_noun_resource, real_noun_society_plural,
            real_proper_noun_1, real_proper_noun_2, real_plural_noun_3, real_adjective_1, real_noun_5, real_noun_6,
            real_plural_noun_4, real_plural_noun_5, real_noun_7, real_verb_1, real_adjective_2, real_noun_8, real_noun_9,
            real_proper_noun_3, real_noun_10, real_noun_11, real_adjective_3, real_noun_12, real_noun_13, real_noun_14,
            real_adverb_1, real_noun_15, real_noun_16, real_verb_2, real_adjective_4, real_noun_17, real_verb_3,
            real_noun_18, real_noun_19, real_noun_20, real_noun_21, real_noun_22, real_noun_23, real_noun_24,
            real_adjective_5, real_noun_25, real_proper_noun_4, real_noun_26, real_noun_27, real_verb_4, real_noun_28,
            real_noun_29, real_noun_30
        ]
        # Shuffle for a more collage-like effect and vary styles
        random.seed(42) # for reproducibility
        random.shuffle(all_real_words)

        collage_html = ""
        colors = ['#FF0000', '#0000FF', '#333333', '#666666'] # Red, Blue, Dark Gray, Medium Gray
        font_sizes = ['1.0em', '1.2em', '1.4em', '1.6em', '1.8em']

        for word in all_real_words:
            color = random.choice(colors)
            font_size = random.choice(font_sizes)
            collage_html += f"<span style='color:{color}; font-size:{font_size}; margin: 0 5px; display: inline-block;'>{word}</span> "
        st.markdown(collage_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing after collage

    # --- Visualizations Stage ---
    elif st.session_state.game_stage == 'visualizations':
        viz_col = st.columns([1]) # Use a single column for visualizations in main_content

        with viz_col[0]:
            # Data Import and Initial Processing (extracted from 4ba3fbe6)
            headers = {'Content-type': 'application/json'}
            current_year = datetime.now().year
            data = json.dumps({
                "seriesid": ['LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183', 'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004'],
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
            elif 'message' in json_data:
                st.error(f"API Error: {json_data['message']}")
            else:
                st.warning("Unknown API response format or no data in 'Results'.")

            # Data Cleaning (extracted from 312be3e4)
            if not df.empty:
                df['value'] = df['value'].astype(str).str.replace(r'\s+\(\d+\)', '', regex=True)
                df['value'] = pd.to_numeric(df['value'], errors='coerce') / 100
                df_filtered = df.dropna(subset=['value']).copy()

                sn_map = {
                    'LNS14000006': 'Black or African American',
                    'LNS14000009': 'Hispanic or Latino',
                    'LNS14000003': 'White',
                    'LNS14032183': 'Asian',
                    'LNS14000002': 'Women',
                    'LNS14000001': 'Men',
                    'LNS14000005': 'White Women',
                    'LNS14000004': 'White Men'
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
                    'Men',
                    'Women',
                    'White Men',
                    'White Women',
                    'Black or African American',
                    'Hispanic or Latino',
                    'Asian',
                    'White'
                ]
                avg_unemployment_latest_year['series_name'] = pd.Categorical(
                    avg_unemployment_latest_year['series_name'],
                    categories=desired_order,
                    ordered=True
                )
                avg_unemployment_latest_year = avg_unemployment_latest_year.sort_values('series_name')

            else:
                st.warning("DataFrame 'df' not available for cleaning. Please ensure the data import ran successfully.")

            # --- Visualization Functions ---
            def plot_unemployment_by_sex(avg_unemployment_df, year):
                sex_groups = ['Men', 'Women', 'White Men', 'White Women']
                df_sex = avg_unemployment_df[avg_unemployment_df['series_name'].isin(sex_groups)].copy()
                df_sex = df_sex.sort_values(by='value', ascending=False)

                fig_sex = px.bar(
                    df_sex,
                    x='series_name',
                    y='value',
                    title=f'Average Unemployment Rate by Sex in {year}',
                    labels={'series_name': 'Demographic Group', 'value': 'Average Unemployment Rate (Proportion)'},
                    color='series_name'
                )
                fig_sex.update_layout(
                    xaxis_title='Demographic Group',
                    yaxis_title='Average Unemployment Rate (Proportion)',
                    showlegend=False
                )
                st.plotly_chart(fig_sex, use_container_width=True)

            def plot_unemployment_by_race(avg_unemployment_df, year):
                race_groups = ['Black or African American', 'Hispanic or Latino', 'Asian', 'White']
                df_race = avg_unemployment_df[avg_unemployment_df['series_name'].isin(race_groups)].copy()
                df_race = df_race.sort_values(by='value', ascending=False)

                fig_race = px.bar(
                    df_race,
                    x='series_name',
                    y='value',
                    title=f'Average Unemployment Rate by Race in {year}',
                    labels={'series_name': 'Demographic Group', 'value': 'Average Unemployment Rate (Proportion)'},
                    color='series_name'
                )
                fig_race.update_layout(
                    xaxis_title='Demographic Group',
                    yaxis_title='Average Unemployment Rate (Proportion)',
                    showlegend=False
                )
                st.plotly_chart(fig_race, use_container_width=True)

            def plot_white_women_comparisons(avg_unemployment_df, year):
                white_women_avg = avg_unemployment_df[avg_unemployment_df['series_name'] == 'White Women'].iloc[0]

                comparison_order = [
                    'Asian',
                    'White Men',
                    'Men',
                    'Women',
                    'Hispanic or Latino',
                    'Black or African American'
                ]

                other_demographics_ordered = avg_unemployment_df[
                    avg_unemployment_df['series_name'] != 'White Women'
                ].set_index('series_name').loc[comparison_order].reset_index()

                for index, row in other_demographics_ordered.iterrows():
                    comparison_group_name = row['series_name']

                    comparison_df = pd.DataFrame({
                        'series_name': ['White Women', comparison_group_name],
                        'value': [white_women_avg['value'], row['value']]
                    })

                    # Define specific colors based on user request
                    color_map = {
                        'White Women': px.colors.qualitative.Plotly[0], # Blue (assuming default first color)
                        comparison_group_name: px.colors.qualitative.Plotly[1] # Red (assuming default second color)
                    }

                    fig = px.bar(
                        comparison_df,
                        x='series_name',
                        y='value',
                        title=f"Average Unemployment Rate: White Women vs. {comparison_group_name} in {year}",
                        labels={'series_name': 'Demographic Group', 'value': 'Average Unemployment Rate (Proportion)'},
                        color='series_name',
                        color_discrete_map=color_map # Use the defined color map
                    )

                    fig.update_layout(
                        xaxis_title='Demographic Group',
                        yaxis_title='Average Unemployment Rate (Proportion)',
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # --- Display Visualizations ---
            if not df.empty and 'avg_unemployment_latest_year' in locals():
                st.subheader("Average Unemployment Rates")
                st.markdown("text text text text text") # Added placeholder text as per user request
                plot_unemployment_by_sex(avg_unemployment_latest_year, latest_full_year)
                plot_unemployment_by_race(avg_unemployment_latest_year, latest_full_year)
                st.subheader("White Women Comparisons")
                plot_white_women_comparisons(avg_unemployment_latest_year, latest_full_year)
            else:
                st.warning("Cannot generate visualizations, data not available.")

            # --- Occupation Analysis Section (Integrated) ---
            st.markdown(f'<div style="height: 20px; background-color: red; width: 100%; margin: 20px 0; padding: 0;"></div>', unsafe_allow_html=True)
            st.subheader("Occupation by Gender and Race")
            st.write("here are employment percentages for major industry divisons from across the US Economy focused on popular job types for each industry.")
            st.markdown("""
            *   Management, professional, and related occupations
                *   Management, business, and financial operations occupations
                *   Business and financial operations occupations
                *   Professional and related occupations
                *   Architecture and engineering occupations
                *   Life, physical, and social science occupations
                *   Community and social service occupations
                *   Legal occupations
                *   Education, training, and library occupations
                *   Arts, design, entertainment, sports, and media occupations
                *   Healthcare practitioners and technical occupations
            *   Service occupations
                *   Healthcare support occupations
                *   Protective service occupations
                *   Food preparation and serving related occupations
                *   Building and grounds cleaning and maintenance occupations
                *   Personal care and service occupations
            *   Sales and office occupations
                *   Sales and related occupations
                *   Office and administrative support occupations
            *   Natural resources, construction, and maintenance occupations
                *   Farming, fishing, and forestry occupations
                *   Construction and extraction occupations
                *   Installation, maintenance, and repair occupations
            *   Production, transportation, and material moving occupations
                *   Production occupations
                *   Transportation and material moving occupations
            """)

        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing before collage
        all_real_words = [
            real_noun_1, real_noun_2, real_noun_3, real_noun_4, real_noun_resource, real_noun_society_plural,
            real_proper_noun_1, real_proper_noun_2, real_plural_noun_3, real_adjective_1, real_noun_5, real_noun_6,
            real_plural_noun_4, real_plural_noun_5, real_noun_7, real_verb_1, real_adjective_2, real_noun_8, real_noun_9,
            real_proper_noun_3, real_noun_10, real_noun_11, real_adjective_3, real_noun_12, real_noun_13, real_noun_14,
            real_adverb_1, real_noun_15, real_noun_16, real_verb_2, real_adjective_4, real_noun_17, real_verb_3,
            real_noun_18, real_noun_19, real_noun_20, real_noun_21, real_noun_22, real_noun_23, real_noun_24,
            real_adjective_5, real_noun_25, real_proper_noun_4, real_noun_26, real_noun_27, real_verb_4, real_noun_28,
            real_noun_29, real_noun_30
        ]
        # Shuffle for a more collage-like effect and vary styles
        random.seed(42) # for reproducibility
        random.shuffle(all_real_words)

        collage_html = ""
        colors = ['#FF0000', '#0000FF', '#333333', '#666666'] # Red, Blue, Dark Gray, Medium Gray
        font_sizes = ['1.0em', '1.2em', '1.4em', '1.6em', '1.8em']

        for word in all_real_words:
            color = random.choice(colors)
            font_size = random.choice(font_sizes)
            collage_html += f"<span style='color:{color}; font-size:{font_size}; margin: 0 5px; display: inline-block;'>{word}</span> "
        st.markdown(collage_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing after collage

    elif st.session_state.game_stage == 'about_project':
        st.header("About This Project")
        st.write("This project explores the interplay of historical socioeconomic structures and contemporary economic indicators, particularly focusing on unemployment across different demographics.")
        st.write("Through a 'Mad Liberal' narrative, it aims to engage users with historical contexts of resource allocation and inequality, transitioning into data-driven visualizations of current labor statistics from the US Bureau of Labor Statistics (BLS).")
        st.write("The goal is to provide insights into how historical patterns might manifest in modern economic disparities, encouraging a deeper understanding of societal structures and their impact on individuals.")
        st.write("The project was developed by Casey Hallas for UNO Econ 8320 in May 2026.")

        st.markdown("---") # Separator

        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing before collage
        all_real_words = [
            real_noun_1, real_noun_2, real_noun_3, real_noun_4, real_noun_resource, real_noun_society_plural,
            real_proper_noun_1, real_proper_noun_2, real_plural_noun_3, real_adjective_1, real_noun_5, real_noun_6,
            real_plural_noun_4, real_plural_noun_5, real_noun_7, real_verb_1, real_adjective_2, real_noun_8, real_noun_9,
            real_proper_noun_3, real_noun_10, real_noun_11, real_adjective_3, real_noun_12, real_noun_13, real_noun_14,
            real_adverb_1, real_noun_15, real_noun_16, real_verb_2, real_adjective_4, real_noun_17, real_verb_3,
            real_noun_18, real_noun_19, real_noun_20, real_noun_21, real_noun_22, real_noun_23, real_noun_24,
            real_adjective_5, real_noun_25, real_proper_noun_4, real_noun_26, real_noun_27, real_verb_4, real_noun_28,
            real_noun_29, real_noun_30
        ]
        # Shuffle for a more collage-like effect and vary styles
        random.seed(42) # for reproducibility
        random.shuffle(all_real_words)

        collage_html = ""
        colors = ['#FF0000', '#0000FF', '#333333', '#666666'] # Red, Blue, Dark Gray, Medium Gray
        font_sizes = ['1.0em', '1.2em', '1.4em', '1.6em', '1.8em']

        for word in all_real_words:
            color = random.choice(colors)
            font_size = random.choice(font_sizes)
            collage_html += f"<span style='color:{color}; font-size:{font_size}; margin: 0 5px; display: inline-block;'>{word}</span> "
        st.markdown(collage_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # Add spacing after collage


# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
