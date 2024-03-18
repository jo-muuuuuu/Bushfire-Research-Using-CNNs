import numpy as np
import os
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
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
            except PIL.UnidentifiedImageError:
                print(
                    f"Warning: Cannot identify image file {img_path}. Skipping.")

    # for filename in os.listdir(folder):
    #    img_path = os.path.join(folder, filename)
    #   img = image.load_img(img_path, target_size=(512, 512), color_mode="rgb")
    #   img_array = image.img_to_array(img)
    #   images.append(img_array)
    #   labels.append(label)
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

# Verify the number of labels
assert np.array_equal(labels_burned_1, labels_burned_2)
assert np.array_equal(labels_unburned_1, labels_unburned_2)

X_burned = np.concatenate([NDVI_burned, NDMI_burned], axis=-1)
X_unburned = np.concatenate([NDVI_unburned, NDMI_unburned], axis=-1)

X = np.vstack([X_burned, X_unburned])
y = np.hstack([labels_burned_1, labels_unburned_1])

X = X / 255.0

model = Sequential([
    Conv2D(6, (5, 5), 1, activation='relu', kernel_initializer='he_normal',
           input_shape=(height, width, 6)),
    MaxPooling2D(2, 2),

    Conv2D(16, (5, 5), 1, activation='relu', kernel_initializer='he_normal'),
    MaxPooling2D(2, 2),
    Conv2D(120, (5, 5), 1, activation='relu', kernel_initializer='he_normal'),

    Flatten(),
    Dense(84, activation='relu', kernel_initializer='he_normal'),
    Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy', Precision(), Recall(), AUC()])

datagen = ImageDataGenerator(
    horizontal_flip=True
)

# Splitting data into training and validation
split_idx = int(0.8 * len(X))
X_train, X_val = X[:split_idx], X[split_idx:]
y_train, y_val = y[:split_idx], y[split_idx:]

batch_size = 32

# Creating two separate iterators for training and validation
train_gen = datagen.flow(X_train, y_train, batch_size=batch_size)
val_gen = datagen.flow(X_val, y_val, batch_size=batch_size)

# Training
model.fit(train_gen, epochs=10, validation_data=val_gen)
