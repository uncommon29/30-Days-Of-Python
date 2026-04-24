# Python for Deep Learning - Complete Guide

A comprehensive guide to learning Python specifically for Deep Learning applications.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Essential Libraries](#essential-libraries)
3. [NumPy for Deep Learning](#numpy-for-deep-learning)
4. [Data Preprocessing with Pandas](#data-preprocessing-with-pandas)
5. [Visualization with Matplotlib](#visualization-with-matplotlib)
6. [Introduction to Neural Networks](#introduction-to-neural-networks)
7. [Building Your First Neural Network](#building-your-first-neural-network)
8. [Convolutional Neural Networks (CNN)](#convolutional-neural-networks-cnn)
9. [Recurrent Neural Networks (RNN)](#recurrent-neural-networks-rnn)
10. [Transfer Learning](#transfer-learning)
11. [Best Practices](#best-practices)

---

## Prerequisites

Before diving into deep learning, you should be comfortable with:
- Basic Python programming
- Variables, data types, and operators
- Functions and modules
- Lists, dictionaries, and tuples
- Loops and conditionals
- Basic mathematics (linear algebra, calculus)

---

## Essential Libraries

Install the required libraries:

```bash
pip install numpy pandas matplotlib scikit-learn tensorflow torch torchvision
```

### Import Statement Template

```python
# Numerical computing
import numpy as np

# Data manipulation
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Deep Learning - TensorFlow/Keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models

# Deep Learning - PyTorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
```

---

## NumPy for Deep Learning

NumPy is the foundation for all deep learning operations.

### Creating Arrays

```python
import numpy as np

# Create arrays
scalar = np.array(5)                    # 0-D array
vector = np.array([1, 2, 3, 4])         # 1-D array
matrix = np.array([[1, 2], [3, 4]])     # 2-D array
tensor = np.array([[[1, 2], [3, 4]], 
                   [[5, 6], [7, 8]]])   # 3-D array

print(f"Scalar shape: {scalar.shape}")
print(f"Vector shape: {vector.shape}")
print(f"Matrix shape: {matrix.shape}")
print(f"Tensor shape: {tensor.shape}")

# Special arrays
zeros = np.zeros((3, 3))                # Array of zeros
ones = np.ones((2, 4))                  # Array of ones
identity = np.eye(3)                    # Identity matrix
random_arr = np.random.rand(3, 3)       # Random values [0, 1)
random_normal = np.random.randn(3, 3)   # Random normal distribution
range_arr = np.arange(0, 10, 2)         # Range with step
linspace = np.linspace(0, 1, 5)         # Evenly spaced values
```

### Array Operations

```python
# Mathematical operations
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

addition = a + b           # Element-wise addition
subtraction = a - b        # Element-wise subtraction
multiplication = a * b     # Element-wise multiplication
division = a / b           # Element-wise division
power = a ** 2             # Element-wise power

# Matrix operations
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])

dot_product = np.dot(matrix_a, matrix_b)    # Matrix multiplication
matrix_power = np.linalg.matrix_power(matrix_a, 2)
inverse = np.linalg.inv(matrix_a)           # Matrix inverse
determinant = np.linalg.det(matrix_a)       # Determinant
transpose = matrix_a.T                      # Transpose

# Statistical operations
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

mean = np.mean(data)
median = np.median(data)
std_dev = np.std(data)
variance = np.var(data)
min_val = np.min(data)
max_val = np.max(data)
sum_val = np.sum(data)

# Reshaping arrays
arr = np.arange(12)
reshaped = arr.reshape(3, 4)        # Reshape to 3x4
flattened = reshaped.flatten()      # Flatten to 1D
transposed = reshaped.T             # Transpose

# Broadcasting
row_vector = np.array([1, 2, 3])
column_vector = np.array([[1], [2], [3]])
result = row_vector + column_vector  # Broadcasting example
```

### Indexing and Slicing

```python
arr = np.array([[1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]])

# Basic indexing
element = arr[1, 2]          # Get element at row 1, col 2
row = arr[1]                 # Get entire row 1
column = arr[:, 2]           # Get entire column 2

# Slicing
subarray = arr[0:2, 1:4]     # Rows 0-1, columns 1-3

# Boolean indexing
mask = arr > 7               # Create boolean mask
filtered = arr[mask]         # Get elements > 7

# Fancy indexing
indices = np.array([0, 2])
selected_rows = arr[indices] # Select specific rows
```

---

## Data Preprocessing with Pandas

### Loading and Exploring Data

```python
import pandas as pd

# Load data
df = pd.read_csv('dataset.csv')
# df = pd.read_excel('dataset.xlsx')
# df = pd.read_json('dataset.json')

# Explore data
print(df.head())              # First 5 rows
print(df.tail())              # Last 5 rows
print(df.info())              # Data types and non-null counts
print(df.describe())          # Statistical summary
print(df.shape)               # (rows, columns)
print(df.columns)             # Column names
print(df.dtypes)              # Data types
```

### Data Cleaning

```python
# Handle missing values
df.dropna()                           # Drop rows with NaN
df.fillna(0)                          # Fill NaN with 0
df.fillna(df.mean())                  # Fill NaN with mean
df['column'].fillna(method='ffill')   # Forward fill

# Remove duplicates
df.drop_duplicates()

# Rename columns
df.rename(columns={'old_name': 'new_name'}, inplace=True)

# Change data types
df['column'] = df['column'].astype('float32')
```

### Feature Engineering

```python
# Create new features
df['new_feature'] = df['feature1'] * df['feature2']
df['log_feature'] = np.log(df['feature1'])

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label Encoding (for ordinal data)
le = LabelEncoder()
df['encoded_column'] = le.fit_transform(df['category_column'])

# One-Hot Encoding (for nominal data)
df_encoded = pd.get_dummies(df, columns=['category_column'])

# Scale features
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
df[['scaled_feature']] = scaler.fit_transform(df[['feature']])

min_max_scaler = MinMaxScaler()
df[['normalized_feature']] = min_max_scaler.fit_transform(df[['feature']])
```

### Splitting Data

```python
from sklearn.model_selection import train_test_split

# Split features and target
X = df.drop('target', axis=1)
y = df['target']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42,    # For reproducibility
    stratify=y          # Maintain class distribution
)

# Further split training into training and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train,
    test_size=0.2,
    random_state=42
)
```

---

## Visualization with Matplotlib

### Basic Plots

```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('X')
plt.ylabel('sin(X)')
plt.grid(True)
plt.show()

# Scatter plot
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 100 * np.random.rand(50)
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5)
plt.title('Scatter Plot')
plt.show()

# Bar chart
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]
plt.bar(categories, values)
plt.title('Bar Chart')
plt.show()

# Histogram
data = np.random.randn(1000)
plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].scatter(x, y)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)
plt.tight_layout()
plt.show()
```

### Deep Learning Visualizations

```python
# Training history visualization
def plot_training_history(history):
    """Plot training and validation accuracy/loss"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy
    ax1.plot(history.history['accuracy'], label='Train Acc')
    ax1.plot(history.history['val_accuracy'], label='Val Acc')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Loss
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

# Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_confusion_matrix(y_true, y_pred, classes):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
```

---

## Introduction to Neural Networks

### What is a Neural Network?

A neural network is a computational model inspired by the human brain, consisting of:
- **Input Layer**: Receives the input data
- **Hidden Layers**: Process the data through weighted connections
- **Output Layer**: Produces the final prediction
- **Activation Functions**: Introduce non-linearity (ReLU, Sigmoid, Tanh, Softmax)
- **Weights and Biases**: Learnable parameters

### Common Activation Functions

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 100)

# ReLU (Rectified Linear Unit)
def relu(x):
    return np.maximum(0, x)

# Sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Tanh
def tanh(x):
    return np.tanh(x)

# Softmax (for multi-class classification)
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Plot activation functions
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(x, relu(x))
axes[0].set_title('ReLU')
axes[0].grid(True)

axes[1].plot(x, sigmoid(x))
axes[1].set_title('Sigmoid')
axes[1].grid(True)

axes[2].plot(x, tanh(x))
axes[2].set_title('Tanh')
axes[2].grid(True)

plt.tight_layout()
plt.show()
```

---

## Building Your First Neural Network

### Using TensorFlow/Keras

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, 
                           n_classes=2, random_state=42)

# Preprocess data
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build the model
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(20,)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Display model architecture
model.summary()

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_accuracy:.4f}')

# Make predictions
predictions = model.predict(X_test)
predicted_classes = (predictions > 0.5).astype(int)
```

### Multi-Class Classification Example

```python
# Generate multi-class data
X, y = make_classification(n_samples=1000, n_features=20, 
                           n_classes=3, n_informative=15, 
                           random_state=42)

# Preprocess
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build model for multi-class classification
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(20,)),
    layers.Dropout(0.4),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes
])

# Compile with categorical crossentropy
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
    ]
)
```

### Regression Example

```python
from sklearn.datasets import make_regression

# Generate regression data
X, y = make_regression(n_samples=1000, n_features=10, 
                       noise=0.1, random_state=42)

# Preprocess
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build regression model
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)  # No activation for regression
])

# Compile with MSE loss
model.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae']
)

# Train
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Evaluate
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f'Test MAE: {test_mae:.4f}')
```

---

## Convolutional Neural Networks (CNN)

CNNs are specialized for processing grid-like data such as images.

### CNN Architecture Components

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Preprocess
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build CNN model
cnn_model = models.Sequential([
    # First Conv Block
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # Second Conv Block
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # Fully Connected Layers
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# Compile
cnn_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

cnn_model.summary()

# Train
history = cnn_model.fit(
    x_train, y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.1,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7
        )
    ]
)

# Evaluate
test_loss, test_acc = cnn_model.evaluate(x_test, y_test)
print(f'Test Accuracy: {test_acc:.4f}')
```

### Data Augmentation for Images

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create data augmentation generator
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    shear_range=0.1,
    fill_mode='nearest'
)

# Fit on training data
datagen.fit(x_train)

# Train with augmented data
history = cnn_model.fit(
    datagen.flow(x_train, y_train, batch_size=128),
    epochs=30,
    validation_data=(x_test, y_test),
    steps_per_epoch=len(x_train) // 128
)
```

---

## Recurrent Neural Networks (RNN)

RNNs are designed for sequential data like time series, text, and speech.

### Simple RNN/LSTM for Sequence Prediction

```python
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load IMDB movie review dataset
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

# Pad sequences to same length
x_train = pad_sequences(x_train, maxlen=500)
x_test = pad_sequences(x_test, maxlen=500)

# Build LSTM model
lstm_model = models.Sequential([
    layers.Embedding(10000, 128, input_length=500),
    layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

# Compile
lstm_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

lstm_model.summary()

# Train
history = lstm_model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        )
    ]
)

# Evaluate
test_loss, test_acc = lstm_model.evaluate(x_test, y_test)
print(f'Test Accuracy: {test_acc:.4f}')
```

### Bidirectional LSTM

```python
# Bidirectional LSTM for better context understanding
bi_lstm_model = models.Sequential([
    layers.Embedding(10000, 128, input_length=500),
    layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
    layers.Bidirectional(layers.LSTM(32)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

bi_lstm_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

bi_lstm_model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.2
)
```

### GRU (Gated Recurrent Unit)

```python
# GRU - Faster alternative to LSTM
gru_model = models.Sequential([
    layers.Embedding(10000, 128, input_length=500),
    layers.GRU(64, dropout=0.2, recurrent_dropout=0.2),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

gru_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

gru_model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.2
)
```

---

## Transfer Learning

Use pre-trained models to solve your problems with less data and computation.

### Using Pre-trained Models (VGG16, ResNet, etc.)

```python
from tensorflow.keras.applications import VGG16, ResNet50, MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout

# Load pre-trained VGG16 (without top layers)
base_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model
base_model.trainable = False

# Add custom layers
inputs = keras.Input(shape=(224, 224, 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(10, activation='softmax')(x)  # 10 classes

# Create model
model = Model(inputs, outputs)

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Fine-tuning (optional - unfreeze some layers after initial training)
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### Popular Pre-trained Models

```python
# Available pre-trained models in Keras
from tensorflow.keras.applications import (
    VGG16, VGG19,
    ResNet50, ResNet101, ResNet152,
    InceptionV3, InceptionResNetV2,
    MobileNet, MobileNetV2,
    DenseNet121, DenseNet169, DenseNet201,
    EfficientNetB0, EfficientNetB1, EfficientNetB2,
    Xception
)

# Example: Load different models
models_dict = {
    'VGG16': VGG16(weights='imagenet', include_top=False),
    'ResNet50': ResNet50(weights='imagenet', include_top=False),
    'MobileNetV2': MobileNetV2(weights='imagenet', include_top=False),
    'EfficientNetB0': EfficientNetB0(weights='imagenet', include_top=False),
}

for name, model in models_dict.items():
    print(f"{name}: {model.input_shape} -> {model.output_shape}")
```

---

## Best Practices

### 1. Prevent Overfitting

```python
# Techniques to prevent overfitting
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(input_dim,)),
    
    # Dropout
    layers.Dropout(0.5),
    
    # Batch Normalization
    layers.BatchNormalization(),
    
    # L2 Regularization
    layers.Dense(64, activation='relu', 
                 kernel_regularizer=keras.regularizers.l2(0.01)),
    
    # Early Stopping (callback)
    # Reduce Learning Rate (callback)
])

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]
```

### 2. Learning Rate Scheduling

```python
# Learning rate scheduler
def lr_schedule(epoch, lr):
    if epoch < 10:
        return lr
    elif epoch < 20:
        return lr * 0.5
    else:
        return lr * 0.1

lr_callback = keras.callbacks.LearningRateScheduler(lr_schedule)

# Or use built-in schedulers
optimizer = keras.optimizers.Adam(
    learning_rate=0.001,
    decay=1e-5
)
```

### 3. Data Pipeline Optimization

```python
# For large datasets, use tf.data API
import tensorflow as tf

def create_dataset(images, labels, batch_size=32, shuffle=True):
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(images))
    
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)  # Optimize performance
    
    return dataset

train_dataset = create_dataset(x_train, y_train, batch_size=32)
val_dataset = create_dataset(x_val, y_val, batch_size=32, shuffle=False)

model.fit(train_dataset, validation_data=val_dataset, epochs=50)
```

### 4. Model Saving and Loading

```python
# Save model
model.save('my_model.h5')  # Save entire model
model.save_weights('my_weights.h5')  # Save only weights

# Save model architecture
model_config = model.to_json()
with open('model_architecture.json', 'w') as f:
    f.write(model_config)

# Load model
loaded_model = keras.models.load_model('my_model.h5')

# Load weights
model.load_weights('my_weights.h5')
```

### 5. GPU Acceleration

```python
# Check GPU availability
import tensorflow as tf
print("GPUs Available:", tf.config.list_physical_devices('GPU'))

# Set memory growth (prevent allocating all GPU memory)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Mixed precision training (faster on modern GPUs)
from tensorflow.keras import mixed_precision
mixed_precision.set_global_policy('mixed_float16')
```

### 6. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier

def create_model(learning_rate=0.01, dropout_rate=0.2, neurons=64):
    model = models.Sequential([
        layers.Dense(neurons, activation='relu', input_shape=(20,)),
        layers.Dropout(dropout_rate),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

# Wrap model for sklearn
model = KerasClassifier(build_fn=create_model, verbose=0)

# Define hyperparameter grid
param_grid = {
    'learning_rate': [0.001, 0.01, 0.1],
    'dropout_rate': [0.2, 0.3, 0.4],
    'neurons': [32, 64, 128],
    'epochs': [50, 100]
}

# Grid search
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
grid_result = grid.fit(X_train, y_train)

print(f"Best Parameters: {grid_result.best_params_}")
```

---

## Complete Example: Image Classification Project

```python
"""
Complete Deep Learning Project: CIFAR-10 Image Classification
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# 1. Load and explore data
print("Loading CIFAR-10 dataset...")
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

print(f"Training samples: {len(x_train)}")
print(f"Test samples: {len(x_test)}")
print(f"Image shape: {x_train[0].shape}")

# 2. Visualize sample images
plt.figure(figsize=(10, 10))
for i in range(9):
    plt.subplot(3, 3, i+1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]])
    plt.axis('off')
plt.tight_layout()
plt.show()

# 3. Preprocess data
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# 4. Data augmentation
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)
datagen.fit(x_train)

# 5. Build CNN model
def create_cnn_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', padding='same', 
                     input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    return model

model = create_cnn_model()

# 6. Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# 7. Define callbacks
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='cifar10_best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

# 8. Train model
print("\nTraining model...")
history = model.fit(
    datagen.flow(x_train, y_train_cat, batch_size=64),
    epochs=100,
    validation_data=(x_test, y_test_cat),
    callbacks=callbacks
)

# 9. Evaluate model
test_loss, test_accuracy = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

# 10. Plot training history
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(history.history['accuracy'], label='Train Acc')
ax1.plot(history.history['val_accuracy'], label='Val Acc')
ax1.set_title('Model Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True)

ax2.plot(history.history['loss'], label='Train Loss')
ax2.plot(history.history['val_loss'], label='Val Loss')
ax2.set_title('Model Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# 11. Make predictions and evaluate
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test_cat, axis=1)

# Classification report
print("\nClassification Report:")
print(classification_report(true_classes, predicted_classes, 
                            target_names=class_names))

# Confusion matrix
cm = confusion_matrix(true_classes, predicted_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 12. Visualize predictions
plt.figure(figsize=(15, 15))
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.imshow(x_test[i])
    color = 'green' if predicted_classes[i] == true_classes[i] else 'red'
    plt.title(f"Pred: {class_names[predicted_classes[i]]}\nTrue: {class_names[true_classes[i]]}", 
              color=color)
    plt.axis('off')
plt.tight_layout()
plt.show()

# 13. Save model
model.save('cifar10_classifier.h5')
print("\nModel saved successfully!")
```

---

## Next Steps

After mastering these fundamentals, explore:

1. **Advanced Architectures**: Transformers, Attention Mechanisms, GANs
2. **Specialized Domains**: NLP, Computer Vision, Time Series, Reinforcement Learning
3. **Deployment**: TensorFlow Serving, ONNX, TensorRT, Mobile deployment
4. **MLOps**: Model versioning, monitoring, CI/CD for ML
5. **Cloud Platforms**: AWS SageMaker, Google AI Platform, Azure ML

## Resources

- **Official Documentation**: 
  - [TensorFlow](https://www.tensorflow.org/)
  - [PyTorch](https://pytorch.org/)
  - [Keras](https://keras.io/)

- **Courses**:
  - DeepLearning.AI (Coursera)
  - Fast.ai
  - Stanford CS231n (Computer Vision)
  - Stanford CS224n (NLP)

- **Books**:
  - "Deep Learning" by Ian Goodfellow
  - "Hands-On Machine Learning" by Aurélien Géron

- **Practice Platforms**:
  - Kaggle
  - Google Colab (free GPU)
  - Papers With Code

---

**Happy Learning! 🚀**
