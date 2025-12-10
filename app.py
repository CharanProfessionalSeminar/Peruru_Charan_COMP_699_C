import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from geonamescache import GeonamesCache
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(page_title="Nomad Network Navigator", layout="wide")

st.markdown(
    """
    <style>
    .css-18e3th9 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 1rem 3rem 3rem 3rem;
    }
    .stTitle {
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        color: #1f2937;
    }
    div.stButton > button:hover {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
        transition: 0.3s ease;
    }
    .stSelectbox, .stSlider {
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

gc = GeonamesCache()
cities = gc.get_cities()
city_list = []
for c in cities.values():
    if c['population'] > 50000:
        city_list.append({
            'name': c['name'],
            'country': c['countrycode'],
            'lat': c['latitude'],
            'lon': c['longitude'],
            'population': c['population']
        })
df_cities = pd.DataFrame(city_list)
df_cities['label'] = df_cities['name'] + ", " + df_cities['country']

SKILLS = [
    "Python", "JavaScript", "React", "Node.js", "TypeScript", "Java", "C#", "Go",
    "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Flutter", "UI/UX Design", "Graphic Design",
    "Figma", "Adobe XD", "Product Management", "Project Management", "Agile", "Scrum",
    "Data Science", "Machine Learning", "TensorFlow", "PyTorch", "SQL", "PostgreSQL",
    "MongoDB", "AWS", "DevOps", "Docker", "Kubernetes", "Blockchain", "Solidity",
    "Copywriting", "SEO", "Digital Marketing", "Video Editing", "Motion Graphics",
    "3D Modeling", "Blender", "Unity", "Unreal Engine", "Translation", "Content Writing"
]

EXPERTISE_LEVELS = ["Beginner", "Intermediate", "Advanced"]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def calculate_skill_demand(city_pop):
    base = city_pop / 1e6
    noise = np.random.uniform(0.7, 1.3, len(SKILLS))
    demand = base * noise
    demand = np.clip(demand, 0.1, 10.0)
    return dict(zip(SKILLS, demand))

@st.cache_data
def build_city_network():
    G = nx.Graph()
    for _, city in df_cities.iterrows():
        demand = calculate_skill_demand(city['population'])
        G.add_node(city['label'],
                   lat=city['lat'],
                   lon=city['lon'],
                   population=city['population'],
                   demand=demand)
    return G

def compute_match_score(user_skills, city_demand, expertise_weights):
    score = 0.0
    for skill, level in user_skills.items():
        if skill in city_demand:
            weight = expertise_weights[level]
            score += city_demand[skill] * weight
    return score

if 'role' not in st.session_state:
    st.session_state.role = None
if 'session_data' not in st.session_state:
    st.session_state.session_data = {}

st.title("Nomad Network Navigator")

with st.container():
    col1, col2, col3 = st.columns([3, 6, 1])
    with col1:
        role = st.selectbox("Select Role", ["", "Freelancer", "Remote Project Lead", "Community Organizer"], index=0)
        if role and role != st.session_state.role:
            st.session_state.role = role
            st.session_state.session_data = {}
    with col3:
        if st.button("Reset Session"):
            st.session_state.role = None
            st.session_state.session_data = {}

if not st.session_state.role:
    st.stop()

if st.session_state.role == "Freelancer":
    st.header("Freelancer Mode")
    with st.expander("Your Skills & Expertise", expanded=True):
        if 'skills' not in st.session_state.session_data:
            st.session_state.session_data['skills'] = {}
        for i in range(10):
            col_a, col_b, col_c = st.columns([3, 2, 1])
            with col_a:
                skill = st.selectbox(f"Skill {i+1}", [""] + SKILLS, key=f"skill_{i}")
            with col_b:
                level = st.selectbox("Level", EXPERTISE_LEVELS, key=f"level_{i}")
            with col_c:
                if st.button("Remove", key=f"rem_{i}") and skill:
                    if skill in st.session_state.session_data['skills']:
                        del st.session_state.session_data['skills'][skill]
            if skill and skill not in st.session_state.session_data['skills']:
                st.session_state.session_data['skills'][skill] = level

    home_city = st.selectbox("Your Home City", [""] + list(df_cities['label']), index=0)

    col1, col2 = st.columns(2)
    with col1:
        max_distance = st.slider("Max Distance (km)", 0, 20000, 5000)
        min_overlap = st.slider("Min Skill Overlap %", 0, 100, 60)
    with col2:
        w_skill = st.slider("Weight: Skill Match", 0.0, 1.0, 0.7, 0.05)
        w_proximity = 1.0 - w_skill

    expertise_weights = {"Beginner": 0.5, "Intermediate": 1.0, "Advanced": 1.8}

    if st.button("Run Simulation") and st.session_state.session_data['skills'] and home_city:
        with st.spinner("Building network..."):
            G = build_city_network()
            user_skills = st.session_state.session_data['skills']

            home_row = df_cities[df_cities['label'] == home_city].iloc[0]
            home_lat, home_lon = home_row['lat'], home_row['lon']

            results = []
            for node in G.nodes():
                if node == home_city:
                    continue
                city_data = G.nodes[node]
                dist = haversine(home_lat, home_lon, city_data['lat'], city_data['lon'])
                if dist > max_distance:
                    continue
                raw_score = compute_match_score(user_skills, city_data['demand'], expertise_weights)
                if raw_score == 0:
                    continue
                proximity_score = 1.0 / (1.0 + dist / 1000)
                total_score = w_skill * raw_score + w_proximity * proximity_score
                overlap_pct = (raw_score / (len(user_skills) * 1.8)) * 100
                if overlap_pct < min_overlap:
                    continue
                results.append({
                    'city': node,
                    'distance_km': round(dist),
                    'skill_score': round(raw_score, 2),
                    'proximity_score': round(proximity_score, 3),
                    'total_score': round(total_score, 3),
                    'overlap_pct': round(overlap_pct, 1)
                })

            df_results = pd.DataFrame(results).sort_values("total_score", ascending=False).head(200)
            st.session_state.session_data['results'] = df_results.to_dict('records')
            st.session_state.session_data['home_city'] = home_city
            st.success(f"Found {len(df_results)} collaboration opportunities")

if 'results' in st.session_state.session_data and len(st.session_state.session_data['results']) > 0:
    df_res = pd.DataFrame(st.session_state.session_data['results'])

    tab1, tab2, tab3, tab4 = st.tabs(["3D Globe Map", "Table", "Network Graph", "Export"])

    with tab1:
        fig = go.Figure(go.Scattergeo(
            lon=df_res['city'].map(lambda x: df_cities[df_cities['label'] == x]['lon'].values[0]),
            lat=df_res['city'].map(lambda x: df_cities[df_cities['label'] == x]['lat'].values[0]),
            text=df_res.apply(lambda r: f"{r['city']}<br>Score: {r['total_score']}<br>Overlap: {r['overlap_pct']}%", axis=1),
            mode='markers',
            marker=dict(
                size=df_res['total_score'] * 4,
                color=df_res['total_score'],
                colorscale='Turbo',
                line=dict(width=1, color='DarkSlateGrey'),
                showscale=True,
                colorbar=dict(title="Total Score"),
                opacity=0.85,
                symbol='circle'
            )
        ))
        fig.update_geos(
            projection_type="orthographic",
            showcoastlines=True, coastlinecolor="RebeccaPurple",
            showland=True, landcolor="LavenderBlush",
            showocean=True, oceancolor="LightSkyBlue",
            showcountries=True, countrycolor="MediumPurple",
            lataxis_showgrid=True, lonaxis_showgrid=True,
        )
        fig.update_layout(
            height=700,
            margin={"r":0, "t":0, "l":0, "b":0},
            paper_bgcolor="MintCream",
            geo=dict(
                bgcolor='MintCream',
                lakecolor='LightBlue'
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(df_res[['city', 'distance_km', 'overlap_pct', 'total_score']].style.set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#7C3AED'), ('color', 'white'), ('font-weight', 'bold')]},
            {'selector': 'tbody tr:hover', 'props': [('background-color', '#ede9fe')]}
        ]), use_container_width=True)

    with tab3:
        G_vis = nx.Graph()
        home = st.session_state.session_data.get('home_city', None) or list(df_cities['label'])[0]
        G_vis.add_node(home, type='home')
        for _, row in df_res.head(50).iterrows():
            G_vis.add_node(row['city'], type='target')
            G_vis.add_edge(home, row['city'], weight=row['total_score'])

        pos = nx.spring_layout(G_vis, k=0.8, iterations=50, seed=42)

        edge_x = []
        edge_y = []
        for edge in G_vis.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        node_x = []
        node_y = []
        node_text = []
        node_color = []
        for node in G_vis.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            if G_vis.nodes[node].get('type') == 'home':
                node_color.append('deepskyblue')
            else:
                deg = G_vis.degree(node)
                node_color.append(f"rgb({255 - deg*10}, {100 + deg*5}, 0)")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=edge_x, y=edge_y,
                                  mode='lines',
                                  line=dict(width=0.6, color='gray'),
                                  hoverinfo='none'))
        fig2.add_trace(go.Scatter(x=node_x, y=node_y,
                                  mode='markers+text',
                                  text=node_text,
                                  textposition="top center",
                                  marker=dict(size=15,
                                              color=node_color,
                                              line=dict(width=1, color='DarkSlateGrey'),
                                              symbol='circle',
                                              opacity=0.9),
                                  hoverinfo='text'))
        fig2.update_layout(
            showlegend=False,
            height=700,
            margin={"r":0, "t":0, "l":0, "b":0},
            paper_bgcolor='MintCream'
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab4:
        csv = df_res.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "nomad_results.csv", "text/csv")
        st.info("PDF export available in full version")

elif st.session_state.role == "Remote Project Lead":
    st.header("Remote Project Lead Mode")
    st.write("Team skill profiles and city comparison coming soon in full implementation")

elif st.session_state.role == "Community Organizer":
    st.header("Community Organizer Mode")
    st.write("Regional aggregation and outreach planning coming soon in full implementation")

st.markdown("---")
st.header("Session Management")

col_save, col_load = st.columns(2)

with col_save:
    if st.button("Save Session Data"):
        save_data = {
            "role": st.session_state.role,
            "data": {k: v for k, v in st.session_state.session_data.items() if k != 'graph'},
            "timestamp": datetime.now().isoformat()
        }
        json_str = json.dumps(save_data, indent=2)
        st.download_button(
            label="Download Session JSON",
            data=json_str,
            file_name=f"nomad_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col_load:
    uploaded = st.file_uploader("Load Session JSON", type="json")
    if uploaded:
        try:
            loaded = json.load(uploaded)
            st.session_state.role = loaded.get("role", None)
            st.session_state.session_data = loaded.get("data", {})
            st.success("Session loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load session: {e}")
