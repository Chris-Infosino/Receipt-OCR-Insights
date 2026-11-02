from PIL import Image as PILImage, ImageDraw

from constants import COLOR_MAP

def draw_annotations(image_to_annotate, annotations):
    """Visually highlight items of note on the receipt."""
    image_annotation = PILImage.fromarray(image_to_annotate)
    draw = ImageDraw.Draw(image_annotation)

    for _, ann in annotations.iterrows(): 
        xmin, ymin, xmax, ymax = ann['xmin'], ann['ymin'], ann['xmax'], ann['ymax']
        label = ann['class']
        color = COLOR_MAP.get(label, 'yellow') 
        
        # Draw rectangle over important text
        draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=3)
        
        # Draw label for important text
        text_bbox = draw.textbbox((xmin, ymin), label)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1] + 8
        
        # Draw background for text to ensure readability
        draw.rectangle([xmin, ymin - text_height, xmin + text_width, ymin], fill=color)
        draw.text((xmin, ymin - text_height), label, fill='white')

    return image_annotation
