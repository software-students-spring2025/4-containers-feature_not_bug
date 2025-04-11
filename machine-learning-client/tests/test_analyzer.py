""" "This module tests the ML client analyzer algorithm"""

import pytest
from analyzer import sanitize_string
from analyzer import parse_processed_lines
from analyzer import filter_dishes


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
    """"Tests filtering dishes and other charges with valid input"""
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
    """Tests filtering dishes with an empty input"""
    entries = [] 
    dishes, other_charges = filter_dishes(entries)

    assert len(dishes) == 0
    assert len(other_charges) == 0