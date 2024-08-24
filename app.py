from flask import Flask, render_template, request, redirect, url_for
import folium
import pandas as pd
import numpy as np
from pytrack.graph import graph, distance
from pytrack.analytics import visualization
from pytrack.matching import candidate, mpmatching_utils, mpmatching

app = Flask(__name__)

def load_and_process_data(file):
    df = pd.read_csv(file)
    latitude = df["latitude"].to_list()
    longitude = df["longitude"].to_list()
    points = [(lat, lon) for lat, lon in zip(latitude, longitude)]
    return points

def perform_map_matching(points):
    # Create BBOX
    north, east = np.max(np.array([*points]), 0)
    south, west = np.min(np.array([*points]), 0)
    
    # Extract road graph
    G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south, west, east, 500), simplify=True, network_type='drive')
    
    # Extract candidates
    G_interp, candidates = candidate.get_candidates(G, points, interp_dist=5, closest=True, radius=30)
    
    # Extract trellis DAG graph
    trellis = mpmatching_utils.create_trellis(candidates)
    
    # Perform the map-matching process
    path_prob, predecessor = mpmatching.viterbi_search(G_interp, trellis, "start", "target")
    
    # Extract matched points
    matched_coords = []
    for state in path_prob:
        matched_coords.append(G.nodes[state]['y'], G.nodes[state]['x'])
    
    return G, matched_coords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and file.filename.endswith('.csv'):
        points = load_and_process_data(file)
        
        # Perform map matching using pytrack
        G, matched_result = perform_map_matching(points)
        
        # Create map
        m = folium.Map(location=[matched_result[0][0], matched_result[0][1]], zoom_start=13)
        
        # Add original points
        for point in points:
            folium.Marker(
                [point[0], point[1]],
                popup=f"Original: {point[0]}, {point[1]}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        
        # Add matched points and connect them
        folium.PolyLine(matched_result, color="red", weight=2.5, opacity=1).add_to(m)
        
        for point in matched_result:
            folium.Marker(
                [point[0], point[1]],
                popup=f"Matched: {point[0]}, {point[1]}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Save the map
        m.save('static/map.html')
        
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
