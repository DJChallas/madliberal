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
    if st.session_state.game_stage == 'madlib_input' or st.session_state.game_stage == 'madlib_reveal': # Show stripes and collage in input/reveal stages
        # Add alternating red and white stripes
        for i in range(47):
            color = "red" if i % 2 == 0 else "#FFFFFF"
            st.markdown(f'<div style="height: 20px; background-color: {color}; width: 100%; margin: 0; padding: 0;"></div>', unsafe_allow_html=True)

        # Only display collage in madlib_input stage, not madlib_reveal
        if st.session_state.game_stage == 'madlib_input':
            display_text_collage()

    elif st.session_state.game_stage == 'visualizations' or st.session_state.game_stage == 'industry_visualizations': # Show 'The Real Story' and navigation in left sidebar for visualization stages
        st.subheader("The Real Story:")
        st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From Mesopotamia to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

        st.markdown("-" * 3)

        if st.button("Unemployment Visualizations", key="unemployment_viz_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'visualizations'
            st.rerun()
        if st.button("Industry Visualizations", key="industry_viz_btn_sidebar", use_container_width=True):
            st.session_state.game_stage = 'industry_visualizations'
            st.rerun()
        if st.button("About this Project", key="about_project_btn_sidebar_common", use_container_width=True):
            st.session_state.game_stage = 'about_project'
            st.rerun()
        display_text_collage()

    elif st.session_state.game_stage == 'about_project': # Show 'Collage' and navigation in left sidebar
        display_text_collage()
        st.markdown("-" * 3) # Separator

        if st.button("Unemployment Visualizations", key="unemployment_viz_btn_sidebar_common", use_container_width=True):
            st.session_state.game_stage = 'visualizations'
            st.rerun()
        if st.button("Industry Visualizations", key="industry_viz_btn_sidebar_common", use_container_width=True):
            st.session_state.game_stage = 'industry_visualizations'
            st.rerun()
        if st.button("About this Project", key="about_project_btn_sidebar_about", use_container_width=True):
            st.session_state.game_stage = 'about_project'
            st.rerun()

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
                # Verb 1 is removed, 'toiled' is inserted directly
                ("Adjective 2", "adjective_2"),
                ("Noun 8", "noun_8"),
                ("Noun 9", "noun_9"),
                ("Proper Noun 3", "proper_noun_3"),
                ("Noun 10", "noun_10"),
                ("Noun 11", "noun_11"),
                ("Noun 12", "noun_12"), # Noun 12 here

                ("Adjective 3", "adjective_3"),
                ("Noun 13", "noun_13"),
                ("Noun 14", "noun_14"),
                ("Noun 15", "noun_15"),
                ("Adverb 1", "adverb_1"),
                ("Noun 16", "noun_16"),
                ("Noun 17", "noun_17"),
                ("Verb 1", "verb_2"), # Changed label from Verb 2 to Verb 1
                ("Adjective 4", "adjective_4"),
                ("Noun 18", "noun_18"),
                ("Verb 2", "verb_3"), # Changed label from Verb 3 to Verb 2
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
                ("Verb 3", "verb_4"), # Changed label from Verb 4 to Verb 3
                ("Noun 29", "noun_29"),
                ("Noun 30", "noun_30"),
                ("Noun 31", "noun_31"),
            ]

            # Define default values for the Mad Lib form
            default_madlib_values = {
                "noun_1": "girl",
                "noun_2": "school",
                "noun_3": "classes",
                "noun_4": "homework",
                "noun_resource": "friends",
                "noun_society_plural": "students",
                "proper_noun_2": "Paris",
                "plural_noun_3": "cliques",
                "adjective_1": "popular",
                "noun_5": "group",
                "noun_6": "reputation",
                "plural_noun_4": "followers",
                "plural_noun_5": "outcasts",
                "noun_7": "nerds",
                "adjective_2": "cool",
                "noun_8": "gossip",
                "noun_9": "rumors",
                "proper_noun_3": "New York",
                "noun_10": "girls",
                "noun_11": "attention",
                "noun_12": "looks",
                "adjective_3": "intense",
                "noun_13": "popularity",
                "noun_14": "drama",
                "noun_15": "friendships",
                "adverb_1": "always",
                "noun_16": "rivalries",
                "noun_17": "secrets",
                "verb_2": "broken",
                "adjective_4": "mean",
                "noun_18": "girls",
                "verb_3": "spread",
                "noun_19": "stories",
                "noun_20": "boys",
                "noun_21": "exclusion",
                "noun_22": "social",
                "noun_23": "hierarchy",
                "noun_24": "queen",
                "adjective_5": "high-school",
                "noun_25": "newcomers",
                "proper_noun_4": "The Plastics",
                "noun_26": "bullying",
                "noun_27": "weapon",
                "noun_28": "leaders",
                "verb_4": "manipulate",
                "noun_29": "crowd",
                "noun_30": "losers",
                "noun_31": "scapegoats"
            }

            input_values = {}

            # Paragraph 1 - at the start
            st.markdown("While the history of <span style='color:red;'>NOUN 1</span> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <span style='color:red;'>NOUN 2</span>, the themes of our <span style='color:red;'>NOUN 3</span> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <span style='color:red;'>NOUN 4</span>. Perhaps the predominant theme throughout is the competition for and allocation of <span style='color:red;'>PLURAL NOUN 1</span> within <span style='color:red;'>PLURAL NOUN 2</span> across the globe.", unsafe_allow_html=True)

            # Input fields 0-5 (Noun 1 through Plural Noun 2)
            cols = st.columns(3)
            for i in range(6):
                label, key = input_fields_all[i]
                with cols[(i - 0) % 3]: # Adjusted for 0-based indexing
                    input_values[key] = st.text_input(label, key=key, value=default_madlib_values.get(key, ''))

            # Paragraph 2 - after Plural Noun 2
            st.markdown("From Mesopotamia to ancient Mexico and Rome to ancient <span style='color:red;'>PROPER NOUN 2</span>, we find <span style='color:red;'>PLURAL NOUN 3</span> that create a <span style='color:red;'>ADJECTIVE 1</span><span style='color:black;'> | </span><span style='color:red;'>NOUN 5</span> that assigns greater value to their own <span style='color:red;'>NOUN 6</span>, and greater resources to themselves and their <span style='color:red;'>PLURAL NOUN 4</span>. This comes, of course, at the expense of the <span style='color:red;'>PLURAL NOUN 5</span>, the <span style='color:red;'>NOUN 7</span> who have toiled in the service of others of <span style='color:red;'>ADJECTIVE 2</span> standing. From prehistory through the modern era, <span style='color:red;'>NOUN 8</span> has existed in various forms and under various names. This includes the <span style='color:red;'>NOUN 9</span> of medieval <span style='color:red;'>PROPER NOUN 3</span> to the chattel <span style='color:red;'>NOUN 9</span> of the early United States, and it persists to this day as wage <span style='color:red;'>NOUN 10</span> where huge swaths of <span style='color:red;'>NOUN 11</span> are unable to reap the full benefit of their own <span style='color:red;'>NOUN 12</span>.", unsafe_allow_html=True)

            # Input fields 6-21 (Proper Noun 2 through Noun 12, 'verb_1' is skipped, so 15 fields)
            cols = st.columns(3)
            for i in range(6, 21): # Adjusted range: 22 - 1 (for removed Verb 1) = 21
                label, key = input_fields_all[i]
                with cols[(i - 6) % 3]:
                    input_values[key] = st.text_input(label, key=key, value=default_madlib_values.get(key, ''))

            # Paragraph 3 - after Noun 12
            st.markdown("While this <span style='color:red;'>ADJECTIVE 3</span> stratification of <span style='color:red;'>NOUN 13</span> and <span style='color:red;'>NOUN 14</span> has persisted across <span style='color:red;'>NOUN 15</span> and, <span style='color:red;'>ADVERB 1</span>, across the globe, it is not naturally self sustaining. Indeed, <span style='color:red;'>NOUN 16</span> have risen and <span style='color:red;'>NOUN 17</span> have <span style='color:red;'>VERB 1</span> as <span style='color:red;'>ADJECTIVE 4</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 18</span> have reached across the globe seeking to <span style='color:red;'>VERB 2</span> the <span style='color:red;'>NOUN 19</span> of the <span style='color:red;'>NOUN 20</span> and <span style='color:red;'>NOUN 21</span>. At the local level, <span style='color:red;'>NOUN 22</span> has always been necessary to maintain <span style='color:red;'>NOUN 23</span> of <span style='color:red;'>NOUN 24</span>, from the <span style='color:red;'>NOUN 25</span> patrols of <span style='color:red;'>ADJECTIVE 5</span> America to the targeting of <span style='color:red;'>NOUN 26</span> by <span style='color:red;'>PROPER NOUN 4</span> today. Even on the individual level, <span style='color:red;'>NOUN 27</span> has been a <span style='color:red;'>NOUN 28</span> of the <span style='color:red;'>VERB 3</span> <span style='color:black;'> | </span><span style='color:red;'>NOUN 29</span> to compel the <span style='color:red;'>NOUN 30</span> of the <span style='color:red;'>NOUN 31</span>.", unsafe_allow_html=True)

            # Input fields 21+ (Adjective 3 through Noun 31) - Adjusted start index
            cols = st.columns(3)
            for i in range(21, len(input_fields_all)):
                label, key = input_fields_all[i]
                with cols[(i - 21) % 3]: # Adjusted for new 0-based indexing relative to this loop
                    input_values[key] = st.text_input(label, key=key, value=default_madlib_values.get(key, ''))

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
        st.markdown(f"While the history of <b>{answers['noun_1']}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{answers['noun_2']}</b>, the themes of our <b>{answers['noun_3']}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{answers['noun_4']}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{answers['noun_resource']}</b> within <b>{answers['noun_society_plural']}</b> across the globe.", unsafe_allow_html=True)
        st.markdown(f"From Mesopotamia to ancient Mexico and Rome to ancient <b>{answers['proper_noun_2']}</b>, we find <b>{answers['plural_noun_3']}</b> that create a <b>{answers['adjective_1']}</b> <b>{answers['noun_5']}</b> that assigns greater value to their own <b>{answers['noun_6']}</b>, and greater resources to themselves and their <b>{answers['plural_noun_4']}</b>. This comes, of course, at the expense of the <b>{answers['plural_noun_5']}</b>, the <b>{answers['noun_7']}</b> who have toiled in the service of others of <b>{answers['adjective_2']}</b> standing. From prehistory through the modern era, <b>{answers['noun_8']}</b> has existed in various forms and under various names. This includes the <b>{answers['noun_9']}</b> of medieval <b>{answers['proper_noun_3']}</b> to the chattel <b>{answers['noun_9']}</b> of the early United States, and it persists to this day as wage <b>{answers['noun_10']}</b> where huge swaths of <b>{answers['noun_11']}</b> are unable to reap the full benefit of their own <b>{answers['noun_12']}</b>.", unsafe_allow_html=True)
        st.markdown(f"While this <b>{answers['adjective_3']}</b> stratification of <b>{answers['noun_13']}</b> and <b>{answers['noun_14']}</b> has persisted across <b>{answers['noun_15']}</b> and, <b>{answers['adverb_1']}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{answers['noun_16']}</b> have risen and <b>{answers['noun_17']}</b> have <b>{answers['verb_2']}</b> as <b>{answers['adjective_4']}</b> <b>{answers['noun_18']}</b> have reached across the globe seeking to <b>{answers['verb_3']}</b> the <b>{answers['noun_19']}</b> of the <b>{answers['noun_20']}</b> and <b>{answers['noun_21']}</b>. At the local level, <b>{answers['noun_22']}</b> has always been necessary to maintain <b>{answers['noun_23']}</b> of <b>{answers['noun_24']}</b>, from the <b>{answers['noun_25']}</b> patrols of <b>{answers['adjective_5']}</b> America to the targeting of <b>{answers['noun_26']}</b> by <b>{answers['proper_noun_4']}</b> today. Even on the individual level, <b>{answers['noun_27']}</b> has been a <b>{answers['noun_28']}</b> of the <b>{answers['verb_4']}</b> <b>{answers['noun_29']}</b> to compel the <b>{answers['noun_30']}</b> of the <b>{answers['noun_31']}</b>.", unsafe_allow_html=True)

        st.subheader("The Real Story:")
        # The real story variables are now defined globally
        st.markdown(f"While the history of <b>{real_noun_1}</b> stretches back for millennia, we find certain themes that reverberate throughout time. The earliest history is only available to us in whispers, evidence gleaned from bones and potshards. As we move towards the <b>{real_noun_2}</b>, the themes of our <b>{real_noun_3}</b> grow louder, a cacophony of evidence from writings, recordings, and oral traditions, <b>{real_noun_4}</b>. Perhaps the predominant theme throughout is the competition for and allocation of <b>{real_noun_resource}</b> within <b>{real_noun_society_plural}</b> across the globe.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px; margin-bottom: 1em;'>From <b>{real_proper_noun_1}</b> to ancient Mexico and Rome to ancient <b>{real_proper_noun_2}</b>, we find <b>{real_plural_noun_3}</b> that create a <b>{real_adjective_1}</b> <b>{real_noun_5}</b> that assigns greater value to their own <b>{real_noun_6}</b>, and greater resources to themselves and their <b>{real_plural_noun_4}</b>. This comes, of course, at the expense of the <b>{real_plural_noun_5}</b>, the <b>{real_noun_7}</b> who have <b>{real_verb_1}</b> in the service of others of <b>{real_adjective_2}</b> standing. From prehistory through the modern era, <b>{real_noun_8}</b> has existed in various forms and under various names. This includes the <b>{real_noun_9}</b> of medieval <b>{real_proper_noun_3}</b> to the chattel <b>{real_noun_8}</b> of the early United States, and it persists to this day as wage <b>{real_noun_9}</b> where huge swaths of <b>{real_noun_10}</b> are unable to reap the full benefit of their own <b>{real_noun_11}</b>.</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-right: 15px;'>While this <b>{real_adjective_3}</b> stratification of <b>{real_noun_12}</b> and <b>{real_noun_13}</b> has persisted across <b>{real_noun_14}</b> and, <b>{real_adverb_1}</b>, across the globe, it is not naturally self sustaining. Indeed, <b>{real_noun_15}</b> have risen and <b>{real_noun_16}</b> have <b>{real_verb_2}</b> as <b>{real_adjective_4}</b> <b>{real_noun_17}</b> have reached across the globe seeking to <b>{real_verb_3}</b> the <b>{real_noun_18}</b> of the <b>{real_noun_19}</b> and <b>{real_noun_20}</b>. At the local level, <b>{real_noun_21}</b> has always been necessary to maintain <b>{real_noun_22}</b> of <b>{real_noun_23}</b>, from the <b>{real_noun_24}</b> patrols of <b>{real_adjective_5}</b> America to the targeting of <b>{real_noun_25}</b> by <b>{real_proper_noun_4}</b> today. Even on the individual level, <b>{real_noun_26}</b> has been a <b>{real_noun_27}</b> of the <b>{real_verb_4}</b> <b>{real_noun_28}</b> to compel the <b>{real_noun_29}</b> of the <b>{real_noun_30}</b>.</div>", unsafe_allow_html=True)

        col1_viz, col2_viz, col3_viz = st.columns([1,1,1])
        with col2_viz:
            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
            if st.button("Proceed to Visualizations"):
                st.session_state.game_stage = 'visualizations'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

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

            # Data Cleaning
            if not df.empty:
                df['value'] = df['value'].astype(str).str.replace(r'\s+\(\d+\)', '', regex=True)
                df['value'] = pd.to_numeric(df['value'], errors='coerce') / 100
                df_filtered = df.dropna(subset=['value']).copy()

                # Store df_filtered in session state for display on 'About This Project' page
                st.session_state.df_cleaned_for_display = df_filtered.copy()

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

                label_mapping = {
                    'Asian': 'Asian, Men/Women',
                    'White Men': 'White Men',
                    'Men': 'Men, All Races',
                    'Women': 'Women, All Races',
                    'Hispanic or Latino': 'Hispanic or Latino, Men/Women',
                    'Black or African American': 'Black or African American, Men/Women'
                }

                other_demographics_ordered = avg_unemployment_df[
                    avg_unemployment_df['series_name'] != 'White Women'
                ].set_index('series_name').loc[comparison_order].reset_index()

                for index, row in other_demographics_ordered.iterrows():
                    comparison_group_name = row['series_name']
                    display_comparison_group_name = label_mapping.get(comparison_group_name, comparison_group_name)

                    comparison_df = pd.DataFrame({
                        'series_name': ['White Women', display_comparison_group_name],
                        'value': [white_women_avg['value'], row['value']]
                    })

                    fig = px.bar(
                        comparison_df,
                        x='series_name',
                        y='value',
                        title=f"Average Unemployment Rate: White Women vs. {display_comparison_group_name} in {year}",
                        labels={'series_name': 'Demographic Group', 'value': 'Average Unemployment Rate (Proportion)'},
                        color='series_name'
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
                st.markdown("The current calculations for unemployment are generated by averaging the seasonal unemployment percentages for all of the listed categories for a period of one year starting from the most recent release by the US Bureau of Labor Statistics: Men, Women, White Men, White Women, Black or African American, Hispanic or Latino and Asian. The data used for Hispanic or Latino is from a subcategory for unemployment statistics independent of the White, Black and Asian datasets.")
                plot_unemployment_by_sex(avg_unemployment_latest_year, latest_full_year)
                plot_unemployment_by_race(avg_unemployment_latest_year, latest_full_year)
                st.subheader("Mad Liberal Comparisons")
                plot_white_women_comparisons(avg_unemployment_latest_year, latest_full_year)
            else:
                st.warning("Cannot generate visualizations, data not available.")

    # --- Industry Visualizations Stage ---
    elif st.session_state.game_stage == 'industry_visualizations':
        viz_col = st.columns([1]) # Use a single column for visualizations in main_content

        with viz_col[0]:
            st.subheader("Industry Visualizations about Sex and Race")
            st.write("The Department of Labor presents a measure of data called Employed people by detailed occupation, sex, race, and Hispanic or Latino ethnicity (https://www.bls.gov/cps/cpsaat11.htm) that presents percentages of demographics employed in each of those occupations, grouped by industry. I’ve collected data for the primary Industries for gender and race to compare the distribution of demographics across some of the most popular occupations shown there. A regression analysis is provided from the data, however, it should not be considered to be representative of the entire US job market, only illustrative of the occupations and industries shown here. Where possible the main Industry is represented as well as the most popular occupations by statistics calculated by the BLS.")
            st.markdown("""
                **Management, professional, and related occupations**
                * Management, business, and financial operations occupations
                * Business and financial operations occupations
                * Professional and related occupations
                * Architecture and engineering occupations
                * Life, physical, and social science occupations
                * Community and social service occupations
                * Legal occupations
                * Education, training, and library occupations
                * Arts, design, entertainment, sports, and media occupations
                * Healthcare practitioners and technical occupations
                **Service occupations**
                * Healthcare support occupations
                * Protective service occupations
                * Food preparation and serving related occupations
                * Building and grounds cleaning and maintenance occupations
                * Personal care and service occupations
                **Sales and office occupations**
                * Sales and related occupations
                * Office and administrative support occupations
                **Natural resources, construction, and maintenance occupations**
                * Farming, fishing, and forestry occupations
                * Construction and extraction occupations
                * Installation, maintenance, and repair occupations
                **Production, transportation, and material moving occupations**
                * Production occupations
                * Transportation and material moving occupations
            """)

    elif st.session_state.game_stage == 'about_project':
        st.header("About This Project")
        st.markdown("""
The first half of my adult life I dedicated to creating art. Primarily music and video - finally producing a body of paintings before starting a graduate program at UNO in Data Science. While attending a liberal arts college in the Midwest I was subjected to civil rights abuses that changed the way I thought and perceived the world. These experiences drove me further into the pursuit of art as a form of social criticism and spirituality. The work I created has become artifacts of the life I’m leaving behind.

For me the pursuit of spirituality can be best understood as a search for truth, to understand the metaphysical nature of reality - the sciences inform us about nature and consciousness itself through measured processes and measured reporting. While art is a personal presentation of the truth, science is collective expression of it. The process must be explained, defined and understood for expression to be considered “correct.”

What has become troubling to me as I mature are the common bounds our mediated environment normalizes as reality. Because once these bounds become distorted our collective perception of reality becomes distorted. This project is a way for me to examine the limits of Classic Liberalism by parodying the normative reality of Modern Liberalism, focusing on the most dangerous thinkers in Human History: White Women.

Thank you to the individuals from Econ 8320: Tools for Data Analysis with shirts and hairstyling provided by Professor Dustin White. Series for visualizations from BLS: LNS14000006, LNS14000009, LNS14000003, LNS14032183, LNS14000002, LNS14000001, LNS14000005, and LNS14000004
""")

        st.markdown("-" * 3)

        # Display cleaned data if available
        if 'df_cleaned_for_display' in st.session_state and not st.session_state.df_cleaned_for_display.empty:
            st.subheader("Cleaned Data Preview:")
            st.dataframe(st.session_state.df_cleaned_for_display)

            # Center the download button
            col_dl_left, col_dl_center, col_dl_right = st.columns([1,1,1])
            with col_dl_center:
                csv = st.session_state.df_cleaned_for_display.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Full Cleaned Data",
                    data=csv,
                    file_name='cleaned_unemployment_data.csv',
                    mime='text/csv',
                )
        else:
            st.info("Cleaned data will appear here after visiting the 'Unemployment Visualizations' section.")


# --- Footer ---
st.markdown("<div style='text-align: center;'>--- Casey Hallas 2026 ---</div>", unsafe_allow_html=True)
