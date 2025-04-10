import pytest
from analyzer import sanitize_string
from analyzer import parse_processed_lines

def test_sanitize_string_normal():
    result = sanitize_string(" 123Chicken Bowl!!")
    assert result == "Chicken Bowl", f"Expected 'Chicken Soup', got '{result}'"

def test_sanitize_string_sanitized():
    result = sanitize_string("Pepperoni Pizza")
    assert result == "Pepperoni Pizza", f"Expected 'Pepperoni Pizza', got '{result}'"

def test_sanitize_string_whitespace():
    result = sanitize_string("   Caesar Salad   ")
    assert result == "Caesar Salad", f"Expected 'Caesar Salad', got '{result}'"

def test_sanitize_string_invalid_input():
    with pytest.raises(TypeError):
        result = sanitize_string(123)

def test_parse_processed_lines_with_valid_input():
    lines = [
        "Chicken Soup    5,50",
        "Pizza 10.00",
        "Lorem impsum dolor sit amet"
    ]

    entries = parse_processed_lines(lines)
    assert isinstance(entries, list), "The returned result should be a list."
    assert len(entries) == 2, f"Expected 2 entries, got {len(entries)}"

    dish1 = entries[0]
    assert dish1["dish"] == "Chicken Soup", f"Expected 'Chicken Soup', got '{dish1['dish']}'"
    assert dish1["price"] == 5.50, f"Expected price 5.50, got {dish1['price']}"

    dish2 = entries[1]
    assert dish2["dish"] == "Pizza", f"Expected 'Pizza', got '{dish2['dish']}'"
    assert dish2["price"] == 10.00, f"Expected price 10.00, got {dish2['price']}"

def test_parse_processed_lines_no_valid_input():
    # Test that lines without a valid price pattern are skipped.
    lines = [
        "Consectetur adipiscing elit",
        "Vivamus ut consectetur massa, et tincidunt ligula"
    ]
    entries = parse_processed_lines(lines)
    assert entries == [], "Expected an empty list"