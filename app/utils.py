import pandas as pd
import numpy as np
import tensorflow_datasets as tfds
from tensorflow.keras import layers
import tensorflow as tf
import pickle
from keras.models import load_model




def preprocess(data):

    text = data['text[]']
    temperature = data['temperature[]']
    textLength = data['length[]']

    features = pd.DataFrame({'text' : text,
                             'temperature' : temperature,
                             'textLength': textLength}, index=[0])
    
    return features


