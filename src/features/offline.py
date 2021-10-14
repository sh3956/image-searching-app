from pathlib import Path

import numpy as np
from PIL import Image

from feature_extractor import FeatureExtractor

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    fe = FeatureExtractor()

    for img_path in sorted(Path("./static/img").glob("*.jpg")):
        feature = fe.extract(img=Image.open(img_path))
        feature_path = Path("./static/feature") / (img_path.stem + ".npy") 
        np.save(feature_path, feature)