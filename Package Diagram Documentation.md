# Package Diagram Documentation

## Overview
This document describes the package structure of the Nomad Network Navigator system, detailing the organization of its core components. The package diagram illustrates the modular architecture, grouping related classes into packages to promote maintainability, scalability, and clarity. Each package encapsulates specific functionality, aligning with the system's functional and non-functional requirements, such as offline operation, role-based simulations, and data visualization.

## Package Diagram Description
The Nomad Network Navigator system is organized into several packages, each responsible for a distinct aspect of the application. The packages are designed to ensure separation of concerns, modularity, and ease of maintenance. The diagram below, created using PlantUML, represents the relationships and dependencies between these packages.

### Packages
1. **User Management**
   - Contains classes related to user roles and session management.
   - Classes: `User`, `Freelancer`, `RemoteProjectLead`, `CommunityOrganizer`, `Session`
   - Responsibilities: Managing user roles, session creation, saving, loading, and resetting sessions.

2. **Data Input**
   - Handles input and validation of user data such as skills and cities.
   - Classes: `Skill`, `City`, `SkillProfile`
   - Responsibilities: Capturing and validating skills, expertise levels, and city selections.

3. **Simulation Engine**
   - Manages the core simulation logic for generating collaboration matches.
   - Classes: `Simulation`, `Match`, `Filter`, `Cluster`
   - Responsibilities: Running simulations, applying filters, calculating match scores, and identifying collaboration clusters.

4. **Visualization**
   - Responsible for generating and displaying interactive and static visualizations.
   - Classes: `Visualization`, `Heatmap`
   - Responsibilities: Creating network graphs, heatmaps, and supporting zoom, pan, and highlight functionalities.

5. **Reporting**
   - Handles export functionalities for simulation results and outreach plans.
   - Classes: `Report`
   - Responsibilities: Generating CSV and PDF reports for offline use.

6. **Geographic Data**
   - Manages offline geographic data for simulations.
   - Classes: `Region`, `City` (shared with Data Input)
   - Responsibilities: Aggregating regional data and summarizing skill hubs.

### Dependencies
- **User Management** depends on **Data Input** for role-specific inputs (e.g., skills, cities).
- **Simulation Engine** depends on **Data Input** for skills and city data, and on **Geographic Data** for region-based simulations.
- **Visualization** depends on **Simulation Engine** for match and cluster data to render graphs and heatmaps.
- **Reporting** depends on **Simulation Engine** and **Visualization** for exporting simulation results and graph snapshots.
- **Geographic Data** depends on **Data Input** for city data used in regional analysis.

