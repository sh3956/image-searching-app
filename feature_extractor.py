import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

class FeatureExtractor:
    """
    Load image model from tensorflow and extract feature from an image
    """
    def __init__(self):
        VGG_model = VGG16(weights='imagenet')
        self.model = Model(inputs=VGG_model.input, outputs=VGG_model.get_layer('fc1').output)
    
    def extract(self, img):
        """
        Extract feature from image
        params:
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        """
        img = img.resize((224, 224))
        img = img.convert_to("RGB")

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)

