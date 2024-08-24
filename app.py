from flask import Flask, render_template, request, redirect, url_for
import folium
import pandas as pd
import osrm
from hmmlearn import hmm
import numpy as np

app = Flask(__name__)

# Initialize OSRM client
osrm_client = osrm.Client(host='http://router.project-osrm.org')

def hmm_algorithm(data):
    X = np.array([[d['lat'], d['lon']] for d in data])
    model = hmm.GaussianHMM(n_components=5, covariance_type="full")
    model.fit(X)
    hidden_states = model.predict(X)
    for i, d in enumerate(data):
        d['hidden_state'] = int(hidden_states[i])
    return data

def map_matching(data):
    coordinates = [[d['lon'], d['lat']] for d in data]
    response = osrm_client.match(coordinates=coordinates)
    matched_points = []
    for tracepoint in response['tracepoints']:
        if tracepoint is not None:
            matched_points.append({
                'lat': tracepoint['location'][1],
                'lon': tracepoint['location'][0]
            })
    return matched_points

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
        df = pd.read_csv(file)
        data = df.to_dict('records')
        
        # Apply HMM algorithm
        hmm_result = hmm_algorithm(data)
        
        # Apply map matching
        matched_result = map_matching(hmm_result)
        
        # Create map
        m = folium.Map(location=[matched_result[0]['lat'], matched_result[0]['lon']], zoom_start=13)
        
        # Add original points
        for point in data:
            folium.Marker(
                [point['lat'], point['lon']],
                popup=f"Original: {point['lat']}, {point['lon']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        
        # Add matched points and connect them
        matched_coords = [(point['lat'], point['lon']) for point in matched_result]
        folium.PolyLine(matched_coords, color="red", weight=2.5, opacity=1).add_to(m)
        
        for point in matched_result:
            folium.Marker(
                [point['lat'], point['lon']],
                popup=f"Matched: {point['lat']}, {point['lon']}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Save the map
        m.save('static/map.html')
        
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)