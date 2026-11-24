import cv2

from constants import READER

def getSkewAngle(orig_image) -> float:
    """Get the angle and direction of skew for the provided image."""
    
    # Prep image for contour identification
    image_copy = orig_image.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Dilate to merge text by lines and paragraph, with large kernel on X axis to merge characters and small kernel on Y axis to separate blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, _hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for contour in contours:
        rect = cv2.boundingRect(contour)
        x,y,width,height = rect
        cv2.rectangle(image_copy,(x,y),(x+width,y+height),(0,255,0),2)

    # Find largest contour and surround in minimun area rectangle
    largest_contour = contours[0]
    minAreaRect = cv2.minAreaRect(largest_contour)

    # cv2.imwrite("temp/boxes.jpg", image_copy)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

def rotateImage(orig_image, angle: float):
    """Rotate the image around its center."""
    
    image_copy = orig_image.copy()
    (height, width) = image_copy.shape[:2]
    center = (width // 2, height // 2)
    Matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    image_copy = cv2.warpAffine(image_copy, Matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return image_copy

def deskew(orig_image):
    angle = getSkewAngle(orig_image)
    return rotateImage(orig_image, -1.0 * angle)

def assess_confidence(image_to_read, preprocess_type, image_confidences):
    """Check if the preprocessing step improved the confidence of read text."""

    result = READER.readtext(image_to_read)
    image_confidence = 0
    for (_bbox, _text, conf) in result:
        image_confidence = image_confidence + conf
    
    image_confidences.append({
        'image_file': image_to_read,
        'preprocess_type': preprocess_type,
        'image_confidence': image_confidence})
    
def select_best_image(image_confidences):
    best_preprocess = max(image_confidences, key=lambda result:result["image_confidence"])
    best_image = best_preprocess['image_file']
    return(best_image)
    
def preprocess_image(orig_image): 
    """Improve the default easyocr reader using image preprocessing."""
    
    image_confidences = []
    
    assess_confidence(orig_image, 'None', image_confidences)

    aligned_image = deskew(orig_image)
    assess_confidence(aligned_image, 'Aligning the Image', image_confidences)
    
    current_best_image = select_best_image(image_confidences)
    inverted_image = cv2.bitwise_not(current_best_image)
    assess_confidence(inverted_image, 'Inversion', image_confidences)
    
    current_best_image = select_best_image(image_confidences)
    grayscale_image = cv2.cvtColor(current_best_image, cv2.COLOR_BGR2GRAY)
    assess_confidence(grayscale_image, 'Grayscale', image_confidences)

    threshold = 128 #pixels from 0 to 127 become white, pixels from 128 to 255 become black
    binary_image = cv2.threshold(grayscale_image, threshold, 255, cv2.THRESH_BINARY)[1]
    assess_confidence(binary_image, 'Binarization', image_confidences)

    ideal_image_for_processing = select_best_image(image_confidences)
    return(ideal_image_for_processing)