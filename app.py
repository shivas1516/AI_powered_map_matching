from flask import Flask, render_template, request, redirect, url_for
import folium
import pandas as pd
from hmmlearn import hmm
import numpy as np
import io

app = Flask(__name__)

# HMM Model initialization (this is a placeholder and should be customized based on your requirements)
class MapMatchingHMM:
    def __init__(self):
        self.model = hmm.GaussianHMM(n_components=3, covariance_type="diag")
    
    def train(self, data):
        # Training the HMM with vehicle trajectory data
        self.model.fit(data)
    
    def predict(self, data):
        # Predict the most likely sequence of states (map matching)
        return self.model.predict(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    # Read CSV file into DataFrame
    if file:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        data = pd.read_csv(stream)
        data_points = data[['latitude', 'longitude']].values
        
        # Map Matching with HMM (Dummy Model)
        map_matcher = MapMatchingHMM()
        map_matcher.train(data_points)
        predicted_route = map_matcher.predict(data_points)
        
        # Create Map
        map_ = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)
        
        # Mark Points and Route
        for i, (lat, lon) in enumerate(data_points):
            folium.Marker([lat, lon], popup=f"Point {i}, State {predicted_route[i]}").add_to(map_)
        
        # Save map to HTML file
        map_.save('templates/map.html')
        
        return redirect(url_for('display_map'))
    return redirect(url_for('index'))

@app.route('/map')
def display_map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
