"""
This module processes receipt images, extracts text with pytesseract,
and parses dish names with corresponding prices.
"""

# pylint: disable=no-member

import re
import cv2
import pytesseract


def process_image(raw_img):
    """Convert the input image to grayscale for better OCR performance."""
    processed_img = cv2.cvtColor(
        raw_img, cv2.COLOR_BGR2GRAY
    )  # pylint: disable=no-member

    return processed_img


def sanitize_string(dish):
    """Remove unnecessary characters from dish name"""
    index_start = 0
    while not dish[index_start].isalnum():
        index_start += 1

    index_end = -1
    while not dish[index_end].isalpha():
        index_end -= 1

    # Adjust end index if there is no invalid characters at the end of string
    if index_end == -1:
        return dish[index_start : len(dish)]

    return dish[index_start : index_end + 1]


def filter_dishes(entries):
    """Filter dishes from subtotal, tax, tips, grand total, and other charges"""
    keywords = [
        "subtotal",
        "sub-total",
        "tax",
        "tip",
        "tips",
        "service",
        "charge",
        "card",
        "fee",
        "total",
    ]
    dishes = []
    charges = []

    for item in entries:
        dish_name = item["dish"].strip().lower()
        if not any(keyword in dish_name for keyword in keywords):
            dishes.append(item)
        else:
            charges.append(item)

    return dishes, charges


def parse_processed_lines(lines):
    """Separate and parse dishes and prices from lines"""
    pattern = re.compile(r"([\d]+[,.][\d]{2})\s*$")
    entries = []

    for line in lines:
        match = pattern.search(line)
        if match:
            price_string = match.group(1).replace(",", ".")  # Replace , with .
            try:
                price_float = float(price_string)
            except ValueError:
                continue

            dish = line[: match.start()].strip()  # Extract dish for each price
            if dish:
                dish = sanitize_string(dish)

                entries.append({"dish": dish, "price": price_float})

    return entries


def normalize_dictionary_list(dictionary_list):
    """Converts a list of dictionaries into a single dictionary"""
    dictionary = {}
    for entry in dictionary_list:
        key = entry["dish"].strip().lower()
        dictionary[key] = entry["price"]
    return dictionary


# user_input data format:
# user_input = {
#   "receipt": (img),
#   "tip": (float),
#   "num-people": (int),
#   "people": [{"name": "", "items": ""}, ...]
# }
def calculate_charge_per_person(
    user_input, dish_entries, charge_entries
):  # pylint: disable=too-many-locals
    """Calculate the total amount per person according to the provided bill"""
    # Convert charge_entries and dish_prices list of dictionaries into a single dictionary
    charges_dict = normalize_dictionary_list(charge_entries)
    dish_prices = normalize_dictionary_list(dish_entries)

    # Get the subtotal and tax from the receipt
    subtotal_from_receipt = charges_dict.get("subtotal")
    tax_from_receipt = charges_dict.get("tax")

    # Extract tip from user input
    tip = user_input.get("tip", 0.0)

    # Get the list of people ordering
    people = user_input.get("people", [])

    # Build a mapping of dishes to the list of people who ordered them
    dish_consumers = {}
    for person in people:
        name = person["name"]
        # Convert the comma-separated items into a list of normalized dish names
        items_list = [
            item.strip().lower() for item in person.get("items", "").split(",")
        ]
        for dish in items_list:
            if dish not in dish_consumers:
                dish_consumers[dish] = []
            dish_consumers[dish].append(name)

    # Initialize base total for each person
    person_totals = {person["name"]: 0.0 for person in people}

    # For each dish that people ordered, add its cost share to each person who had the dish
    for dish, consumers in dish_consumers.items():
        if dish in dish_prices:
            price = dish_prices[dish]
            split_price = price / len(consumers)
            for name in consumers:
                person_totals[name] += split_price

    # Calculate each person's share of the tip and tax proportionally
    for name in person_totals:
        base = person_totals[name]
        # Initialize tip_share and tax_share (linting)
        tip_share = 0.0
        tax_share = 0.0
        if subtotal_from_receipt is not None and subtotal_from_receipt > 0:
            tip_share = (base / subtotal_from_receipt) * tip
            tax_share = (base / subtotal_from_receipt) * tax_from_receipt
        person_totals[name] = round(base + tip_share + tax_share, 2)

    return person_totals


# def store_receipt_in_db(receipt_img):


# img = cv2.imread(r"IMG_2437.png") # Receipt taken from camera
img = cv2.imread(r"test-receipt_2.jpg")  # pylint: disable=no-member

processed_text = pytesseract.image_to_string(process_image(img))
processed_lines = parse_processed_lines(processed_text.splitlines())

filtered_dishes, other_charges = filter_dishes(processed_lines)
