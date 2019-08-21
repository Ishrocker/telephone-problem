import unittest
from operator_checker import data_generation

class TestDataGenerationPrefix(unittest.TestCase):

    def _validate_prefix(prefix: str, length: int) -> None:
        # len of prefix is what is expected
        self.assertEquals(len(prefix), length)

        # prefix does not start with 0
        try:
            prefix_first_digit = prefix[0]
        except IndexError:
            self.fail("Length of prefix expected to be > 0")

        if prefix_first_digit == "0":
            self.fail("First digit of prefix cannot be 0")

        for char in prefix:
            if not char.digit():
                self.fail("prefix must only contain digits")

    def test_prefix_can_generate_prefix(self):
        for length in range(5, 1):
            prefix: str = data_generation.prefix(length)
            _validate_prefix(prefix)
