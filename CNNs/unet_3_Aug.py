import numpy as np
import os
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall, AUC


def load_images_from_folder(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            img_path = os.path.join(folder, filename)
            try:
                img = image.load_img(img_path, target_size=(
                    512, 512), color_mode="rgb")
                img_array = image.img_to_array(img)
                images.append(img_array)
                labels.append(label)
            except UnidentifiedImageError:
                print(
                    f"Warning: Cannot identify image file {img_path}. Skipping.")
    return np.array(images), np.array(labels)


height, width = 512, 512

NDVI_burned, labels_burned_1 = load_images_from_folder(
    "../data/NDVI/Burned", 1)
NDVI_unburned, labels_unburned_1 = load_images_from_folder(
    "../data/NDVI/Unburned", 0)
NDMI_burned, labels_burned_2 = load_images_from_folder(
    "../data/NDMI/Burned", 1)
NDMI_unburned, labels_unburned_2 = load_images_from_folder(
    "../data/NDMI/Unburned", 0)

assert np.array_equal(labels_burned_1, labels_burned_2)
assert np.array_equal(labels_unburned_1, labels_unburned_2)

X_burned = np.concatenate([NDVI_burned, NDMI_burned], axis=-1)
X_unburned = np.concatenate([NDVI_unburned, NDMI_unburned], axis=-1)

X = np.vstack([X_burned, X_unburned])
y = np.hstack([labels_burned_1, labels_unburned_1])

X = X / 255.0


def unet_model(input_shape):
    inputs = Input(input_shape)

    # Contracting path
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(256, (3, 3), activation='relu', padding='same')(p2)
    c3 = Conv2D(256, (3, 3), activation='relu', padding='same')(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(512, (3, 3), activation='relu', padding='same')(p3)
    c4 = Conv2D(512, (3, 3), activation='relu', padding='same')(c4)

    # Expansive path
    u5 = UpSampling2D((2, 2))(c4)
    u5 = Concatenate()([u5, c3])
    c5 = Conv2D(256, (3, 3), activation='relu', padding='same')(u5)
    c5 = Conv2D(256, (3, 3), activation='relu', padding='same')(c5)

    u6 = UpSampling2D((2, 2))(c5)
    u6 = Concatenate()([u6, c2])
    c6 = Conv2D(128, (3, 3), activation='relu', padding='same')(u6)
    c6 = Conv2D(128, (3, 3), activation='relu', padding='same')(c6)

    u7 = UpSampling2D((2, 2))(c6)
    u7 = Concatenate()([u7, c1])
    c7 = Conv2D(64, (3, 3), activation='relu', padding='same')(u7)
    c7 = Conv2D(64, (3, 3), activation='relu', padding='same')(c7)

    flat = Flatten()(c7)  # Add a flatten layer
    outputs = Dense(1, activation='sigmoid')(flat)

    model = Model(inputs=inputs, outputs=outputs)
    return model


unet = unet_model((height, width, 6))
unet.compile(optimizer='adam',
             loss='binary_crossentropy',
             metrics=['accuracy', Precision(), Recall(), AUC()])


datagen = ImageDataGenerator(horizontal_flip=True)

split_idx = int(0.8 * len(X))
X_train, X_val = X[:split_idx], X[split_idx:]
y_train, y_val = y[:split_idx], y[split_idx:]

y_train = y_train.reshape(-1, 1)
y_val = y_val.reshape(-1, 1)

batch_size = 32
train_gen = datagen.flow(X_train, y_train, batch_size=batch_size)
val_gen = datagen.flow(X_val, y_val, batch_size=batch_size)

unet.fit(train_gen, epochs=10, validation_data=val_gen)
