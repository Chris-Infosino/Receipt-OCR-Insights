import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from reader import extract_text
from draw import draw_annotations
from annotate import create_csv, get_json_details, create_json_file
from constants import OUTPUT_CSV_FILE_PATH, OUTPUT_JSON_DIR, OUTPUT_IMAGES_DIR

def process_receipt(image_container, text_container, progress_container, success_container, file_to_process, filename):
    """Core process to analyze receipt, annotate important information, and provide user feedback."""
    
    text_container.update(label="Processing image", state="running", expanded=True)
    progress_container.progress(10)
    
    text_container.write("Extracting text from image")
    progress_container.progress(20)
    extracted_data = extract_text(file_to_process, filename)
    
    text_container.write("Identifying key information from image")
    progress_container.progress(50)
    create_csv(extracted_data)

    # Read the annotations CSV file
    annotations_df = pd.read_csv(OUTPUT_CSV_FILE_PATH)

    result = []

    text_container.write("Creating JSON for image")
    progress_container.progress(65)
    result = get_json_details(filename, annotations_df) 
    create_json_file(result, OUTPUT_JSON_DIR, filename)

    # Extract annotations for the current image
    annotations = annotations_df[annotations_df['filename'] == filename]
            
    # Draw annotations on image
    text_container.write("Annotating image")
    progress_container.progress(80)
    annotated_image = draw_annotations(file_to_process, annotations)
        
    # Display and save the image with annotations
    plt.figure(figsize=(10, 10))
    plt.imshow(np.array(annotated_image))
    plt.axis('off')
    plt.title(filename)
    plt.savefig(Path(OUTPUT_IMAGES_DIR,f'annotated_{filename}'))
    
    text_container.update(label="Receipt processing complete", state="complete")
    progress_container.progress(100)
    image_container.image(annotated_image, caption=filename)
    progress_container.empty()
    
    success_container.success("Thank you for your attention, I hope you liked my project and app!")
    
    return annotated_image