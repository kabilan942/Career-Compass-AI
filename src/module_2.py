# Branch Info 

import streamlit as st
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
import os

# take environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# load the GROQ API Key
groq_api_key = os.getenv("GROQ_API_KEY")

groq_model_name = "llama3-70b-8192"
llm = ChatGroq(model=groq_model_name, groq_api_key=groq_api_key)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # current directory
TRUNK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))      # Move up one level to reach the trunk
BRANCH_INFO_PROMPT = os.path.join(TRUNK_DIR, 'prompts', 'branch_info_prompt.txt')
CAREER_GOAL_PROMPT = os.path.join(TRUNK_DIR, 'prompts', 'career_goal_prompt.txt')

with open(BRANCH_INFO_PROMPT, "r") as file:
    branch_info_prompt = file.read()

with open(CAREER_GOAL_PROMPT, "r") as file:
    career_goal_prompt = file.read()

def run(): 

    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;'>

    <h4>Explore Your Engineering Path!</h4>

    <p style="font-size:18px; margin-bottom: 10px;">
    We help you explore and choose the right undergraduate branch based on your <strong>interests</strong> or <strong>career goals</strong>.
    </p>

    <p style="font-size:16px; margin-bottom: 6px;"><strong> How to Use:</strong></p>

    <ul style="font-size:16px; padding-left: 20px; line-height: 1.6;">
    <li><strong>Select a Mode:</strong><br>
        <strong>Learn About Branches</strong> – Get detailed information on a specific branch (subjects, career prospects, etc.)<br>
        <strong>Branch Recommender</strong> – Tell us what career you want or topics you liked in high school, and we'll suggest the best undergraduate branches for you.
    </li><br>

    <li><strong>Ask a Question:</strong><br>
    - For "Learn About Branches": Type a branch name (e.g., <code>Tell me about Mechanical Engineering</code>)<br>
    - For "Branch Recommender": Share your goal (e.g., <code>I want to become an aerospace engineer</code>) or subjects you liked (e.g., <code>Physics</code>, <code>Mechanics</code>)
    </li><br>

    <li><strong>View AI Recommendations:</strong> You'll get structured and helpful responses tailored to your input.</li>
    </ul>

    <p style="font-size:18px; margin-top: 12px;"><strong>Start exploring your future now!</strong></p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("\n")

    # Initialize session state variables
    if "mode" not in st.session_state:
        st.session_state.mode = None
    if "branch_name" not in st.session_state:
        st.session_state.branch_name = ""

    # Create two buttons for mode selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Learn About Branches"):
            st.session_state.mode = "branch_info"
    with col2:
        if st.button("Branch Recommender"):
            st.session_state.mode = "career_goal"

    # Ensure a mode is selected
    if st.session_state.mode is None:
        st.warning("Please select a mode to continue.")
        st.stop()

    # User Input Section (Changes Based on Mode)
    if st.session_state.mode == "branch_info":
        st.subheader("Learn About a Branch")
        branch_name = st.text_input("Enter the branch name (e.g., 'Mechanical Engineering'):")
        
        if branch_name:
            st.session_state.branch_name = branch_name  # Store branch name
            st.session_state.show_sections = False  # Reset section visibility

            # Buttons for different sections
            if st.button("Introduction"):
                st.session_state.show_sections = "introduction"
            if st.button("High School Concepts"):
                st.session_state.show_sections = "high_school"
            if st.button("College Subjects"):
                st.session_state.show_sections = "college_subjects"
            if st.button("Future Career Roles"):
                st.session_state.show_sections = "career_roles"

            # Fetch information from LLM only for selected sections
            if "show_sections" in st.session_state and st.session_state.show_sections:
                system_prompt = branch_info_prompt
                user_input = f"Provide {st.session_state.show_sections} information for {st.session_state.branch_name}."
                response = llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}])
                
                st.write(f"### {st.session_state.show_sections.replace('_', ' ').title()}:")
                st.write(response.content)

    elif st.session_state.mode == "career_goal":
        st.subheader("Branch Recommender")
        career_input = st.text_input("Tell us your career goal or subjects you liked:")

        if career_input:
            system_prompt = career_goal_prompt
            response = llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": career_input}])
            st.write("### AI Recommendation:")
            st.write(response.content)

    specializations = {
        "Aeronautical / Aerospace Engineering": "Specializes in aircraft and spacecraft design, aerodynamics, propulsion, and avionics. Prepares you for roles in the aviation industry, defense R&D, and space missions.",
        "Agricultural and Food Engineering": "Applies engineering principles to agriculture—crop processing, food preservation, irrigation systems, and farm machinery. Focus on improving food security and agribusiness.",
        "Architecture": "Blends art and engineering to design functional, aesthetic buildings and spaces. Involves structural basics, building materials, and urban design principles.",
        "Artificial Intelligence and Data Science": "Covers machine learning, deep learning, data mining, and big-data systems. Prepares you for AI research, data analytics, and building intelligent applications.",
        "Bio Tech and Engineering": "Merges biology with engineering to develop bioprocesses, genetic engineering, and medical devices. Applications include biopharmaceuticals, biofuels, and tissue engineering.",
        "Chemical Engineering": "Combines chemistry, physics, and biology to design processes for large-scale chemical production—petrochemicals, pharmaceuticals, plastics, and food processing.",
        "Chemistry": "A pure science program covering organic, inorganic, physical, and analytical chemistry. Opens paths in research labs, pharmaceuticals, materials science, and chemical analysis.",
        "Civil Engineering": "Studies the design, construction, and maintenance of infrastructure—roads, bridges, dams, and buildings. Covers structural analysis, geotechnical engineering, transportation systems, and urban planning.",
        "Computer Science and Engineering (CSE)": "Focuses on algorithms, data structures, software design, operating systems, databases, and computer networks. Prepares you for roles in software development, systems architecture, and high-performance computing.",
        "Economics": "Applies quantitative and qualitative methods to study markets, resource allocation, and policy. Valuable for roles in finance, consulting, and data-driven policy analysis.",
        "Electrical and Electronics Engineering (EEE)": "Encompasses power generation/distribution, electrical machines, control systems, and basic electronics. Trains you in circuit design, renewable energy systems, and industrial automation.",
        "Electronics and Communication Engineering (ECE)": "Covers analog/digital electronics, signal processing, telecommunications, and embedded systems. Equips you to work on everything from mobile networks to IoT hardware.",
        "Energy and Environment": "Integrates renewable energy technologies (solar, wind, biofuels) with environmental engineering (wastewater treatment, pollution control). Addresses sustainability and resource management.",
        "Engineering Design": "Focuses on product development, CAD/CAM, and human-centered design. Teaches you to take ideas from concept through prototyping to manufacturing.",
        "Geology": "Studies earth materials, rock formations, and geological processes—volcanism, tectonics, and sedimentology. Essential for exploration, environmental assessment, and hazard analysis.",
        "Industrial Engineering": "Optimizes complex systems and processes in manufacturing, logistics, and service industries. Uses operations research, quality control, and human-factors engineering to boost productivity.",
        "Information Technology": "Emphasizes network management, cybersecurity, database administration, and web/mobile application development. Preps you for managing and securing enterprise IT systems.",
        "Instrumentation Engineering": "Deals with sensors, transducers, and control instrumentation for industrial processes. Combines electronics, measurement, and automation for precise system monitoring.",
        "Mathematics": "Focuses on pure and applied math—calculus, algebra, statistics, and numerical methods. Foundation for careers in cryptography, modeling, finance, and academic research.",
        "Mechanical Engineering": "Deals with the design, analysis, and manufacturing of mechanical systems—engines, machines, HVAC, and robotics. Blends theory (thermodynamics, fluid mechanics) with hands-on prototyping.",
        "Metallurgical and Materials Engineering": "Explores the properties, processing, and performance of metals, ceramics, polymers, and composites. Applications range from aerospace alloys to biomedical implants and nanomaterials.",
        "Mining and Earth Sciences": "Covers mining techniques, mineral processing, and geological surveying. Trains you to locate, extract, and manage earth resources safely and sustainably.",
        "Physics": "A foundational science program studying mechanics, electromagnetism, quantum theory, and optics. Ideal for careers in research, teaching, instrumentation, and R&D labs.",
        "Planning": "Covers urban and regional planning, transportation systems, and infrastructure policy. Trains you to design sustainable cities and manage public-sector development projects.",
        "Textile Technology": "Studies fibers, yarns, fabrics, and textile processing. Includes weaving/knitting, dyeing/finishing, and sustainable textile innovations—key to the Erode textile cluster."
    }

    st.markdown('\n')

    st.markdown("""
    <div style='font-size:18px; font-weight:500;'>
        <strong>The following are the major specializations offered in JoSAA participating universities. Browse through them to understand what each field involves:</strong>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 24px 32px;
        margin-top: 20px;
    }

    .card {
        background-color: #f3f7fb;
        border-left: 6px solid #2c6ecb;
        padding: 20px 22px;
        border-radius: 10px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
        font-family: "Segoe UI", sans-serif;
        margin-bottom: 24px;
    }

    .card h4 {
        margin: 0 0 12px 0;
        color: #1a4c7c;
        font-size: 18px;
    }

    .card p {
        margin: 0;
        color: #333;
        font-size: 14.5px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card-grid'>", unsafe_allow_html=True)
    for name, desc in specializations.items():
        st.markdown(f"""
        <div class='card'>
            <h4>{name}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
