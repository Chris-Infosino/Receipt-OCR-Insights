import re
import csv
import json
from pathlib import Path

import pandas as pd

from constants import OUTPUT_CSV_FILE_PATH, INCLUDE_TOTAL_TEXTS, EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS, EXCLUDED_DATE_TEXTS, INCLUDE_DATE_TEXTS, IMAGES_DIR, OUTPUT_JSON_DIR
from date_finder import check_if_date, PROBABLE_DATE_FORMAT

def annotation_coordinates(class_label, important_ocr_data, row):
    """Create a CSV file containing details of important information from receipts, to include the date of the transaction and the totals/amounts."""
    important_ocr_data['all_classes'].append({
    'filename': row['filename'],
    'class': class_label,
    'xmin': row['xmin'],
    'ymin': row['ymin'],
    'xmax': row['xmax'],
    'ymax': row['ymax'],
    'text': row['text']
    })

def create_csv (extracted_ocr_data):    
    """Append csv with details of every image highlighting identified text and bboxes."""
    important_ocr_data = {
        'all_classes': []
        }
    indices_of_totals = []
    indices_of_dates = []
    indices_of_non_dates = []
    filtered_results = extracted_ocr_data['filtered_results']

    if OUTPUT_CSV_FILE_PATH.exists():
        with open(OUTPUT_CSV_FILE_PATH, mode='r', newline='') as csv_file:
            num_rows = len(csv_file.readlines())
        # Add headers if the file does not already have them
        if num_rows > 0:
            pass
        else:
            with open(OUTPUT_CSV_FILE_PATH, mode='a', newline='') as csv_file:
                fieldnames = ['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'text']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
    else:
        with open(OUTPUT_CSV_FILE_PATH, mode='a', newline='') as csv_file:
            fieldnames = ['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'text']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
    
    with open(OUTPUT_CSV_FILE_PATH, mode='a', newline='') as csv_file:
        fieldnames = ['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for row in filtered_results:
            # Add instances of total text read by the OCR to csv
            if any(included_word in row['text'].lower() for included_word in INCLUDE_TOTAL_TEXTS):
                if any(excluded_word in row['text'].lower() for excluded_word in EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS):
                    continue
                else:
                    annotation_coordinates("total", important_ocr_data, row)
                    indices_of_totals.append(filtered_results.index(row))
            # Remove non-date text
            elif any(excluded_word in row['text'].lower() for excluded_word in EXCLUDED_DATE_TEXTS):
                indices_of_non_dates.append(filtered_results.index(row))
            # Add instances of date text read by the OCR to csv
            elif any(included_word in row['text'].lower() for included_word in INCLUDE_DATE_TEXTS):
                annotation_coordinates("date", important_ocr_data, row)
                indices_of_dates.append(filtered_results.index(row))            
            elif (filtered_results.index(row)- 1) in indices_of_dates and re.search(r'[\d]', row['text']):            
                annotation_coordinates("date", important_ocr_data, row)
            # Add string values that are identified as potential dates to csv  
            elif len(check_if_date(str(row['text']))) != 0:
                if (filtered_results.index(row)- 1) in indices_of_non_dates and not(re.search(PROBABLE_DATE_FORMAT, row['text'])) or (filtered_results.index(row)- 1) in indices_of_totals or (filtered_results.index(row)- 2) in indices_of_totals:
                    continue
                else:   
                    annotation_coordinates("potential datetime", important_ocr_data, row)
            # Add amounts that are seen after "total" instances
            elif (filtered_results.index(row)- 1) in indices_of_totals:
                if re.search(r'[A-Za-z]' or r'[^\$\.\,]', row['text']):
                    continue
                else:
                    annotation_coordinates("amount", important_ocr_data, row)
        
        for row in important_ocr_data['all_classes']:
            # Write annotation to CSV
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(row)

    return important_ocr_data

def create_json_file(output, output_dir: str, image_file_name): 
    """Create JSON files containing identified important text, coordinates, and labels."""
    Path(OUTPUT_JSON_DIR).mkdir(parents=True, exist_ok=True)
    
    # Save JSON to input/json folder
    json_path = Path(output_dir, image_file_name + '_ocr_results.json')
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def get_json_details(image_name: str, annotations_csv: pd.DataFrame) -> dict:
    """Create each part of the JSON file working from the smallest section up."""
    image_data = annotations_csv.loc[annotations_csv["filename"] == image_name]    
    image_path = str(Path(IMAGES_DIR, image_name))
    info_json_path = str(Path(OUTPUT_JSON_DIR, image_name + '_ocr_results.json'))
    
    date_words = []
    total_words = []
    important_words = []
    
    # Highlight coordinates section for each important block of text and its label
    for _index, row in image_data.iterrows():  
        if "total" in row["class"].lower() or "amount" in row["class"].lower():
            coordinates = {
                "xmin": row["xmin"],
                "ymin": row["ymin"],
                "xmax": row["xmax"],
                "ymax": row["ymax"]
                }
        # Create "total" words section to join coordinate with the important block of text                
            important_info = row["text"]
            word = {
                "Coordinates": coordinates,
                "Text": important_info
                }
            total_words.append(word)
        # Create important "total" words section to highlight each distinct part of the receipt
            label = row["class"]
            important_total_word = {
                "words": total_words,
                "label": label
                }
        elif "date" in row["class"].lower():
            coordinates = {
                "xmin": row["xmin"],
                "ymin": row["ymin"],
                "xmax": row["xmax"],
                "ymax": row["ymax"]
                }
        # Create "date" words section to join coordinate with the important block of text                 
            important_info = row["text"]
            word = {
                "Coordinates": coordinates,
                "Text": important_info
                }
            date_words.append(word)
        # Create important "date" words section to highlight each distinct part of the receipt
            label = row["class"]
            important_date_word = {
                "words": date_words,
                "label": label
                }

    try:
        important_words.append(important_total_word)
    except:
        pass
    try:
        important_words.append(important_date_word)
    except:
        pass
    
    # Put together all important parts
    total_bboxes = []
    date_bboxes = []
        
    for _index, row in image_data.iterrows():  
        if "total" in row["class"].lower():
            total_bbox = {
                "xmin": row["xmin"],
                "ymin": row["ymin"],
                "xmax": row["xmax"],
                "ymax": row["ymax"]
                }
            total_bboxes.append(total_bbox)
        elif "date" in row["class"].lower():
            date_bbox = {
                "xmin": row["xmin"],
                "ymin": row["ymin"],
                "xmax": row["xmax"],
                "ymax": row["ymax"]
                }
            date_bboxes.append(date_bbox)
    
    # Build output JSON
    output = {
    "image_path": image_path,
    "info_json_path": info_json_path,
    "important_words": important_words,
    "total": total_bboxes,
    "date": date_bboxes,
    }
    
    return output