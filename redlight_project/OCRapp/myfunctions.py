import cv2
import easyocr
import imutils
import string
import re

reader = easyocr.Reader(['en'])

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def preprocessimg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    gray = cv2.medianBlur(gray, 3)
    # perform otsu thresh (using binary inverse since opencv contours work better with white text)
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
    roi = cv2.bitwise_not(dilation)
    return roi


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    if len(text) != 10:
        return False

    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()) and \
       (text[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[7] in dict_char_to_int.keys()) and \
       (text[8] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[8] in dict_char_to_int.keys()) and \
       (text[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[9] in dict_char_to_int.keys()):

        return True

    else:
        return False


def retain_alphanumeric(text):
    # Use regular expression to keep only alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9]', '', text)


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char,2: dict_char_to_int, 3: dict_char_to_int ,  4: dict_int_to_char, 5: dict_int_to_char, 6: dict_char_to_int,
               7: dict_char_to_int, 8: dict_char_to_int , 9:dict_char_to_int }
    for j in [0, 1, 2, 3, 4, 5, 6 , 8, 9]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

def clean_text(result):

    raw_string = ""
    for detection in result:
        bbox, text, score = detection
        raw_string += text

    return retain_alphanumeric(raw_string)


def extract_plate(img):
    final = preprocessimg(img)
    detections = reader.readtext(final)

    cleantxt = clean_text(detections)

    if license_complies_format(cleantxt):
        final_txt = format_license(cleantxt)
        return final_txt

    else: 
        return None

