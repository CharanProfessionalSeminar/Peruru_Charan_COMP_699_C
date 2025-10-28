import streamlit as st
import pandas as pd
import geonamescache
import json
from pathlib import Path

st.set_page_config(page_title="Nomad Network Navigator", layout="wide")

@st.cache_data(show_spinner=False)
def load_cities():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    city_list = [(city['name'], city['countrycode']) for city_id, city in cities.items()]
    return sorted(city_list, key=lambda x: x[0])

def save_session_to_file(session_name, data):
    session_dir = Path("sessions")
    session_dir.mkdir(exist_ok=True)
    session_path = session_dir / f"{session_name}.json"
    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_saved_sessions():
    session_dir = Path("sessions")
    session_dir.mkdir(exist_ok=True)
    sessions = {}
    for file in session_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            sessions[file.stem] = json.load(f)
    return sessions

def main():
    if 'session_data' not in st.session_state:
        st.session_state.session_data = {
            'role': None,
            'skills': [],
            'expertise': {},
            'city': None,
            'saved_sessions': load_saved_sessions()
        }

    st.title("Nomad Network Navigator")

    if st.session_state.session_data['role'] is None:
        role = st.selectbox("Select Role", ["Freelancer", "Remote Project Lead", "Community Organizer"], key="role_select")
        if st.button("Start Session", key="start_btn"):
            st.session_state.session_data['role'] = role
            st.rerun()
    else:
        st.write(f"Current Role: {st.session_state.session_data['role']}")
        if st.button("Reset Session", key="reset_btn"):
            st.session_state.session_data = {
                'role': None,
                'skills': [],
                'expertise': {},
                'city': None,
                'saved_sessions': load_saved_sessions()
            }
            st.rerun()

        st.subheader("Input Skills and Expertise")
        skill_input = st.text_input("Enter a skill (e.g., graphic design, Python)", key="skill_input")
        if skill_input:
            expertise = st.selectbox(f"Expertise level for {skill_input}", ["Beginner", "Intermediate", "Advanced"], key="expertise_select")
            if st.button("Add Skill", key="add_skill_btn"):
                if skill_input not in st.session_state.session_data['skills']:
                    st.session_state.session_data['skills'].append(skill_input)
                    st.session_state.session_data['expertise'][skill_input] = expertise
                    st.rerun()

        if st.session_state.session_data['skills']:
            st.write("Current Skills:")
            skills_df = pd.DataFrame([
                {"Skill": skill, "Expertise": st.session_state.session_data['expertise'][skill]}
                for skill in st.session_state.session_data['skills']
            ])
            st.dataframe(skills_df, use_container_width=True)

        st.subheader("Select Home City")
        cities = load_cities()
        city_names = [f"{city[0]}, {city[1]}" for city in cities]
        selected_city = st.selectbox("Choose your city", city_names, key="city_select")
        if st.button("Set City", key="set_city_btn"):
            st.session_state.session_data['city'] = selected_city
            st.rerun()

        if st.session_state.session_data['city']:
            st.write(f"Selected City: {st.session_state.session_data['city']}")

        st.subheader("Save Session")
        session_name = st.text_input("Enter session name", key="session_name_input")
        if st.button("Save Session", key="save_session_btn"):
            if session_name:
                st.session_state.session_data['saved_sessions'][session_name] = {
                    'skills': st.session_state.session_data['skills'],
                    'expertise': st.session_state.session_data['expertise'],
                    'city': st.session_state.session_data['city']
                }
                save_session_to_file(session_name, st.session_state.session_data['saved_sessions'][session_name])
                st.success(f"Session '{session_name}' saved successfully.")
                st.rerun()

        st.subheader("Load Session")
        saved_session_names = list(st.session_state.session_data['saved_sessions'].keys())
        if saved_session_names:
            session_to_load = st.selectbox("Select session to load", saved_session_names, key="session_load_select")
            if st.button("Load Session", key="load_session_btn"):
                if session_to_load:
                    loaded_data = st.session_state.session_data['saved_sessions'][session_to_load]
                    st.session_state.session_data['skills'] = loaded_data['skills']
                    st.session_state.session_data['expertise'] = loaded_data['expertise']
                    st.session_state.session_data['city'] = loaded_data['city']
                    st.success(f"Session '{session_to_load}' loaded successfully.")
                    st.rerun()
        else:
            st.info("No saved sessions available.")

if __name__ == "__main__":
    main()
