import streamlit as st
import io
from datetime import datetime

def generate_summary():
    buffer = io.StringIO()
    buffer.write(f"Session Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    for i, entry in enumerate(st.session_state.chat_log, 1):
        buffer.write(f"{i}. Module: {entry['module']}\n")
        buffer.write(f"   Q: {entry['query']}\n")
        buffer.write(f"   A: {entry['response']}\n\n")
    
    return buffer.getvalue()

def run():
    
    # --- Page Header ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 12px; padding: 24px; background-color: #f4f8fc;'>

    <h3 style='text-align: center; color: #004080; font-weight: normal;'>
    <span style='font-size: 20px;'>Welcome to</span> <span style='font-size: 30px;'>Career Compass AI</span>
    </h3>

    <h6 style='text-align: center; font-weight: normal; color: #333;'>Explore. Compare. Decide.</h4>

    <p style="font-size: 17px; line-height: 1.6; margin-top: 20px;">
    This is your personalized companion to discovering the <strong>right engineering branch</strong>, finding your <strong>best-fit colleges</strong>, and making <strong>smart, informed decisions</strong> — all in one place.
    </p>

    <p style="font-size: 16px; line-height: 1.6;">
    Whether you're starting to explore or narrowing down choices, <em>Career Compass AI</em> helps you:
    <ul style="font-size: 16px; padding-left: 20px; line-height: 1.8;">
    <li>Understand which specializations match your interests and strengths</li>
    <li>Explore branches and careers</li>
    <li>Filter and find colleges that suit your preferences and scores</li>
    <li>Compare college-branch combinations side-by-side</li>
    <li>Get instant answers from official JEE documents</li>
    </ul>
    </p>

    <p style="font-size: 17px; margin-top: 16px;">
    <strong>Let’s get started on mapping your path to engineering success!</strong>
    </p>
                               
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Module 1 ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;'>
    <h4>1️⃣ Specialization Recommender</h4>
    <p style="font-size:16px;">
    This short questionnaire is designed to help you discover the engineering specializations that best align with your interests, strengths, and career aspirations.
    </p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li>Answer honestly — this is not a test!</li>
        <li>Get personalized recommendations on engineering branches that match your profile.</li>
        <li>Understand why each field suits your goals.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- Module 2 ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #fdfdfd; margin-top: 20px;'>
    <h4>2️⃣ Branch Explorer</h4>
    <p style="font-size:16px;">Explore and choose the right engineering branch based on your interests or career goals.</p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li><strong>Learn About Branches:</strong> Ask about a specific branch (e.g., <code>Tell me about Mechanical Engineering</code>).</li>
        <li><strong>Branch Recommender:</strong> Share your goal (e.g., <code>I want to work in robotics</code>) or topics you enjoy (e.g., <code>Maths</code>, <code>Design</code>).</li>
        <li>Get structured, AI-generated responses with career outlook, subjects involved, and relevance.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- Module 3 ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9; margin-top: 20px;'>
    <h4>3️⃣ College Filter & Map</h4>
    <p style="font-size:16px;">Find the best colleges and branches based on your preferences and JEE scores.</p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li>Filter by: institute type (IIT/NIT/IIIT/GFTI), degree, quota, branch, and JEE rank or score.</li>
        <li>See all matching college-branch options in a sortable table.</li>
        <li>Explore institute locations interactively on the map.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- Module 4 ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #fdfdfd; margin-top: 20px;'>
    <h4>4️⃣ College–Branch Insight Hub</h4>
    <p style="font-size:16px;">Make smarter academic decisions by accessing detailed insights and comparisons.</p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li><strong>Info Bot:</strong> Learn about any specific college & branch (e.g., <code>IIT Kanpur, Aerospace</code>).</li>
        <li><strong>Comparison Bot:</strong> Compare two options (e.g., <code>IIT Delhi CSE vs IIIT Hyderabad CSE</code>).</li>
        <li>Understand curriculum, fees, placements, student culture, and more!</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- Module 5 ---
    st.markdown("""
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9; margin-top: 20px;'>
    <h4>5️⃣ JEE Docs Chat</h4>
    <p style="font-size:16px;">
    Ask questions directly to the chatbot and get accurate responses from official JEE documents.
    </p>
    <p><strong>What are JEE Mains & Advanced?</strong></p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li><strong>JEE Mains:</strong> Conducted by NTA for entry to NITs, IIITs, and GFTIs.</li>
        <li><strong>JEE Advanced:</strong> Conducted by IITs for admission into IITs.</li>
        <li><strong>JoSAA Counselling:</strong> Admission handled through <a href="https://josaa.nic.in/" target="_blank">https://josaa.nic.in/</a>.</li>
    </ul>
    <p><strong>Documents Used:</strong></p>
    <ul style="font-size:15px; padding-left: 20px;">
        <li><a href="https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2024/10/2024102824.pdf" target="_blank">JEE Mains Information Bulletin 2025</a></li>
        <li><a href="https://jeeadv.ac.in/documents/IBEnglish_2025.pdf" target="_blank">JEE Advanced Information Bulletin 2025</a></li>
    </ul>
    <p>Example Questions: <code>What is the eligibility for JEE Advanced?</code>, <code>When does registration start?</code></p>
    </div>
    """, unsafe_allow_html=True)