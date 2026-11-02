import os
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image as PILImage

from constants import IMAGES_DIR
from process import process_receipt

def display_image(image_container, image_file, filename):
    """App display and button functionality."""
    image_container.image(image_file, caption = filename)

def select_random_receipt(image_container, text_container, progress_container, success_container):
    # Get a list of all image files for users to pull from
    image_files = [file for file in os.listdir(IMAGES_DIR) if file.endswith('.jpg')]

    # Get random image file from available selection
    random_images = random.sample(image_files, 1)

    for image_file in random_images:
        image_path = Path(IMAGES_DIR, image_file)
        image_preview = cv2.imread(image_path)
        display_image(image_container, image_preview, image_file)
        try:
            process_receipt(image_container, text_container, progress_container, success_container, image_preview, image_file)
        except:
            text_container.write("An error was encountered with this image, please select a new file")


def use_uploaded_receipt(image_container, text_container, progress_container, success_container, uploaded_file):
    normalized_file = PILImage.open(uploaded_file)
    uploaded_filename = uploaded_file.name
    display_image(image_container, normalized_file, uploaded_filename)
    try:
        process_receipt(image_container, text_container, progress_container, success_container, np.array(normalized_file), uploaded_filename)
    except:
        text_container.write("An error was encountered with this image, please select a new file")

