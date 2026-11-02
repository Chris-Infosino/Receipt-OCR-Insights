import os

import numpy as np
import easyocr

# Initialize the OCR reader and select language to read
reader = easyocr.Reader(['en'])

def extract_text(image_to_read, image_filename):
    """Use the OCR to extract text strings, confidence scores, and coordinates."""

    result = reader.readtext(image_to_read)
        
    extracted_ocr_data = {
    'raw_results': result,
    'filtered_results': [],
    'full_text': '',
    'confidence_stats': {},
    'word_count': 0,
    'line_count': 0
    }

    for (bbox, text, conf) in result:
        pts = np.array(bbox, dtype=np.int32)
        x_min, y_min = pts[:,0].min(), pts[:,1].min()
        x_max, y_max = pts[:,0].max(), pts[:,1].max()
        
        extracted_ocr_data['filtered_results'].append({
                    'filename': os.path.basename(image_filename),
                    'text': text,
                    'confidence': conf,
                    'bbox': bbox,
                    'xmin': x_min,
                    'ymin': y_min,
                    'xmax': x_max,
                    'ymax': y_max
                    })
    
    return extracted_ocr_data