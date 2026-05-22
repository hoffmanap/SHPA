# Save this in your main folder as compile.py
import json
import os

geojson_source = 'sunsetparking.GEOjson'
output_directory = 'dashboard'
output_filepath = os.path.join(output_directory, 'index.html')

if not os.path.exists(geojson_source):
    raise FileNotFoundError(f"Missing '{geojson_source}'! Place it in this exact folder.")

# Create the dashboard directory if it doesn't exist yet
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

print("🔄 Processing and optimizing Sunset Heights parcel geometries...")

with open(geojson_source, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Keep the payload highly optimized for rapid loading on web browsers
clean_features = []
for feature in raw_data.get('features', []):
    if feature.get('geometry') and feature['geometry'].get('coordinates'):
        props = feature.get('properties', {})
        clean_props = {
            'address': props.get('address'),
            'll_address_count': props.get('ll_address_count'),
            'lbcs_structure_desc': props.get('lbcs_structure_desc'),
            'zoning': props.get('zoning'),
            'yearbuilt': props.get('yearbuilt'),
            'OffStreet': props.get('OffStreet'),
            'Type': props.get('Type'),
            'CurbCut': props.get('CurbCut'),
            'highest_parcel_elevation': props.get('highest_parcel_elevation'),
            'lowest_parcel_elevation': props.get('lowest_parcel_elevation'),
            'll_gissqft': props.get('ll_gissqft')
        }
        clean_features.append({
            'type': feature.get('type', 'Feature'),
            'geometry': feature['geometry'],
            'properties': clean_props
        })

optimized_geojson = {'type': 'FeatureCollection', 'features': clean_features}

# Complete dashboard application layout skeleton
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sunset Heights Topographic & Parking Feasibility Hub</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        #map { height: calc(100vh - 140px); min-height: 400px; }
        .chart-container { position: relative; height: 210px; width: 100%; }
        .dual-slider-container { position: relative; height: 20px; margin-top: 10px; }
        .dual-slider-container input[type="range"] {
            position: absolute; width: 100%; pointer-events: none; -webkit-appearance: none; z-index: 2; height: 5px; background: none; opacity: 0;
        }
        .dual-slider-container input[type="range"]::-webkit-slider-thumb {
            pointer-events: auto; width: 15px; height: 15px; border-radius: 50%; background: #4f46e5; cursor: pointer; -webkit-appearance: none; box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        .dual-slider-container input[type="range"]::-moz-range-thumb {
            pointer-events: auto; width: 15px; height: 15px; border-radius: 50%; background: #4f46e5; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        .slider-custom-track { position: absolute; width: 100%; height: 5px; background: #e2e8f0; border-radius: 3px; top: 6px; z-index: 1; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 flex flex-col h-screen overflow-hidden">
    <header class="bg-slate-900 text-white px-6 py-4 shadow-md flex justify-between items-center z-10">
        <div>
            <h1 class="text-xl font-bold tracking-tight">Sunset Heights Topographic & Parking Feasibility Hub</h1>
            <p class="text-xs text-slate-400">Evaluating Urban Grading Challenges, Lot Forms & Access Patterns • El Paso, Texas</p>
        </div>
        <div><span class="text-xs bg-indigo-950 px-3 py-1.5 rounded-full font-medium text-indigo-300" id="metric-summary">Processing Parcels...</span></div>
    </header>

    <div class="flex flex-1 overflow-hidden relative">
        <aside class="w-96 bg-white shadow-xl flex flex-col z-10 border-r border-slate-200 overflow-y-auto p-5 space-y-5">
            <div class="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-xl p-4 shadow-md">
                <h2 class="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-1.5">Off-Street Capacity Rate</h2>
                <div class="flex items-baseline space-x-2">
                    <span class="text-4xl font-extrabold text-white" id="parking-pct">0%</span>
                    <span class="text-xs font-medium text-slate-400">Selection Yield</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-2 mt-3 overflow-hidden">
                    <div id="parking-progress" class="bg-emerald-500 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-[11px] text-slate-400 mt-2 font-medium" id="raw-counts">Processing...</p>
            </div>

            <div class="space-y-4 border-b border-slate-100 pb-5">
                <div class="flex justify-between items-center">
                    <h2 class="text-xs font-bold tracking-tight text-slate-900 uppercase">Variable Modifiers</h2>
                    <button onclick="resetFilters()" class="text-xs text-indigo-600 hover:text-indigo-800 font-bold">Reset All</button>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Terrain Slope Constraints</label>
                    <select id="filter-slope" onchange="filterData()" class="w-full text-xs px-2.5 py-2 border border-slate-300 rounded-md bg-white">
                        <option value="">All Slopes</option>
                        <option value="Escarpment">Severe Escarpment (&gt;30ft Delta)</option>
                        <option value="Incline">Moderate Incline (10ft - 30ft Delta)</option>
                        <option value="Plateau">Flat Terrain (&lt;10ft Delta)</option>
                    </select>
                </div>
                <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                    <div class="flex justify-between text-xs font-semibold text-slate-600">
                        <span>Era of Construction:</span><span class="text-indigo-600 font-bold" id="year-range-display">1900 - 2022</span>
                    </div>
                    <div class="dual-slider-container">
                        <div class="slider-custom-track" id="year-track"></div>
                        <input type="range" id="slider-min-year" min="1900" max="2022" value="1900" oninput="controlYearMin()">
                        <input type="range" id="slider-max-year" min="1900" max="2022" value="2022" oninput="controlYearMax()">
                    </div>
                </div>
                <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                    <div class="flex justify-between text-xs font-semibold text-slate-600">
                        <span>Parcel Size Envelope:</span><span class="text-indigo-600 font-bold" id="lot-range-display">500 - 15,000+ sqft</span>
                    </div>
                    <div class="dual-slider-container">
                        <div class="slider-custom-track" id="lot-track"></div>
                        <input type="range" id="slider-min-lot" min="500" max="15000" step="250" value="500" oninput="controlLotMin()">
                        <input type="range" id="slider-max-lot" min="500" max="15000" step="250" value="15000" oninput="controlLotMax()">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Property Address Match</label>
                    <input type="text" id="filter-address" oninput="filterData()" placeholder="Search address..." class="w-full text-xs px-3 py-2 border border-slate-300 rounded-md">
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Curb Cut</label>
                        <select id="filter-curbcut" onchange="filterData()" class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-md bg-white">
                            <option value="">All</option><option value="Y">Yes</option><option value="N">No</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Zoning Code</label>
                        <select id="filter-zoning" onchange="filterData()" class="w-full text-xs px-2 py-1.5 border border-slate-300 rounded-md bg-white">
                            <option value="">All</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="pt-2 flex-1 flex flex-col min-h-[180px]">
                <h3 class="text-xs font-bold text-slate-900 uppercase mb-2 flex items-center"><span class="inline-block w-2 h-2 rounded-full bg-indigo-600 mr-2"></span>Key Policy Insights</h3>
                <div class="space-y-3 text-[11px] text-slate-600 leading-relaxed overflow-y-auto pr-1">
                    <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100"><strong>The Ridge Preclusion Effect:</strong> Elevation challenges physically barred grading corridors or cost-effective garage configurations natively on hillsides.</div>
                    <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100"><strong>The 5,000 SqFt Gatekeeper:</strong> Total lot area acts as a width proxy. Sub-standard configurations below 3,500 sqft show only a 18.9% off-street deployment rate.</div>
                    <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100"><strong>Missing-Middle Space Conflicts:</strong> Small multi-unit structures (4-8 units) on compact footprints experience a total parking capacity collapse (0% yield).</div>
                </div>
            </div>
        </aside>

        <main class="flex-1 flex flex-col overflow-hidden relative">
            <div id="map" class="w-full flex-1"></div>
            <div class="h-[260px] bg-white border-t border-slate-200 p-4 grid grid-cols-3 gap-4 shadow-inner">
                <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-200 flex flex-col justify-between">
                    <h3 class="text-xs font-bold text-slate-700 text-center uppercase mb-1">Parking Rate by Slope Profile</h3>
                    <div class="chart-container flex-1"><canvas id="chart-slope"></canvas></div>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-200 flex flex-col justify-between">
                    <h3 class="text-xs font-bold text-slate-700 text-center uppercase mb-1">Historical Adaptation Timeline</h3>
                    <div class="chart-container flex-1"><canvas id="chart-timeline"></canvas></div>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-200 flex flex-col justify-between">
                    <h3 class="text-xs font-bold text-slate-700 text-center uppercase mb-1">Site Parking Typologies Share</h3>
                    <div class="chart-container flex-1 flex justify-center items-center"><canvas id="chart-typology"></canvas></div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const geojsonData = __GEOJSON_INJECTION__;
        let map, geojsonLayer;
        let charts = {};
        const minYearGlobal = 1900, maxYearGlobal = 2022;
        const minLotGlobal = 500, maxLotGlobal = 15000;

        function processFeatures() {
            geojsonData.features.forEach(f => {
                const p = f.properties;
                const delta = (p.highest_parcel_elevation || 0) - (p.lowest_parcel_elevation || 0);
                if (delta > 30) p.computed_slope = 'Escarpment';
                else if (delta > 10) p.computed_slope = 'Incline';
                else p.computed_slope = 'Plateau';
            });
        }

        function controlYearMin() {
            const minS = document.getElementById('slider-min-year');
            const maxS = document.getElementById('slider-max-year');
            if (parseInt(minS.value) > parseInt(maxS.value) - 4) minS.value = parseInt(maxS.value) - 4;
            document.getElementById('year-range-display').textContent = `${minS.value} - ${maxS.value}`;
            updateTrack('year-track', minS.value, maxS.value, minYearGlobal, maxYearGlobal);
            filterData();
        }
        function controlYearMax() {
            const minS = document.getElementById('slider-min-year');
            const maxS = document.getElementById('slider-max-year');
            if (parseInt(maxS.value) < parseInt(minS.value) + 4) maxS.value = parseInt(minS.value) + 4;
            document.getElementById('year-range-display').textContent = `${minS.value} - ${maxS.value}`;
            updateTrack('year-track', minS.value, maxS.value, minYearGlobal, maxYearGlobal);
            filterData();
        }
        function controlLotMin() {
            const minS = document.getElementById('slider-min-lot');
            const maxS = document.getElementById('slider-max-lot');
            if (parseInt(minS.value) > parseInt(maxS.value) - 500) minS.value = parseInt(maxS.value) - 500;
            displayLotText(minS.value, maxS.value);
            updateTrack('lot-track', minS.value, maxS.value, minLotGlobal, maxLotGlobal);
            filterData();
        }
        function controlLotMax() {
            const minS = document.getElementById('slider-min-lot');
            const maxS = document.getElementById('slider-max-lot');
            if (parseInt(maxS.value) < parseInt(minS.value) + 500) maxS.value = parseInt(minS.value) + 500;
            displayLotText(minS.value, maxS.value);
            updateTrack('lot-track', minS.value, maxS.value, minLotGlobal, maxLotGlobal);
            filterData();
        }
        function displayLotText(min, max) {
            const maxText = parseInt(max) === maxLotGlobal ? '15,000+ sqft' : `${max} sqft`;
            document.getElementById('lot-range-display').textContent = `${min} - ${maxText}`;
        }
        function updateTrack(id, currentMin, currentMax, globalMin, globalMax) {
            const pctMin = ((currentMin - globalMin) / (globalMax - globalMin)) * 100;
            const pctMax = ((currentMax - globalMin) / (globalMax - globalMin)) * 100;
            document.getElementById(id).style.background = `linear-gradient(to right, #e2e8f0 ${pctMin}%, #4f46e5 ${pctMin}%, #4f46e5 ${pctMax}%, #e2e8f0 ${pctMax}%)`;
        }

        function initDashboard() {
            processFeatures();
            map = L.map('map', { center: [31.7645, -106.5010], zoom: 15 });
            const standardBase = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { attribution: 'CARTO' }).addTo(map);
            const topoBase = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/tile/{z}/{y}/{x}', { attribution: 'USGS', opacity: 0.75 });
            L.control.layers({ "Planimetric Base": standardBase, "USGS Topo Shaded Relief": topoBase }, null, { position: 'topright' }).addTo(map);

            const zonings = new Set();
            geojsonData.features.forEach(f => { if (f.properties.zoning) zonings.add(f.properties.zoning); });
            const selectZ = document.getElementById('filter-zoning');
            Array.from(zonings).sort().forEach(z => {
                const opt = document.createElement('option'); opt.value = z; opt.textContent = z; selectZ.appendChild(opt);
            });
            updateVisualization();
        }

        function filterData() { updateVisualization(); }

        function updateVisualization() {
            const slopeVal = document.getElementById('filter-slope').value;
            const addrVal = document.getElementById('filter-address').value.toLowerCase();
            const curbVal = document.getElementById('filter-curbcut').value;
            const zoneVal = document.getElementById('filter-zoning').value;
            const minYear = parseInt(document.getElementById('slider-min-year').value);
            const maxYear = parseInt(document.getElementById('slider-max-year').value);
            const minLot = parseInt(document.getElementById('slider-min-lot').value);
            const maxLot = parseInt(document.getElementById('slider-max-lot').value);

            const filteredFeatures = geojsonData.features.filter(f => {
                const p = f.properties;
                const lotSqft = p.ll_gissqft || 0;
                if (slopeVal && p.computed_slope !== slopeVal) return false;
                if (addrVal && (!p.address || !p.address.toLowerCase().includes(addrVal))) return false;
                if (curbVal && p.CurbCut !== curbVal) return false;
                if (zoneVal && p.zoning !== zoneVal) return false;
                if (p.yearbuilt && (p.yearbuilt < minYear || p.yearbuilt > maxYear)) return false;
                if (lotSqft < minLot) return false;
                if (maxLot !== maxLotGlobal && lotSqft > maxLot) return false;
                return true;
            });

            if (geojsonLayer) map.removeLayer(geojsonLayer);
            geojsonLayer = L.geoJSON({ type: "FeatureCollection", features: filteredFeatures }, {
                style: (f) => ({ fillColor: f.properties.OffStreet === 'Y' ? '#10b981' : '#ef4444', weight: 1.2, opacity: 0.85, color: '#ffffff', fillOpacity: 0.65 }),
                onEachFeature: (f, l) => {
                    const p = f.properties;
                    l.bindPopup(`<div class="font-sans text-xs p-1"><h4 class="font-bold border-b pb-1 mb-1">${p.address || 'Boundary'}</h4><b>Zoning:</b> ${p.zoning}<br/><b>Size:</b> ${p.ll_gissqft || 'N/A'} sqft<br/><b>Parking:</b> ${p.OffStreet === 'Y' ? 'Yes' : 'No'}</div>`);
                }
            }).addTo(map);

            const total = filteredFeatures.length;
            const yesCount = filteredFeatures.filter(f => f.properties.OffStreet === 'Y').length;
            const pct = total > 0 ? Math.round((yesCount / total) * 100) : 0;
            document.getElementById('parking-pct').textContent = pct + '%';
            document.getElementById('parking-progress').style.width = pct + '%';
            document.getElementById('raw-counts').textContent = `Isolating ${yesCount} lots out of ${total}`;
            document.getElementById('metric-summary').textContent = `Scope: ${total} Parcels | ${pct}% Parking`;
            renderCharts(filteredFeatures);
        }

        function renderCharts(features) {
            const slopeMap = { 'Escarpment': { total: 0, yes: 0 }, 'Incline': { total: 0, yes: 0 }, 'Plateau': { total: 0, yes: 0 } };
            features.forEach(f => {
                const s = f.properties.computed_slope;
                if(slopeMap[s]) { slopeMap[s].total++; if (f.properties.OffStreet === 'Y') slopeMap[s].yes++; }
            });
            const slopePcts = Object.keys(slopeMap).map(k => slopeMap[k].total > 0 ? Math.round((slopeMap[k].yes / slopeMap[k].total) * 100) : 0);
            drawChart('chart-slope', 'bar', { labels: ['Severe Escarpment', 'Moderate Incline', 'Flat Plateau'], datasets: [{ label: '% Off-Street Parking', data: slopePcts, backgroundColor: '#4f46e5', borderRadius: 4 }] }, { maxScale: 100 });

            const timelineMap = {};
            features.forEach(f => {
                if (!f.properties.yearbuilt) return;
                const dec = Math.floor(f.properties.yearbuilt / 10) * 10 + 's';
                if (!timelineMap[dec]) timelineMap[dec] = { total: 0, yes: 0 };
                timelineMap[dec].total++; if (f.properties.OffStreet === 'Y') timelineMap[dec].yes++;
            });
            const sortedDecades = Object.keys(timelineMap).sort();
            const timelinePcts = sortedDecades.map(d => Math.round((timelineMap[d].yes / timelineMap[d].total) * 100));
            drawChart('chart-timeline', 'line', { labels: sortedDecades, datasets: [{ label: 'Adaptation %', data: timelinePcts, borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.05)', fill: true, tension: 0.25 }] }, { maxScale: 100 });

            const typeMap = { 'Surface Lot': 0, 'Garage Asset': 0, 'No Dedicated Asset': 0 };
            features.forEach(f => {
                const t = f.properties.Type;
                if (t === 'Surface') typeMap['Surface Lot']++; else if (t === 'Garage') typeMap['Garage Asset']++; else typeMap['No Dedicated Asset']++;
            });
            drawChart('chart-typology', 'doughnut', { labels: Object.keys(typeMap), datasets: [{ data: Object.values(typeMap), backgroundColor: ['#6366f1', '#f59e0b', '#ef4444'], borderWidth: 1 }] }, { isDoughnut: true });
        }

        function drawChart(id, type, data, options = {}) {
            if (charts[id]) { charts[id].data = data; charts[id].update(); return; }
            const ctx = document.getElementById(id).getContext('2d');
            charts[id] = new Chart(ctx, {
                type: type, data: data,
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: !options.isDoughnut, position: 'top', labels: { boxWidth: 10, font: { size: 9 } } } },
                    scales: options.isDoughnut ? {} : {
                        y: { min: 0, max: options.maxScale, ticks: { font: { size: 9 }, callback: v => v + '%' }, grid: { color: '#f1f5f9' } },
                        x: { grid: { display: false }, ticks: { font: { size: 9 } } }
                    }
                }
            });
        }

        function resetFilters() {
            document.getElementById('filter-slope').value = ''; document.getElementById('filter-address').value = '';
            document.getElementById('filter-curbcut').value = ''; document.getElementById('filter-zoning').value = '';
            document.getElementById('slider-min-year').value = minYearGlobal; document.getElementById('slider-max-year').value = maxYearGlobal;
            document.getElementById('slider-min-lot').value = minLotGlobal; document.getElementById('slider-max-lot').value = maxLotGlobal;
            document.getElementById('year-range-display').textContent = '1900 - 2022'; displayLotText(minLotGlobal, maxLotGlobal);
            updateTrack('year-track', minYearGlobal, maxYearGlobal, minYearGlobal, maxYearGlobal); updateTrack('lot-track', minLotGlobal, maxLotGlobal, minLotGlobal, maxLotGlobal);
            updateVisualization();
        }
        window.onload = initDashboard;
    </script>
</body>
</html>
"""

final_output = html_template.replace('__GEOJSON_INJECTION__', json.dumps(optimized_geojson))

with open(output_filepath, 'w', encoding='utf-8') as out_f:
    out_f.write(final_output)

print(f"🎉 SUCCESS! Integrated dashboard built at: {output_filepath}")
