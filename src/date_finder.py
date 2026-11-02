import re
from dateutil.parser import parse

from dateparser.search import search_dates

from constants import EXCLUDED_DATE_TEXTS, INCLUDE_TOTAL_TEXTS, EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS, DATE_TEXT_MUST_INCLUDE, DATE_TEXT_MIGHT_INCLUDE

# Define constants 
PROBABLE_DATE_FORMAT = r'(\b\d{2}\b|\b\d{4}\b)'+r'[\-\.\,\:\/\{\}\_]'+r'(\b\d{2}\b)'+r'[\-\.\,\:\/\{\}\_]'+r'(\b\d{2}\b|\b\d{4}\b)'

def parse_date (string, confirmed_dates):
    """Review strings identified by the OCR and assess if they are likely to be dates."""
    confirmed_date = parse(string, fuzzy=True)
    confirmed_dates.append(confirmed_date)

def confirm_potential_date (string, confirmed_dates, indices_of_non_dates):
    potential_dates = []
    split_strings = string.split(' ')

    for item in split_strings:
        search_results = search_dates(item)
        if search_results is not None:
            potential_dates.append(search_results)

    potential_dates_str = str(potential_dates)

    potential_dates_split = potential_dates_str.split('],')
    for potential_date in potential_dates_split:
        if any(excluded_word.lower() in potential_date.lower() for excluded_word in EXCLUDED_DATE_TEXTS) or any(excluded_word in potential_date.lower() for excluded_word in INCLUDE_TOTAL_TEXTS) or any(excluded_word in potential_date.lower() for excluded_word in EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS):
            indices_of_non_dates.append(potential_dates_split.index(potential_date))
        else:
            if (potential_dates_split.index(potential_date)- 1) in indices_of_non_dates:
                continue
            else:
                try:
                    parse_date (potential_date, confirmed_dates)
                except:
                    potential_date_stripped = potential_date[potential_date.find('[('):]
                    potential_date_stripped = potential_date_stripped.split(']]')[0] + ']'
                    potential_date_orig_input = potential_date_stripped.split("'")[1]     

                    if re.match(r'[^A-Za-z0-9\-\.\,\:\/\{\}\_\s]', potential_date_orig_input):
                        continue
                    else:
                        if any(excluded_word.lower() in potential_date_orig_input.lower() for excluded_word in EXCLUDED_DATE_TEXTS) or any(excluded_word in potential_date.lower() for excluded_word in INCLUDE_TOTAL_TEXTS) or any(excluded_word in potential_date.lower() for excluded_word in EXCLUDED_TOTAL_TEXTS_FOR_AMOUNT_CLASS):
                            continue
                        else:
                            try:
                                parse_date (potential_date_orig_input, confirmed_dates)
                            except:
                                continue
    
def date_too_long(string):
    return any(float(object) > 60 for object in re.findall(r'\b\d{2}\b', string)) or any(float(object) > 2099 for object in re.findall(r'\b\d{4}\b', string))
 
def check_if_date(string):
    confirmed_dates = []
    indices_of_non_dates = []
    
    if any(excluded_word.lower() in string.lower() for excluded_word in EXCLUDED_DATE_TEXTS):
        pass
    elif re.search(PROBABLE_DATE_FORMAT, string):
        if date_too_long(string):
            pass
        else:
            try:
                parse_date(string, confirmed_dates)
            except:
                confirm_potential_date(string, confirmed_dates, indices_of_non_dates)
    elif any(needed_word.lower() in string.lower() for needed_word in DATE_TEXT_MUST_INCLUDE):
        if date_too_long(string):
            pass
        else:
            try:
                confirm_potential_date(string, confirmed_dates, indices_of_non_dates)
            except:
                pass
    elif re.search(r'[A-Za-z]', string) and re.search(r'^[AM|PM|am|pm]', string) or re.search(r'\b\d{3}\b|\b\d{5}\b', string) or (sum(character.isdigit() for character in string) < sum(character.isalpha() for character in string)):
        pass
    else:
        if re.search(r'(\d)'+r'[\-\.\,\:\/\{\}\_]'+r'(\d)', string):
            if date_too_long(string):
                pass
            else:
                try:
                    confirm_potential_date (string, confirmed_dates, indices_of_non_dates)
                except:
                    pass     
        elif any(needed_word.lower() in string.lower() for needed_word in DATE_TEXT_MIGHT_INCLUDE):
                if date_too_long(string):
                    pass
                else:
                    try:
                        confirm_potential_date (string, confirmed_dates, indices_of_non_dates)
                    except:
                        pass   

    return confirmed_dates
