import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# --- ENVIRONMENT SETUP ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SESSION STATE SETUP ---
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = {}
if 'patient_notes' not in st.session_state:
    st.session_state.patient_notes = ""
if 'symptom_checker_notes' not in st.session_state:
    st.session_state.symptom_checker_notes = ""
if 'doc_helper_notes' not in st.session_state:
    st.session_state.doc_helper_notes = ""
if 'patient_education_notes' not in st.session_state:
    st.session_state.patient_education_notes = ""
if 'curaai_history' not in st.session_state:
    st.session_state.curaai_history = []

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to...",
    [
        "Patient Intake",
        "Symptom Checker",
        "Documentation Helper",
        "Patient Education",
        "CuraAI",
        "Custom Question",
        "Feedback"
    ]
)

# --- PAGE LOGIC ---
if page == "Patient Intake":
    st.title("Patient Intake")
    name = st.text_input("Patient Name")
    age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
    if st.button("Save Patient Profile"):
        st.session_state.patient_profile = {"name": name, "age": age}
        st.success("Patient profile saved!")
    st.text_area("Patient Notes (Click to expand)", key="patient_notes")

elif page == "Symptom Checker":
    st.title("Symptom Checker")
    st.text_area("Symptom Checker Notes (Editable)", key="symptom_checker_notes")
    # Add your symptom checking logic here as needed

elif page == "Documentation Helper":
    st.title("Documentation Helper")
    st.text_area("Documentation Helper Notes (Editable)", key="doc_helper_notes")
    # Add your documentation helper logic here as needed

elif page == "Patient Education":
    st.title("Patient Education")
    st.text_area("Patient Education Notes (Editable)", key="patient_education_notes")
    # Add your patient education logic here as needed

elif page == "CuraAI":
    st.title("CuraAI: AI-Powered Clinical Assistant")
    user_query = st.text_area("Enter any clinical question or request here:")
    if st.button("Ask CuraAI"):
        if user_query:
            prompt = f"Clinical question: {user_query}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_answer = response.choices[0].message.content.strip()
            st.session_state.curaai_history.append({
                "query": user_query,
                "response": ai_answer
            })
            st.success("CuraAI response added to history.")
        else:
            st.warning("Please enter a question.")
    # Show the most recent CuraAI Q&A
    if st.session_state.curaai_history:
        st.markdown("### CuraAI History")
        for entry in reversed(st.session_state.curaai_history):
            st.markdown(f"**Query:** {entry['query']}")
            st.markdown(f"**Response:** {entry['response']}")
            st.markdown("---")

elif page == "Custom Question":
    st.title("Custom Clinical Question")
    st.write("Coming soon! Build your own Q&A modules.")

elif page == "Feedback":
    st.title("Feedback")
    feedback = st.text_area("We want your feedback:")
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")

# Show saved patient profile at the bottom of every page
if st.session_state.patient_profile:
    st.sidebar.markdown("---")
    st.sidebar.write("**Current Patient Profile:**")
    st.sidebar.write(st.session_state.patient_profile)