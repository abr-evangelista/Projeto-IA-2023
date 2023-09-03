import cv2
import numpy as np
import json

# Create a dictionary to store contours for each image

def scale_contour(cnt, scale):
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        # set values as what you need in the situation
        cx, cy = 0, 0

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled 

fixed_contour_length = 100

for j in range(41,81):
    # Load an image
    image_path = f'./banco_destino/image{j}.png'
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #print(j) #Só para não me perder nas imagens

    # Find contours in the grayscale image
    contours = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    im_contours_dict = {
        "contornos": []
    }

    preprocessed_contours = []
    for contour in contours:
        leng = len(contour)
        if leng < fixed_contour_length:
            contour = cv2.approxPolyDP(contour, 0.02, closed=True)
            if leng < fixed_contour_length:
                contour = scale_contour(contour, 1.1)
        elif leng > fixed_contour_length:
            contour = cv2.approxPolyDP(contour, fixed_contour_length, closed=True)
        preprocessed_contours.append(contour)
        im_contours_dict["contornos"].append(contour.tolist())
    


    # Define minimum and maximum area thresholds for filtering contours
    min_contour_area = 7  # Adjust this value as needed
    max_contour_area = 200  # Adjust this value as needed

    # Merge near contours and filter noisy contours
    contours_filtered = []

    for contour in preprocessed_contours:
        area = cv2.contourArea(contour)
        if min_contour_area <= area <= max_contour_area:
            contours_filtered.append(contour)

    
    

    # Create dictionaries to store contours for each category
    contours_dict = {
        "guardarContornoBoca": [],
        "guardarContornoNariz": [],
        "guardarContornoOlhoEsquerdo": [],
        "guardarContornoOlhoDireito": [],
        "guardarRostoCompleto": [],
        "guardarRuido": []
    }

    # Navigate through the specified range of contours
    exit_flag = -1
    q_flag = 0
    for i, contour in enumerate(contours_filtered):
        # Access and process a specific contour by its index (e.g., i)
        cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)  # atual

        cv2.imshow(f'Contorno i, j: {i, j}', image)

        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)  # passado

        if q_flag == 1:
            contours_dict["guardarRuido"].append(contour.tolist())  # Convert to list
            continue

        key = cv2.waitKey(0)

        if key == ord('1'):
            contours_dict["guardarContornoBoca"].append(contour.tolist())  # Convert to list
            contours_dict["guardarRostoCompleto"].append(contour.tolist())  # Convert to list
        elif key == ord('2'):
            contours_dict["guardarContornoNariz"].append(contour.tolist())  # Convert to list
            contours_dict["guardarRostoCompleto"].append(contour.tolist())  # Convert to list
        elif key == ord('3'):
            contours_dict["guardarContornoOlhoEsquerdo"].append(contour.tolist())  # Convert to list
            contours_dict["guardarRostoCompleto"].append(contour.tolist())  # Convert to list
        elif key == ord('4'):
            contours_dict["guardarContornoOlhoDireito"].append(contour.tolist())  # Convert to list
            contours_dict["guardarRostoCompleto"].append(contour.tolist())  # Convert to list
        elif key == ord('q'):
            contours_dict["guardarRuido"].append(contour.tolist())  # Convert to list
            q_flag = 1
            continue
        elif key == ord('p'):
            exit_flag = 1
            break
        else:
            contours_dict["guardarRuido"].append(contour.tolist())  # Convert to list

    cv2.destroyAllWindows()

    with open(f'banco_destino_json/image{j}.json', 'w') as json_file:
        json.dump(im_contours_dict, json_file, indent=2)
    # Salva separadamente o json de labelling
    with open(f'banco_label/image{j}.json', 'w') as json_file:
        json.dump(contours_dict, json_file, indent=2) 

    if exit_flag == 1:
        break