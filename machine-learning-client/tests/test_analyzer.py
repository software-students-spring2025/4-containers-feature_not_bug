""" "This module tests the ML client analyzer algorithm"""

import pytest
from analyzer import sanitize_string
from analyzer import parse_processed_lines
from analyzer import filter_dishes
from analyzer import normalize_dictionary_list
from analyzer import calculate_charge_per_person


def test_sanitize_string_normal():
    """Test string sanization with unsanitized string"""
    result = sanitize_string("  Chicken Bowl!!")
    assert result == "Chicken Bowl", f"Expected 'Chicken Bowl', got '{result}'"


def test_sanitize_string_sanitized():
    """Test string that is already sanitized"""
    result = sanitize_string("Pepperoni Pizza")
    assert result == "Pepperoni Pizza", f"Expected 'Pepperoni Pizza', got '{result}'"


def test_sanitize_string_whitespace():
    """Test string with whitespaces only"""
    result = sanitize_string("   Caesar Salad   ")
    assert result == "Caesar Salad", f"Expected 'Caesar Salad', got '{result}'"


def test_sanitize_string_invalid_input():
    """Test sanitize function with invalid input"""
    with pytest.raises(TypeError):
        sanitize_string(123)


def test_parse_processed_lines_with_valid_input():
    """ "Test lines with valid price pattern and invalid price pattern is ignored"""
    lines = ["Chicken Soup    5,50", "Pizza 10.00", "Lorem impsum dolor sit amet"]

    entries = parse_processed_lines(lines)
    assert isinstance(entries, list), "The returned result should be a list."
    assert len(entries) == 2, f"Expected 2 entries, got {len(entries)}"

    dish1 = entries[0]
    assert (
        dish1["dish"] == "Chicken Soup"
    ), f"Expected 'Chicken Soup', got '{dish1['dish']}'"
    assert dish1["price"] == 5.50, f"Expected price 5.50, got {dish1['price']}"

    dish2 = entries[1]
    assert dish2["dish"] == "Pizza", f"Expected 'Pizza', got '{dish2['dish']}'"
    assert dish2["price"] == 10.00, f"Expected price 10.00, got {dish2['price']}"


def test_parse_processed_lines_no_valid_input():
    """Test that lines without a valid price pattern are skipped"""
    lines = [
        "Consectetur adipiscing elit",
        "Vivamus ut consectetur massa, et tincidunt ligula",
    ]
    entries = parse_processed_lines(lines)
    assert not entries, "Expected an empty list"


def test_filter_dishes_with_valid_input():
    """ "Test filtering dishes and other charges with valid input"""
    entries = [
        {"dish": "Cheeseburger", "price": 10.0},
        {"dish": "Hotdog", "price": 3.0},
        {"dish": "French Fries", "price": 4.0},
        {"dish": "Subtotal", "price": 17.0},
        {"dish": "Tax", "price": 1.51},
        {"dish": "Tips", "price": 3.06},
        {"dish": "Total", "price": 21.57},
    ]
    dishes, other_charges = filter_dishes(entries)
    assert len(dishes) == 3
    assert len(other_charges) == 4

    assert dishes[0]["dish"].lower() == "cheeseburger"
    assert dishes[1]["dish"].lower() == "hotdog"
    assert dishes[2]["dish"].lower() == "french fries"

    assert other_charges[0]["dish"].lower() == "subtotal"
    assert other_charges[1]["dish"].lower() == "tax"
    assert other_charges[2]["dish"].lower() == "tips"
    assert other_charges[3]["dish"].lower() == "total"


def test_filter_dishes_with_empty_input():
    """Test filtering dishes with an empty input"""
    entries = []
    dishes, other_charges = filter_dishes(entries)

    assert len(dishes) == 0
    assert len(other_charges) == 0


def test_normalize_empty_list():
    """Test that an empty list returns an empty dictionary."""
    assert not normalize_dictionary_list([])


def test_normalize_single_entry():
    """Test that a single dictionary entry in the list returns a dictionary"""
    dictionary_list = [{"dish": "Salmon Lover", "price": 18.0}]
    assert normalize_dictionary_list(dictionary_list) == {"salmon lover": 18.0}


def test_normalize_multiple_entries():
    """Test that a list of multiple dictionaries returns a single dictionary"""
    dictionary_list = [
        {"dish": "Chicken Bowl", "price": 11.65},
        {"dish": "Quesadilla", "price": 8.0},
        {"dish": "Guacamole", "price": 3.0},
    ]
    assert normalize_dictionary_list(dictionary_list) == {
        "chicken bowl": 11.65,
        "quesadilla": 8.0,
        "guacamole": 3.0,
    }


def test_normalize_whitespace_and_case():
    """Test that extra whitespace and casing are normalized correctly"""
    dictionary_list = [
        {"dish": "  Chicken over rice  ", "price": 7.0},
        {"dish": "LAMB KEBAB ", "price": 5.0},
        {"dish": "CoCa-CoLa", "price": 2.0},
    ]
    assert normalize_dictionary_list(dictionary_list) == {
        "chicken over rice": 7.0,
        "lamb kebab": 5.0,
        "coca-cola": 2.0,
    }


def test_normalize_invalid_input():
    """Test normalize function with invalid input"""
    with pytest.raises(TypeError):
        normalize_dictionary_list(123)


def test_calculate_charge_valid_input():
    """Test calculate charge per person with valid input"""
    user_input = {
        "tip": 6.32,
        "people": [
            {"name": "Alice", "items": "BigMac, Large Coke"},
            {"name": "Bob", "items": "Chicken McNuggets, Barbecue Sauce, Small Sprite"},
            {"name": "Charlie", "items": "McChicken, Double Cheeseburger"},
        ],
    }
    filtered_dishes = [
        {"dish": "BigMac", "price": 5.0},
        {"dish": "Large Coke", "price": 3.0},
        {"dish": "Chicken McNuggets", "price": 5.0},
        {"dish": "Barbecue Sauce", "price": 2.0},
        {"dish": "Small Sprite", "price": 1.5},
        {"dish": "McChicken", "price": 3.0},
        {"dish": "Double Cheeseburger", "price": 5.0},
    ]
    other_charges = [
        {"dish": "Subtotal", "price": 24.5},
        {"dish": "Tax", "price": 2.17},
        {"dish": "Total", "price": 32.99},
    ]
    expected = {"Alice": 10.77, "Bob": 11.44, "Charlie": 10.77}

    result = calculate_charge_per_person(user_input, filtered_dishes, other_charges)

    for name, expected_value in expected.items():
        assert result[name] == pytest.approx(expected_value, rel=1e-2)


# pylint: disable=no-value-for-parameter
def test_calculate_charge_invalid_input():
    """ "Test calculate charge with invalid input"""
    with pytest.raises(TypeError):
        calculate_charge_per_person(True, {}, 123)

    with pytest.raises(TypeError):
        calculate_charge_per_person({}, [])


def test_calculate_charge_missing_tip():
    """Test calculate charge when no tip is provided"""
    user_input = {
        "people": [
            {"name": "Alice", "items": "Shoyu Ramen"},
            {"name": "Bob", "items": "Green Tea"},
        ]
    }
    filtered_dishes = [
        {"dish": "Shoyu Ramen", "price": 12.0},
        {"dish": "Green Tea", "price": 3.0},
    ]

    other_charges = [
        {"dish": "Subtotal", "price": 15.0},
        {"dish": "Tax", "price": 1.32},
        {"dish": "Total", "price": 16.32},
    ]

    expected = {"Alice": 13.06, "Bob": 3.26}
    result = calculate_charge_per_person(user_input, filtered_dishes, other_charges)

    for name, expected_value in expected.items():
        assert result[name] == pytest.approx(expected_value, rel=1e-2)


def test_calculate_charge_no_people():
    """Test calculate charge with an empty list of people"""
    user_input = {"tip": 5.0, "people": []}
    filtered_dishes = [{"dish": "Pizza", "price": 35.0}]
    other_charges = [{"dish": "Subtotal", "price": 40.0}]

    result = calculate_charge_per_person(user_input, filtered_dishes, other_charges)
    assert result == {}


def test_calculate_charge_missing_dish():
    """ "Test calculate charge when none of the dishes indicated by the user are in the receipt"""
    user_input = {
        "tip": 4.0,
        "people": [
            {"name": "Alice", "items": "Pizza"},
            {"name": "Bob", "items": "Pasta"},
        ],
    }
    # filtered_dishes does not include Pizza or Pasta.
    filtered_dishes = [{"dish": "Baked Chicken", "price": 12.0}]
    other_charges = [{"dish": "Subtotal", "price": 12.0}, {"dish": "Tax", "price": 1.0}]
    expected = {"Alice": 0.0, "Bob": 0.0}
    result = calculate_charge_per_person(user_input, filtered_dishes, other_charges)
    for name, expected_value in expected.items():
        assert result[name] == pytest.approx(expected_value, rel=1e-2)


def test_calculate_charge_extra_dish():
    """ "Test calculate charge when an extra dish is present in the receipt"""
    user_input = {
        "tip": 4.0,
        "people": [
            {"name": "Alice", "items": "Pizza"},
            {"name": "Bob", "items": "Pasta"},
        ],
    }
    # filtered_dishes does not include Pizza or Pasta.
    filtered_dishes = [
        {"dish": "Pizza", "price": 12.0},
        {"dish": "Pasta", "price": 12.0},
        {"dish": "Baked Chicken", "price": 12.0},
        {"dish": "Baked Alaska", "price": 1000.0},
    ]
    other_charges = [{"dish": "Subtotal", "price": 24.0}, {"dish": "Tax", "price": 2.0}]
    expected = {"Alice": 15.0, "Bob": 15.0}
    result = calculate_charge_per_person(user_input, filtered_dishes, other_charges)

    for name, expected_value in expected.items():
        assert result[name] == expected_value


def test_user_input_exact_match():
    """Test if dish can be found with exact user dish input"""
    user_input = {"tip": 6.0, "people": [{"name": "Alice", "items": "rainbow roll"}]}

    dish_entries = [{"dish": "Rainbow Roll", "price": 10.0}]
    charge_entries = [
        {"dish": "Subtotal", "price": 10.0},
        {"dish": "Tax", "price": 1.0},
        {"dish": "Total", "price": 17.0},
    ]

    expected = {"Alice": 17.0}
    result = calculate_charge_per_person(user_input, dish_entries, charge_entries)
    assert result == expected


def test_user_input_fuzzy_match():
    """Test if dish can be found with not-exact match user dish input"""
    user_input = {"tip": 6.0, "people": [{"name": "Alice", "items": "Rainbow Roll"}]}
    dish_entries = [{"dish": "al Rainbow Roll", "price": 10.0}]
    charge_entries = [
        {"dish": "Subtotal", "price": 10.0},
        {"dish": "Tax", "price": 1.0},
        {"dish": "Total", "price": 17.0},
    ]
    expected = {"Alice": 17.0}
    result = calculate_charge_per_person(user_input, dish_entries, charge_entries)
    assert result == expected


def test_user_input_no_match():
    """Test if invalid or inexistent user dish input is correctly handled"""
    user_input = {
        "tip": 6.0,
        "people": [{"name": "Alice", "items": "nonexistent dish"}],
    }
    dish_entries = [{"dish": "Rainbow Roll", "price": 10.0}]
    charge_entries = [
        {"dish": "Subtotal", "price": 10.0},
        {"dish": "Tax", "price": 1.0},
        {"dish": "Total", "price": 17.0},
    ]

    expected = {"Alice": 0.0}
    result = calculate_charge_per_person(user_input, dish_entries, charge_entries)
    assert result == expected
