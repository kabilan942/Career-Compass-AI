import streamlit as st
from src import module_1, module_2, module_3, module_4, module_5, homepage

st.set_page_config(
    page_title="Career Compass AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app helps you explore colleges and branches under JoSAA in India.",
        'Report a bug': "mailto:support@example.com"
    }
)

# Sidebar for navigation
st.sidebar.title("Navigation")
app_choice = st.sidebar.radio("Go to:", ("Home Page", "Specialization Recommender", "Branch Explorer", 
                                         "College Filter & Map", "College–Branch Insight Hub", "JEE Docs Chat"))

# Conditional routing
if app_choice == "Home Page":
    homepage.run()
if app_choice == "Specialization Recommender":
    module_1.run()
if app_choice == "Branch Explorer":
    module_2.run()
if app_choice == "College Filter & Map":
    module_3.run()
if app_choice == "College–Branch Insight Hub":
    module_4.run()
elif app_choice == "JEE Docs Chat":
    module_5.run()
