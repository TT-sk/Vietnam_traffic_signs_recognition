import glob
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, url_for
from pathlib import Path
import json
import os
import subprocess
import sys
from datetime import datetime
import shutil

app = Flask(__name__)
os.makedirs('static/detected', exist_ok=True)  # Create the directory if it doesn't exist
os.makedirs('static/uploaded', exist_ok=True)  # Ensure the uploaded directory exists

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_img_path = None
    if request.method == 'POST':
        file = request.files['query_img']
        img = Image.open(file.stream)

        crop_data = json.loads(request.form.get('crop_data', "{}"))  # Get crop_data, return empty dict if not present
        print(crop_data)
        if crop_data:
            left = int(crop_data['x'])
            top = int(crop_data['y'])
            width = int(crop_data['width'])
            height = int(crop_data['height'])
            right = left + width
            bottom = top + height
            img = img.crop((left, top, right, bottom))  

        # Save the image temporarily
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run the Python script
        subprocess.run([sys.executable, "C:/Users/thien/DO_AN/demo/static/yolov5/detect.py", "--weights", "C:/Users/thien/DO_AN/demo/static/yolov5/best.pt", "--source", "C:/Users/thien/DO_AN/demo/static/uploaded"])
        
        # Get the latest detected image
        latest_detected_dir = get_latest_detected_dir(os.path.join('static', 'yolov5', 'runs', 'detect'))
        detected_img_path = get_latest_detected_image(latest_detected_dir)

        # Copy the detected image to the static/detected directory
        if detected_img_path:
            detected_img_name = os.path.basename(detected_img_path)
            new_detected_img_path = os.path.join('static', 'detected', detected_img_name)
            shutil.copy(detected_img_path, new_detected_img_path)
            detected_img_path = new_detected_img_path

        return render_template(
            'index.html', 
            cropped_img_path=url_for('static', filename='uploaded/' + os.path.basename(uploaded_img_path)),
            detected_img_path=url_for('static', filename='detected/' + os.path.basename(detected_img_path)) if detected_img_path else None,
        )
    
    # For GET request, render the index page without image paths
    return render_template('index.html')

def get_latest_detected_dir(detected_base_dir):
    """
    Retrieves the latest detected directory from the specified base directory.
    """
    detected_dirs = sorted(glob.glob(os.path.join(detected_base_dir, 'exp*')), key=os.path.getmtime, reverse=True)
    if detected_dirs:
        latest_detected_dir = detected_dirs[0]
        return latest_detected_dir
    return None

def get_latest_detected_image(detected_dir):
    """
    Retrieves the latest detected image from the specified directory.
    """
    detected_images = sorted(glob.glob(os.path.join(detected_dir, '*.jpg')), key=os.path.getmtime, reverse=True)
    if detected_images:
        latest_detected_image = detected_images[0]
        return latest_detected_image
    return None

if __name__ == "__main__":
    app.run("0.0.0.0")
