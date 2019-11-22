#For Keras model
from keras.models import Sequential
from keras import layers, optimizers, backend
from keras import regularizers
from keras.models import load_model

def create_AI():
    import keras.backend.tensorflow_backend as tb
    tb._SYMBOLIC_SCOPE.value = True
    model = load_model('ai/lstm_model.h5')
    model._make_predict_function()
    # model.load_weights('ai/best-weights.hdf5')

    return model