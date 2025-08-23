# Institute-Branch Info & Comparison Bot

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
import os
import pandas as pd

# take environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# load the GROQ API Key and Hugging Face Token
groq_api_key = os.getenv("GROQ_API_KEY")

# LLM setup using Groq
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# Importing the dataset for college category and name, branches and more info link
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # current directory
TRUNK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))      # Move up one level to reach the trunk
DATA_FILE = os.path.join(TRUNK_DIR, 'data', 'josaa_branchwise_info_viz.csv')
INFO_BOT_PROMPT = os.path.join(TRUNK_DIR, 'prompts', 'info_bot_prompt.txt')
COMPARISON_BOT_PROMPT = os.path.join(TRUNK_DIR, 'prompts', 'comparison_bot_prompt.txt')

df = pd.read_csv(DATA_FILE)

with open(INFO_BOT_PROMPT, "r") as file:
    info_bot_prompt = file.read()

with open(COMPARISON_BOT_PROMPT, "r") as file:
    comparison_bot_prompt = file.read()

def run():

    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;'>

    <h4>College-Branch Insight Hub</h4>

    We help you make smarter academic decisions by providing **detailed insights** and **comparisons** between college-branch combinations using AI.

    ### How to Use:

    1. **Select a Mode:**
    - <strong>Info Bot</strong> – Get in-depth information about a specific <strong>college & branch</strong>: curriculum, fees, placements, student reviews, and more.
    - <strong>Comparison Bot</strong> – Compare <strong>two college-branch combinations</strong> side by side to evaluate academic and career prospects.

    2. **Ask a Question:**
    - For Info Bot: Enter a college name and <branch (e.g., <code>IIT Bombay, Mechanical Engineering</code>).
    - For Comparison Bot: Enter two college-branch pairs (e.g., <code>IIT Madras CSE vs IIIT Hyderabad CSE</code>).

    3. **View AI Insights** – Get a structured breakdown to guide your decision-making process.

    <strong>Make confident and informed academic choices!</strong>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("\n")

    # Initialize session state
    if "mode" not in st.session_state:
        st.session_state.mode = None

    # UI: Toggle between Info Bot and Comparison Bot
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Info Bot"):
            st.session_state.mode = "info_bot"
    with col2:
        if st.button("Comparison Bot"):
            st.session_state.mode = "comparison_bot"

    # Prompt selection logic
    if st.session_state.mode is None:
        st.warning("Please select a mode to continue.")
        st.stop()

    # --- INFO BOT Mode ---
    if st.session_state.mode == "info_bot":
        st.subheader("College & Branch Info")

        categories = ['All'] + sorted(list(df['College Category'].unique()))
        selected_category = st.selectbox("Select College Category", categories)

        # Filter college list based on selected category
        if selected_category == 'All':
            filtered_colleges = df['College Name'].unique()
        else:
            filtered_colleges = df[df['College Category'] == selected_category]['College Name'].unique()

        college = st.selectbox("Select College", sorted(filtered_colleges), key="info_college")

        # Filter branches based on selected college
        branches = df[df["College Name"] == college]["Branch Name"].unique()
        branch = st.selectbox("Select Branch", sorted(branches), key="info_branch")
        detailed_info = list(df[(df['College Name']==college) & (df['Branch Name']==branch)]['View Details'])[0]

        if st.button("Get Info"):
            # st.spinner() is a context manager in Streamlit that shows a temporary loading spinner while executing a block of code.
            with st.spinner("Fetching information..."):
                prompt = PromptTemplate.from_template(info_bot_prompt)
                chain = prompt | llm
                response = chain.invoke({"college": college, "branch": branch, "josaa_info": detailed_info})
                st.write("### Result")
                st.markdown(response.content)

    # --- COMPARISON BOT Mode ---
    elif st.session_state.mode == "comparison_bot":
        st.subheader("Compare Two Colleges & Branches")
        
        colleges = ["NIT Trichy", "IIT Madras", "c3", "c4", "c5"]
        branches = ["Production Engineering", "Mechanical Engineering", "b3", "b4", "b5"]

        col1, col2 = st.columns(2)
        with col1:

            categories1 = ['All'] + sorted(list(df['College Category'].unique()))
            selected_category1 = st.selectbox("Select College Category 1", categories1)

            if selected_category1 == 'All':
                filtered_colleges1 = df['College Name'].unique()
            else:
                filtered_colleges1 = df[df['College Category'] == selected_category1]['College Name'].unique()
            college1 = st.selectbox("Select College 1", sorted(filtered_colleges1), key="c1")

            branches1 = df[df["College Name"] == college1]["Branch Name"].unique()
            branch1 = st.selectbox("Select Branch 1", sorted(branches1), key="b1")
            detailed_info1 = list(df[(df['College Name']==college1) & (df['Branch Name']==branch1)]['View Details'])[0]

        with col2:

            categories2 = ['All'] + sorted(list(df['College Category'].unique()))
            selected_category2 = st.selectbox("Select College Category 2", categories2)

            if selected_category2 == 'All':
                filtered_colleges2 = df['College Name'].unique()
            else:
                filtered_colleges2 = df[df['College Category'] == selected_category2]['College Name'].unique()
            college2 = st.selectbox("Select College 2", sorted(filtered_colleges2), key="c2")

            branches2 = df[df["College Name"] == college2]["Branch Name"].unique()
            branch2 = st.selectbox("Select Branch 2", sorted(branches2), key="b2")
            detailed_info2 = list(df[(df['College Name']==college2) & (df['Branch Name']==branch2)]['View Details'])[0]

        if st.button("Compare"):
            with st.spinner("Comparing..."):
                prompt = PromptTemplate.from_template(comparison_bot_prompt)
                chain = prompt | llm
                response = chain.invoke({
                    "college1": college1,
                    "branch1": branch1,
                    "josaa_info1": detailed_info1,
                    "college2": college2,
                    "branch2": branch2,
                    "josaa_info2": detailed_info2
                })
                st.write("### Comparison Result")
                st.markdown(response.content)