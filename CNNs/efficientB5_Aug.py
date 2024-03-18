import os
import numpy as np
from PIL import Image, UnidentifiedImageError
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB5
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dense
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


def transform_to_three_channels(data):
    num_samples, height, width, channels = data.shape
    flattened_data = data.reshape(-1, channels)
    pca = PCA(n_components=3)
    transformed_data = pca.fit_transform(flattened_data)
    return transformed_data.reshape(num_samples, height, width, 3)


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

X_three_channels = transform_to_three_channels(X)
X_three_channels /= 255.0  # Normalize

input_tensor = Input(shape=(512, 512, 3))
base_model = EfficientNetB5(
    input_tensor=input_tensor, include_top=False, weights='imagenet')
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy', Precision(), Recall(), AUC()])

batch_size = 32

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_three_channels, y, test_size=0.2)

# Create data generators
train_datagen = ImageDataGenerator(horizontal_flip=True)
# You can keep augmentation for validation or just use ImageDataGenerator() without any augmentation.
val_datagen = ImageDataGenerator(horizontal_flip=True)

train_data = (X_train, y_train)
val_data = (X_val, y_val)

train_generator = train_datagen.flow(train_data, batch_size=batch_size)
val_generator = val_datagen.flow(val_data, batch_size=batch_size)

# Train the model
model.fit(train_generator,
          steps_per_epoch=len(X_train) / batch_size,
          epochs=10,
          validation_data=val_generator,
          validation_steps=len(X_val) / batch_size)
