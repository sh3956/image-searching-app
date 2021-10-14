import os
import glob
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image
from flask import Blueprint, request, render_template, flash
from flask_login import login_required, current_user

from __init__ import create_app, db
from feature_extractor import FeatureExtractor


main = Blueprint('main', __name__)
folder_path = Path("./static") / ("uploaded")

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  
        ids = np.argsort(dists)[:5]  # Top 5 results
        scores = [(dists[id], img_paths[id]) for id in ids]

        return render_template('home.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('home.html')

@main.route('/database')
def database():
    images = glob.glob(os.path.join(folder_path, '*'))
    return render_template('database.html', database_images=images)


app = create_app() 

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(port=5050, debug=True) 