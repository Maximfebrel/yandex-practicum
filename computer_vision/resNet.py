#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet import ResNet50


# In[2]:


def load_train(path):
 

    train_datagen = ImageDataGenerator(rescale=1/255, horizontal_flip=True, vertical_flip=True)
 

    train_datagen_flow = train_datagen.flow_from_directory(
        '/datasets/fruits/',
        target_size=(150, 150),
        batch_size=16,
        class_mode='sparse',
        seed=12345)
 

    return train_datagen_flow


# In[5]:


def create_model(input_shape):
 

    optimizer = Adam(lr=0.0001)
    backbone = ResNet50(input_shape=(150, 150, 3),
                    weights='imagenet', 
                    include_top=False)
    model = Sequential()
    model.add(backbone)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(12, activation='softmax')) 
 

    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['acc'])
 

    return model
 


# In[6]:


def train_model(model, train_data, test_data, batch_size=None, epochs=5,
                steps_per_epoch=None, validation_steps=None):
    if steps_per_epoch is None:
        steps_per_epoch = len(train_data)
    if validation_steps is None:
        validation_steps = len(test_data)
 

    model.fit(train_data,
              validation_data=test_data,
              epochs=epochs,
              batch_size=batch_size,
              steps_per_epoch=steps_per_epoch,
              validation_steps=validation_steps,
              verbose=2, shuffle=True)
 

    return model


# In[ ]:




