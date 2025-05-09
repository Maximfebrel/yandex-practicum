from tensorflow.keras.datasets import fashion_mnist

from tensorflow.keras.layers import Conv2D, Flatten, Dense, AvgPool2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np

optimizer = Adam(lr=0.001)


def load_train(path):
    features_train = np.load(path + 'train_features.npy')
    target_train = np.load(path + 'train_target.npy')
    features_train = features_train.reshape(features_train.shape[0], 28, 28, 1) / 255.
    return features_train, target_train


def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(filters=10, kernel_size=(3, 3), padding='valid', activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(filters=10, kernel_size=(3, 3), input_shape=input_shape, activation='relu', padding='valid'))
    model.add(AvgPool2D(pool_size=(10, 10)))
    model.add(Flatten())
    model.add(Dense(128, input_shape=input_shape, activation='relu'))
    model.add(Dense(128, input_shape=input_shape, activation='relu'))
    model.add(Dense(128, input_shape=input_shape, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy',
                  metrics=['acc'])

    return model


def train_model(model, train_data, test_data, batch_size=32, epochs=24,
                steps_per_epoch=None, validation_steps=None):
    features_train, target_train = train_data
    features_test, target_test = test_data
    model.fit(features_train, target_train,
              validation_data=(features_test, target_test),
              batch_size=batch_size, epochs=epochs,
              steps_per_epoch=steps_per_epoch,
              validation_steps=validation_steps,
              verbose=2, shuffle=True)

    return model