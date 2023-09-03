import cv2
import numpy as np
import os
import json
from itertools import islice

# Step 1: Load your custom contour dataset and organize it into a list of images and contours

# Initialize lists to store images and corresponding contours
images_contours = []
label_contours = []

# Directory where your dataset is stored (each subdirectory contains images of a specific feature)
dataset_dir = 'banco_destino'
labels_dir = 'label'
MAX_ITERACOES = 3

# CARREGA DATASET
for image_file in islice(os.listdir(dataset_dir), MAX_ITERACOES):
    image_path = os.path.join(dataset_dir, image_file)

    # DATASET
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)      
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    images_contours.append(contours)

for label_file in islice(os.listdir(labels_dir), MAX_ITERACOES):        
    label_path = os.path.join(labels_dir, label_file)

    with open(label_path, 'r') as json_file:
        label_data = json.load(json_file)
        label_contours.append(label_data)

# Step 2: Convert the lists of images and contours into NumPy arrays
images_contours = np.array(images_contours, dtype=object)  # Use dtype=object for arrays of varying shape
label_contours = np.array(label_contours)

# Step 3: Split the data into training and testing sets
from sklearn.model_selection import train_test_split

#X_train, X_test, y_train, y_test = train_test_split(images_contours, label_contours, test_size=0.2, random_state=42)

# Step 4: Choose and initialize a machine learning or deep learning model (e.g., CNN)

# Step 5: Train the model on the training data and contours
# Here, you'll need to define a custom training loop or function
# that uses the contours as labels for your model

# Step 6: Evaluate the model's performance on the testing set (optional)

# Step 7: Deploy the trained model for facial feature recognition
