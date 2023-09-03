import cv2
import numpy as np
import json

# Create a dictionary to store contours for each image

for j in range(1, 3):
    # Load an image
    image_path = f'./banco_destino/image{j}.png'
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find contours in the grayscale image
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define minimum and maximum area thresholds for filtering contours
    min_contour_area = 7  # Adjust this value as needed
    max_contour_area = 50  # Adjust this value as needed

    # Merge near contours and filter noisy contours
    contours_filtered = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_contour_area <= area <= max_contour_area:
            contours_filtered.append(contour)

    # Create dictionaries to store contours for each category
    contours_dict = {
        "guardarContornoBoca": [],
        "guardarContornoNariz": [],
        "guardarContornoOlhoEsquerdo": [],
        "guardarContornoOlhoDireito": []
    }

    # Navigate through the specified range of contours
    for i, contour in enumerate(contours_filtered):
        # Access and process a specific contour by its index (e.g., i)
        cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)  # atual

        cv2.imshow(f'Contorno i: {i}', image)

        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)  # passado

        key = cv2.waitKey(0)

        if key == ord('1'):
            contours_dict["guardarContornoBoca"].append(contour.tolist())  # Convert to list
        elif key == ord('2'):
            contours_dict["guardarContornoNariz"].append(contour.tolist())  # Convert to list
        elif key == ord('3'):
            contours_dict["guardarContornoOlhoEsquerdo"].append(contour.tolist())  # Convert to list
        elif key == ord('4'):
            contours_dict["guardarContornoOlhoDireito"].append(contour.tolist())  # Convert to list
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

    # Salva separadamente o json de labelling
    with open(f'label/image{j}.json', 'w') as json_file:
        json.dump(contours_dict, json_file, indent=2)  


