import cv2
import json
import numpy as np

# Load the JSON file containing contours data
with open('contours_data.json', 'r') as json_file:
    contours_data = json.load(json_file)

# Loop through each image and its associated contours
for image_name, contours_dict in contours_data.items():
    # Load the corresponding image
    image_path = f'./banco_destino/{image_name}.png'
    image = cv2.imread(image_path)

    # Create an empty canvas for drawing contours
    canvas = np.zeros_like(image)

    # Loop through each category and draw its contours
    for category, contours_list in contours_dict.items():
        for i, contour_points in enumerate(contours_list):
            contour = np.array(contour_points)  # Convert the list back to a NumPy array
            cv2.drawContours(canvas, [contour], -1, (0, 255, 0), 2)  # Draw contours in green
            cv2.imshow(f'Contours for {i}', canvas)
            cv2.waitKey(0)


cv2.destroyAllWindows()
