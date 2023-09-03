import cv2
import numpy as np
import json


def compare_contours_by_shape(contour1, contour2, threshold=0):
    """
    Compare two contours based on their shape similarity using Hu Moments.

    Args:
        contour1: The first contour to compare (OpenCV contour or list of points).
        contour2: The second contour to compare (OpenCV contour or list of points).
        threshold: A threshold value to determine the similarity. Default is 0.3.

    Returns:
        True if the contours are similar (Hu Moments similarity >= threshold), False otherwise.
    """
    # Convert both contours to OpenCV contour format
    if not isinstance(contour1, np.ndarray):
        contour1 = np.array(contour1)
    if not isinstance(contour2, np.ndarray):
        contour2 = np.array(contour2)

    # Calculate Hu Moments for each contour
    hu_moments1 = cv2.HuMoments(cv2.moments(contour1)).flatten()
    hu_moments2 = cv2.HuMoments(cv2.moments(contour2)).flatten()

    # Compare Hu Moments using a similarity metric (lower values are more similar)
    similarity = cv2.matchShapes(hu_moments1, hu_moments2, cv2.CONTOURS_MATCH_I1, 0.0)

    # Compare the similarity with the threshold
    return similarity <= threshold

# Load contours data from the JSON file
with open('contours_data.json', 'r') as json_file:
    contours_data = json.load(json_file)


# Example usage:
if __name__ == "__main__":
    # Load two example images
    image2 = cv2.imread('banco_destino/image2.png', cv2.IMREAD_GRAYSCALE)

    # Find contours in the second image
    contours2, _ = cv2.findContours(image2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    resultadoFinal = []
    aaaaa = 0
    # Iterate through the contours for image2
    for i, contour in enumerate(contours2):
        # Compare the current contour to the saved contours from the JSON file
        for category, saved_contours in contours_data['image1'].items():
            if category == "guardarContornoBoca":
                for saved_contour in saved_contours:
                    result = compare_contours_by_shape(saved_contour, contour)

                    if result == True:
                        resultadoFinal.append(contour)


    canvas = np.zeros_like(image2)
    cv2.drawContours(canvas, resultadoFinal, -1, (255, 255, 255), 2)
    cv2.imshow(f'teste{i}_{category}', canvas)
    cv2.waitKey(0)