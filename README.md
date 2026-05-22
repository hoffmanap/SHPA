
# Sunset Heights Parking Prevalence Dashboard (SHPA)
  
An interactive urban planning dashboard analyzing the prevalence and commonness of off-street parking configurations within the historic **Sunset Heights Neighborhood** in El Paso, Texas.

🚀 **[👉 Click Here to Open the Interactive Dashboard](https://hoffmanap.github.io/SHPA/dashboard/)**

---

## 📊 Project Overview

This tool maps, filters, and visualizes urban parcel metrics to evaluate how off-street parking capacity intersects with architectural eras, residential unit density, and underlying zoning regulations. Understanding these patterns is key to assessing local development feasibility and auditing municipal zoning constraints (such as parking minimums).

The dynamic client-side application integrates a spatial geospatial interface with responsive charting elements, providing a unified platform to splice architectural and parking data metrics.

---

## 🛠️ Key Dashboard Features

* **Interactive Spatial Layer (Leaflet.js):** Custom polygon-rendered map mapping historic Sunset Heights parcels. Features are explicitly color-coded via conditional logic:
    * 🟢 **Emerald Green:** Properties with verified Off-Street Parking (`OffStreet: Y`).
    * 🔴 **Rose Red:** Properties missing dedicated Off-Street Parking (`OffStreet: N`).
* **Dynamic Yield KPI Card:** An analytical engine tracks and updates a major metric card revealing the exact **percentage of selected properties that have off-street parking**, allowing instant context when changing criteria.
* **Clustered Multi-Series Bar Charts (Chart.js):** Three baseline charts calculate the percentage breakdown of parking availability (`Y` vs `N`) across:
    1.  **Zoning District** configurations (e.g., `R-4-H`, `A-3-H`).
    2.  **Decade Built** structural timelines.
    3.  **Building Use Descriptions** (LBCS Structure Classifications).
* **Advanced Multi-Attribute Sidepanel Filters:** Granular client-side data cascading logic across:
    * *Property Address* (Instant text lookup string matching).
    * *Unit Count / Residential Scale* (Segmented into Single Unit `1`, Missing/Middle Multi-family `2-4`, or High-Density Multi-family `5+` options).
    * *Parking Configuration Type* (Surface lot, detached/attached garage, hybrid).
    * *Curb Cut Presence* (`Y`/`N` options indicating structural right-of-way infrastructure).

---

## 🗂️ Data Dictionary & Filter Attributes

The underlying spatial layer parses the following specific schema metrics extracted directly from neighborhood structural surveys:

1.  `address`: The physical siting address of the property parcel.
2.  `ll_address_count`: The total unit load/density on site (crucial for evaluating multifamily trends).
3.  `lbcs_structure_desc`: The Land Based Classification Standards (LBCS) structural descriptions for building use.
4.  `zoning`: The base City of El Paso zoning district classification (with `-H` historical designations).
5.  `yearbuilt`: The baseline structural year of construction.
6.  `OffStreet`: Binary marker (`Y`/`N`) confirming off-street asset presence.
7.  `Type`: Explanatory configuration type (`Surface`, `Garage`, `Garage/Surface`, etc.).
8.  `CurbCut`: Operational flag (`Y`/`N`) assessing physical access connectivity.

---

## 💻 Tech Stack & Performance

* **Frontend Interface:** Pure HTML5, Tailwind CSS framework.
* **Mapping API:** Leaflet.js (utilizing desaturated CartoDB Light vector tile layers for emphasis on property features).
* **Data Aggregation Engine:** Chart.js for canvas-rendered relational data matrices.
* **Data Footprint:** Optimized and minified GeoJSON geometry records baked directly into the document container to bypass asynchronous CORS request blockers, ensuring ultra-fast load times when hosted as static pages.

---
