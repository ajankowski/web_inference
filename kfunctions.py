import numpy as np
from keras.models import load_model
from keras.preprocessing import image

def upload_model():
    global model
    model = load_model('keras_trained_xor_model.h5')
    return model

def upload_model_MNIST():
    global model
    model = load_model('mnist_cnn.h5')
    return model

def przygotowanie_danych(dane):
    t = dane.split(',')
    i = int(t[0])
    j = int(t[1]) 
    return np.array([[i, j]])

def prepare_img(picture_path):
    img = image.load_img(path=picture_path,grayscale=True,target_size=(28,28))
    img = 255 - image.img_to_array(img)
    test_img = img.reshape((1,28,28,1))
    return test_img

def odp_sieci(prediction):
    p = list(prediction[0])
    for i in enumerate(p):
        if i[1] > 0.5:
            return f'{i[0]} ({i[1]})'
    return p
