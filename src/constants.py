from pathlib import Path

# Define input paths
PROJECT_ROOT = Path(Path.cwd())
INPUT_DIR = Path(PROJECT_ROOT, 'data/input')
IMAGES_DIR = Path(INPUT_DIR, 'jpg')
JSON_DIR = Path(INPUT_DIR, 'json')

# Define output paths
WORKING_DIR = Path(INPUT_DIR, 'output')
OUTPUT_DIR = Path(PROJECT_ROOT, 'data/output')
OUTPUT_CSV_FILE_PATH = Path(OUTPUT_DIR, 'annotations.csv')
OUTPUT_JSON_DIR = Path(OUTPUT_DIR, 'json')
OUTPUT_IMAGES_DIR = Path(OUTPUT_DIR, 'annotated_images')

# Classes to be identified from the receipt
ALLOWED_CLASSES = [
    'date',
    'potential datetime',
    'total',
    'amount'
    ]

# Words that should be highlighted from the receipt
INCLUDE_TOTAL_TEXTS = [
    'total',
    'tot',
    'amount',
    'amt'
    ]
INCLUDE_DATE_TEXTS = [
    'date',
    'time',
    ]

# Words that must be included if a date is not exclusively integers 
DATE_TEXT_MUST_INCLUDE = [
    'year',
    'month',
    'day',
    'date',
    'time',
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',
    ]
DATE_TEXT_MIGHT_INCLUDE = [
    'am',
    'pm',
    'jan',
    'feb',
    'mar',
    'apr',
    'aug',
    'sept',
    'sep',
    'oct',
    'nov',
    'dec',
    '/',
    '-',
    '.',
    ',',
    ':',
    ';'
    ]

# Words that should not be considered when identifying important information from the receipt
EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS = [
    'total tax',
    'total gst',
    'total saving',
    'total savings',
    'total quantity',
    'total qty',
    'total items',
    'discount',
    'round',
    'change'
    ]
EXCLUDED_DATE_TEXTS = [
    'telephone',
    'tel',
    'fax',
    'email',
    'address',
    'number',
    'no.',
    'no',
    '#',
    'order',
    'ord',
    'id',
    'code',
    'account',
    'acc',
    'rm',
    'invoice',
    '$',
    'change',
    'cash',
    'credit'
    ]

# Highlight colors to annotate image
COLORS = [
    'red',
    'orange',
    'blue',
    'green'
] 

# Assign color to each class
COLOR_MAP = {}
for i, label in enumerate(ALLOWED_CLASSES):
    COLOR_MAP[label] = COLORS[i] if i < len(COLORS) else 'yellow'