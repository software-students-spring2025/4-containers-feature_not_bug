"""
This module processes receipt images, extracts text with pytesseract, 
and parses dish names with corresponding prices.
"""

import re
import cv2
import pytesseract

def process_image(raw_img):
    """Convert the input image to grayscale for better OCR performance."""
    processed_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY) # pylint: disable=no-member

    return processed_img

def sanitize_string(dish):
    """"Remove unnecessary characters from dish name"""
    index_start = 0
    while not dish[index_start].isalpha():
        index_start += 1

    index_end = -1
    while not dish[index_end].isalpha():
        index_end -= 1

    # Adjust end index if there is no invalid characters at the end of string
    if index_end == -1:
        return dish[index_start:len(dish)]

    return dish[index_start:index_end + 1]

# Parse lines from text
def parse_processed_lines(lines):
    """"Separate and parse dishes and prices from lines"""
    pattern = re.compile(r'([\d]+[,.][\d]{2})\s*$')
    entries = []

    for line in lines:
        match = pattern.search(line)
        if match:
            price_string = match.group(1).replace(",", ".") # Replace , with .
            try:
                price_float = float(price_string)
            except ValueError:
                continue

            dish = line[:match.start()].strip() # Extract dish for each price
            if dish:
                dish = sanitize_string(dish)

                entries.append({"dish": dish, "price": price_float})

    return entries

# img = cv2.imread(r"IMG_2437.png") # Receipt taken from camera
img = cv2.imread(r"test-receipt_2.jpg") # pylint: disable=no-member

processed_text = pytesseract.image_to_string(process_image(img))
processed_lines = parse_processed_lines(processed_text.splitlines())

print(processed_lines)
