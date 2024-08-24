# Map Matching with HMM

This project provides a web interface for uploading vehicle trajectory data, processing it with a Hidden Markov Model (HMM), and displaying the results on an interactive map.

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- git

## Setup and Running

Follow these steps to set up and run the project:

1. **Clone the Repository:**

    ```bash
    https://github.com/shivas1516/map-matching.git
    cd map-matching-hmm
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment:**

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask Application:**

    ```bash
    python app.py
    ```

6. **Open the Web Application:**

    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Prepare Your CSV Data File:**

    Ensure your CSV file contains at least `lat` (latitude) and `lon` (longitude) columns, along with optional additional columns like `timestamp`.

2. **Upload and Process Data:**

    - On the web interface, click on the "Choose File" button and select your CSV file.
    - Click the "Run Map Matching" button to upload the file and process the data.
    - The processed map will display both the original and matched points.

## Example

Here's an example of how your CSV file might look:

```csv
latitude, longitude,timestamp
40.7128,-74.0060,2023-08-24 10:00:00
40.7129,-74.0061,2023-08-24 10:00:10
40.7130,-74.0062,2023-08-24 10:00:20
40.7131,-74.0063,2023-08-24 10:00:30

Save this as trajectory_data.csv and upload it through the web interface to see the results.
