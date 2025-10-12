import streamlit as st
import pandas as pd
import geonamescache

st.set_page_config(page_title="Nomad Network Navigator", layout="wide")

def load_cities():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    city_list = [(city['name'], city['countrycode']) for city_id, city in cities.items()]
    return sorted(city_list, key=lambda x: x[0])

def main():
    if 'session_data' not in st.session_state:
        st.session_state.session_data = {
            'role': None,
            'skills': [],
            'expertise': {},
            'city': None,
            'saved_sessions': {}
        }

    st.title("Nomad Network Navigator")

    if st.session_state.session_data['role'] is None:
        role = st.selectbox("Select Role", ["Freelancer", "Remote Project Lead", "Community Organizer"])
        if st.button("Start Session"):
            st.session_state.session_data['role'] = role
            st.rerun()
    else:
        st.write(f"Current Role: {st.session_state.session_data['role']}")
        if st.button("Reset Session"):
            st.session_state.session_data = {
                'role': None,
                'skills': [],
                'expertise': {},
                'city': None,
                'saved_sessions': {}
            }
            st.rerun()

        st.subheader("Input Skills and Expertise")
        skill_input = st.text_input("Enter a skill (e.g., graphic design, Python)")
        if skill_input:
            expertise = st.selectbox(f"Expertise level for {skill_input}", ["Beginner", "Intermediate", "Advanced"])
            if st.button("Add Skill"):
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
            st.table(skills_df)

        st.subheader("Select Home City")
        cities = load_cities()
        city_names = [f"{city[0]}, {city[1]}" for city in cities]
        selected_city = st.selectbox("Choose your city", city_names)
        if st.button("Set City"):
            st.session_state.session_data['city'] = selected_city
            st.rerun()

        if st.session_state.session_data['city']:
            st.write(f"Selected City: {st.session_state.session_data['city']}")

        st.subheader("Save Session")
        session_name = st.text_input("Enter session name")
        if st.button("Save Session"):
            if session_name:
                st.session_state.session_data['saved_sessions'][session_name] = {
                    'skills': st.session_state.session_data['skills'],
                    'expertise': st.session_state.session_data['expertise'],
                    'city': st.session_state.session_data['city']
                }
                with open(f"{session_name}.json", "w") as f:
                    pd.Series(st.session_state.session_data['saved_sessions'][session_name]).to_json(f)
                st.success(f"Session '{session_name}' saved.")

        st.subheader("Load Session")
        session_to_load = st.selectbox("Select session to load", list(st.session_state.session_data['saved_sessions'].keys()))
        if st.button("Load Session"):
            if session_to_load:
                st.session_state.session_data['skills'] = st.session_state.session_data['saved_sessions'][session_to_load]['skills']
                st.session_state.session_data['expertise'] = st.session_state.session_data['saved_sessions'][session_to_load]['expertise']
                st.session_state.session_data['city'] = st.session_state.session_data['saved_sessions'][session_to_load]['city']
                st.rerun()

if __name__ == "__main__":
    main()
