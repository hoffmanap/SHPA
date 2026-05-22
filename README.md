# Sunset Heights Parking Prevalence & Feasibility Hub (SHPA)
  
An interactive urban planning dashboard analyzing the relationship between off-street parking configurations, natural topography, and parcel size constraints within the historic **Sunset Heights Neighborhood** in El Paso, Texas.

🚀 **[View the Live Interactive Dashboard Here](https://hoffmanap.github.io/SHPA/)**

---

## 📊 Project Overview

This tool maps, filters, and visualizes urban parcel metrics to evaluate how physical terrain constraints and historic platted dimensions intersect with municipal zoning requirements (such as parking minimums). Understanding these spatial relationships is key to auditing local development bottlenecks, streamlining permitting, and informing zoning text amendments for housing affordability.

---

## 💡 Key Policy Insights

* **The Ridge Preclusion Effect:** Geospatial analysis isolates a direct correlation between natural slope challenges and parking deficits. On the steep western escarpment and hillside blocks (characterized by elevation deltas exceeding 30 feet per parcel), off-street parking rates drop dramatically. Grading driveways or constructing garages into natural limestone cliffs was physically and structurally unfeasible during the neighborhood's core historic development window (1900–1930), illustrating why flat, uniform municipal parking mandates fail to fit historic hill terrains.
* **The 5,000 Sq. Ft. Width Gatekeeper:** Total parcel square footage behaves as a direct proxy for historic platted lot widths. The data exposes a severe regulatory breakpoint at the **5,000 sqft threshold** (the standard historic 40–50 ft wide lot configuration). Properties on narrow or sub-standard historic fractions under 3,500 sqft yield an off-street parking rate of just **18.9%** because side-yard clearances are physically too narrow to route a vehicle past a building facade without destroying the structure's historic footprint.
* **The Missing-Middle Space Conflict:** While duplexes and triplexes successfully leverage parallel alleyway networks on flatter plateaus to match single-family parking rates, small-scale multi-family configurations (4–8 units) mapped onto sub-5,000 sqft lots experience an absolute parking asset collapse (**0% off-street capture**). On limited parcel footprints, building massing and setback rules fully consume the lot. Enforcing standard parking minimums on these traditional layouts acts as an outright prohibition against low-impact, missing-middle housing infill.

---

## 🛠️ Key Dashboard Features

* **Interactive Spatial Layer (Leaflet.js):** Custom polygon-rendered map of historic Sunset Heights parcels, conditionally color-coded:
    * 🟢 **Emerald Green:** Properties with verified Off-Street Parking (`OffStreet: Y`).
    * 🔴 **Rose Red:** Properties lacking dedicated Off-Street Parking (`OffStreet: N`).
* **Topographic Base Mapping:** Includes an on-canvas layer toggle to switch from a planimetric view to high-contrast **USGS Shaded Relief Topography**, instantly aligning the "rose red" parking deficits with the dense contour lines of the hillsides.
* **Dynamic Variable Modifiers (Dual Sliders):** Real-time client-side cascading data logic allowing you to slice the entire neighborhood by:
    * *Terrain Slope Constraints* (Programmatic categories: Severe Escarpment, Moderate Incline, Flat Plateau).
    * *Era of Construction* (Dual-handle slider from 1900 to 2022).
    * *Parcel Size Envelope* (Dual-handle slider from 500 to 15,000+ sqft).
* **Single-Metric Visualizations (Chart.js):** Replaced duplicate multi-series charts with high-impact visuals: a horizontal bar layout for zoning performance comparison, a smooth timeline trend line showing the mid-century surge in parking mandates, and a land-use typology share doughnut chart.

---

## 🗂️ Data Dictionary & Attributes

1.  `address`: The physical sitings address of the parcel.
2.  `ll_address_count`: Total unit density count on-site (residential scale evaluation).
3.  `lbcs_structure_desc`: Land Based Classification Standards (LBCS) structural building use descriptions.
4.  `zoning`: Base El Paso zoning classification code (including `-H` historic designators).
5.  `yearbuilt`: Core structural construction year.
6.  `OffStreet`: Binary marker (`Y`/`N`) confirming off-street parking asset presence.
7.  `Type`: Explanatory asset typology (`Surface`, `Garage`, `Hybrid/Other`).
8.  `CurbCut`: Operational indicator flag (`Y`/`N`) tracking right-of-way cuts.
