from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image
from flask import Flask, request, render_template

from feature_extractor import FeatureExtractor


app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


@app.route('/', methods=['GET', 'POST'])
def index():
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


if __name__=="__main__":
    app.run(port=5050, debug=True)