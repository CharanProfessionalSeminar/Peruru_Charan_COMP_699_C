# Nomad Network Navigator

## Project Overview
The Nomad Network Navigator is a desktop-based application designed to empower freelancers, remote project leads, and community organizers by simulating global collaboration opportunities based on skills and geographic proximity. The system operates fully offline, ensuring accessibility and privacy, and leverages Python libraries for data processing, visualization, and user interaction.

## Features
- **Role-Based Functionality**: Supports three user roles (Freelancer, Remote Project Lead, Community Organizer) with tailored simulation capabilities.
- **Skill and Location Input**: Users can input skills, expertise levels, and home city to generate personalized collaboration matches.
- **Network Simulation**: Utilizes graph-based algorithms to simulate connections across 200+ global cities, with filtering by skill overlap and geographic radius.
- **Interactive Visualizations**: Provides dynamic (Plotly) and static (Matplotlib) network graphs and heatmaps for exploring opportunities.
- **Offline Operation**: Runs entirely offline using local datasets (geonamescache) and stores session data locally.
- **Export Capabilities**: Generates CSV and PDF reports for collaboration matches, cluster summaries, and outreach planning.
- **What-If Simulations**: Allows real-time tweaks to inputs for exploring alternative scenarios.
- **Performance**: Optimized for consumer-grade hardware, ensuring sub-second responses for simulations and visualizations.

## Requirements
- **Python Version**: 3.8 or higher
- **Dependencies**:
  - streamlit: For interactive front-end
  - networkx: For graph-based algorithms
  - pandas: For data handling
  - numpy: For mathematical computations
  - plotly: For dynamic visualizations
  - matplotlib: For static visualizations
  - geonamescache: For offline city data
- **Operating Systems**: Windows, macOS, Linux
- **Hardware**: Consumer-grade hardware (no specific requirements beyond standard desktop capabilities)

**Navigate to the project directory:**
cd nomad-network-navigator

**Install dependencies:**
pip install -r requirements.txt

**Run the application:**
streamlit run app.py

**Usage**

Launch the application using the command above.
Select a role (Freelancer, Remote Project Lead, or Community Organizer) to start a session.
Input skills, expertise levels, and home city using the provided interface.
Run simulations to generate collaboration matches and visualize results as graphs or heatmaps.
Apply filters (e.g., radius, skill overlap) to refine results.
Export results as CSV or PDF for offline use.
Save or load sessions to preserve or resume work.

**Project Structure**

app.py: Main application file for Streamlit interface
src/: Source code for simulation engine, visualization, and data handling
data/: Offline datasets (e.g., geonamescache city data)
reports/: Exported CSV and PDF files
tests/: Unit tests for core components


**Contact**
For questions or feedback, contact Venkata Sai Charan Peruru at vperuru@rivier.edu
