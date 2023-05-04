from project import base_currency, convert, balance
# use mock unittesting in order to test user input
# https://forum.learncodethehardway.com/t/testing-input-and-print/1757/2
from unittest import mock

# Test will fail as exchange rates change
# Date of latest tests
# 2/23/2023
def main():
    test_convert()

def test_base_currency():
    # return_value == user_input
    with mock.patch("builtins.input", return_value="USD"):
        assert base_currency() == "USD"
    with mock.patch("builtins.input", return_value="BOB"):
        assert base_currency() == "BOB"

def test_convert():
    # return_value == user_input
    # Convert argument currency to user_input by returning rate
    with mock.patch("builtins.input", return_value="EUR"):
        assert convert("USD") == ["EUR", 0.942]
    with mock.patch("builtins.input", return_value="USD"):
        assert convert("BOB") == ["USD", 0.144]
    with mock.patch("builtins.input", return_value="SRD"):
        assert convert("BMD") == ["SRD", 33.24]
    with mock.patch("builtins.input", return_value="USD"):
        assert convert("USD") == ["USD", 1]

def test_balance():
    # Use rate received from currency conversion
    # Apply rate to amount entered by user_input
    with mock.patch("builtins.input", return_value="50"):
        assert balance(0.942) == ["50", 47.1]
    with mock.patch("builtins.input", return_value="100"):
        assert balance(0.144) == ["100", 14.4]
    with mock.patch("builtins.input", return_value="10"):
        assert balance(33.24) == ["10", 332.4]
if __name__ == "__main__":
    main()