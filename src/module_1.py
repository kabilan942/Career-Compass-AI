import streamlit as st
import os
import pandas as pd

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# take environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# load the GROQ API Key
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model_name = "llama3-70b-8192"
llm = ChatGroq(model=groq_model_name, groq_api_key=groq_api_key)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # current directory
TRUNK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))      # Move up one level to reach the trunk
DATA_FILE = os.path.join(TRUNK_DIR, 'data', 'josaa_seats_aggregated.csv')
df = pd.read_csv(DATA_FILE)
clusters = df['Branch Cluster'].unique()

PROMPT = """

<context>
You are an expert AI career counselor helping students find their most suited branch to study based on a Class 12 student's questionnaire responses.
</context>

<Instructions>

Based on a Class 12 student's questionnaire responses,
recommend the **top 3 engineering subgroups** from this list: {clusters}

Give reason for each recommendation.

Student responses in questionnaire:
1. Core Subject Strength: {q1}
2. On campus, you’d most enjoy: {q2}
3. Which future role appeals most?: {q3}
4. You prefer problems that are: {q4}
5. Most appealing workplace: {q5}
6. Scale & Impact Preference: {q6}
7. Creative Balance (Scale of 1 to 5): Creative: {q7_creative}
8. Analytical Balance (Scale of 1 to 5): Analytic: {q7_analytic}
9. Which club are you most drawn to?: {q8}

Only provide the recommendations along with their reasons. Don't add statemetns such as "I've considered the student's core 
subject strengths, their interest in running lab experiments, and their preference for data-driven problems." at the end.

</Instructions>

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI career counselor helping students find their most suited branch to study based on a Class 12 student's questionnaire responses."),
    ("human", PROMPT),
])

chain = prompt | llm

def get_top_subgroups(responses: dict):
    """
    responses keys: q1, q2, q3, q4, q5, q6, q7_creative, q7_analytic, q8
    """
    result = chain.invoke(responses)
    return result.content

def run():
    
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;'>
        <h4>Welcome to the Engineering Specialization Recommendor!</h4>
        <p>
        This short questionnaire is designed to help you discover the engineering specializations that best align with your interests, strengths, and career aspirations.
        Based on your answers, an AI model will recommend the top fields that may suit you best, along with explanations for each suggestion.
        </p>
        <p>
        Take your time to reflect and answer honestly — this isn't a test, but a tool to guide you toward informed academic and career decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("\n")
    st.markdown("**Please answer the following questions:**")

    # Q1: Core Subject Strength
    q1 = st.multiselect(
        "Which subjects do you excel at? (Select all that apply)",
        ["Mathematics", "Physics", "Chemistry", "Biology", "Economics"]
    )

    # Q2: Preferred Campus Activities
    q2 = st.radio(
        "On campus, you’d most enjoy:",
        [
            "Coding hackathons or programming projects",
            "Building circuits or electronics kits",
            "Designing structures or models (e.g. small bridges, houses)",
            "Running lab experiments (chemistry/biotech)",
            "Mapping, surveying, or geology field trips",
            "Textile weaving or fabric design workshops",
            "Urban planning / architectural sketching"
        ]
    )

    # Q3: Career Vision
    q3 = st.multiselect(
        "Which future role appeals most?",
        [
            "Data scientist / AI specialist",
            "Software developer / IT architect",
            "Mechanical designer or automotive engineer",
            "Civil/structural engineer (roads, dams)",
            "Chemical process engineer (pharma/energy)",
            "Environmental consultant / renewable-energy engineer",
            "Research scientist in physics or materials",
            "Agricultural technologist or food-tech innovator",
            "Urban planner or infrastructure manager",
            "Mining engineer or geologist",
            "Textile technologist or sustainable-fashion engineer",
            "Biomedical/biotech engineer (medical devices)"
        ]
    )

    # Q4: Problem-Solving Style
    q4 = st.multiselect(
        "You prefer problems that are:",
        [
            "Highly quantitative (heavy math & modeling)",
            "Hands-on with physical prototypes",
            "Creative/design oriented (CAD, UI, product form)",
            "Data-driven (statistics, ML, optimization)",
            "Field-based (surveying, sampling, site visits)"
        ]
    )

    # Q5: Work Environment
    q5 = st.multiselect(
        "Most appealing workplace:",
        [
            "A high-tech lab or silicon fab",
            "A software startup or big tech office",
            "A construction site or city planning office",
            "A chemical plant or refinery",
            "An environmental / renewable-energy field station",
            "A university or R&D institute",
            "A farm or agro-processing facility",
            "A fashion/textile mill"
        ]
    )

    # Q6: Scale & Impact
    q6 = st.radio(
        "Would you rather work on:",
        [
            "Global-scale systems (internet, power grids, AI models)",
            "Community-scale projects (local roads, water supply, urban design)",
            "Small-batch or custom products (medical devices, specialty materials)"
        ]
    )

    # Q7: Creative vs Analytical
    st.markdown("Rate yourself (1–5) on each axis:")
    q7_creative = st.slider("Creativity (art, design, new ideas):", 1, 5, 3)
    q7_analytic = st.slider("Analysis (data, numbers, logic):", 1, 5, 3)

    # Q8: Extracurricular Clubs
    q8 = st.multiselect(
        "Which club are you most drawn to?",
        [
            "Robotics Club",
            "Coding & Data Science Club",
            "Civil/Architecture Society",
            "Chemistry/Biotech Society",
            "Environmental/Green Tech Club",
            "Materials & Manufacturing Club",
            "Agriculture & Food Innovation Club",
            "Mining & Geology Forum",
            "Textile & Apparel Club"
        ]
    )
    
    # Submit
    if st.button("Submit and Generate Recommendation"):
        user_answers = {
            "q1": ", ".join(q1),
            "q2": q2,
            "q3": ", ".join(q3),
            "q4": ", ".join(q4),
            "q5": ", ".join(q5),
            "q6": q6,
            "q7_creative": str(q7_creative),
            "q7_analytic": str(q7_analytic),
            "q8": ", ".join(q8)
        }

        user_answers["clusters"]= clusters
        ai_recom = get_top_subgroups(user_answers)

        st.subheader("Recommended Branch Clusters:")

        st.write(ai_recom)

