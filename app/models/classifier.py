import tensorflow as tf
import numpy as np
from PIL import Image
import io

class FossilClassifier:
    def __init__(self):
        self.model = tf.keras.models.load_model('models/fossil_classifier.h5')
        self.img_height = 224
        self.img_width = 224
        self.class_names = ['ammonite', 'belemnite', 'coral', 
                          'crinoid', 'leaf fossil', 'trilobite']

    def process_image(self, image_data):
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((self.img_height, self.img_width))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        return img_array / 255.0

    def predict(self, file):
        image_data = file.read()
        processed_image = self.process_image(image_data)
        predictions = self.model.predict(processed_image)
        predicted_class = self.class_names[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))
        
        return {
            'class': predicted_class,
            'confidence': float(confidence * 100)
        }