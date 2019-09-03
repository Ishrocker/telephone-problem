import unittest
from decimal import Decimal
from operator_checker.models import Operator, PrefixCache


class TestOperator(unittest.TestCase):
    def setUp(self):
        self.operator = Operator(
            name="Verison",
            rates={
                "415": Decimal("1.00"),
                "512": Decimal("1.01")
            }
        )

    def test_operator_has_correct_types(self):
        self.assertIsInstance(self.operator, Operator)
        self.assertIsInstance(self.operator.name, str)
        self.assertIsInstance(self.operator.rates, dict)
    
    def test_bad_operator_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            Operator(
                name=415,
                rates={
                    "512": Decimal("1.01"),
                }
            )

    def test_bad_operator_rate_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            Operator(
                name="Verizon",
                rates={
                    512: Decimal("1.01"),
                }
            )

    def test_bad_operator_rate_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Operator(
                name="Verizon",
                rates={
                    "415": 1.01,
                }
            )

    def test_price_for_prefix_returns_price(self):
        expected_price = Decimal("1.00")
        price = self.operator.price_for_prefix("415")
        self.assertEqual(price, expected_price)

    def test_price_for_prefix_returns_none_on_missing_key(self):
        expected_price = None
        price = self.operator.price_for_prefix("72")
        self.assertEqual(price, expected_price)


    def test_has_better_price_for_prefix(self):
        self.assertFalse(
            self.operator.has_better_price_for_prefix(
                prefix="415",
                price=Decimal(".99")
            )
        )        
        self.assertTrue(
            self.operator.has_better_price_for_prefix(
                prefix="415",
                price=Decimal("1.01")
            )
        )

    def test_bad_prefix_for_has_better_price_for_prefix_raises_error(self):
        with self.assertRaises(TypeError):
            self.operator.has_better_price_for_prefix(
                prefix="415",
                price="1.00"
            )

    def test_bad_prefix_type_for_price_for_prefix_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.operator.price_for_prefix(prefix=415)

    def test_bad_prefix_value_for_price_for_prefix_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.operator.price_for_prefix(prefix="bad")

    def test_bad_type_for_operator_rates_raise_type_error(self):
        with self.assertRaises(TypeError):
            Operator(
                name="Verizon",
                rates=None
            )


class TestPrefixCache(unittest.TestCase):
    def setUp(self):
        self.cache = PrefixCache()
        self.cache.data.update({  # noqa
            "415": Operator(
                name="AT&T",
                rates={
                    "415": Decimal("1.00")
                }
            ),
            "512": Operator(
                name="Verizon",
                rates={
                    "512": Decimal("1.00")
                }
            ),
            "599": Operator(
                name="Sprint",
                rates={
                    "415": Decimal("1.00")
                }
            )
        })

    def test_prefix_cache_defaults_to_empty_dict(self):
        cache = PrefixCache()
        self.assertIsInstance(cache.data, dict)
        self.assertEqual(cache.data, {})
    
    def test_can_find_prefix(self):
        prefix = self.cache.find("415")
        self.assertIsInstance(prefix, str)
        self.assertEqual(prefix, "415")

    def test_find_returns_none_if_not_found(self):
        prefix = self.cache.find("Not a valid string")
        self.assertEqual(prefix, None)

    def test_can_update_with_operator(self):
        operator = Operator(
            name="Tele2",
            rates={
                "415": Decimal("0.99")
            }
        )
        self.cache.update_with_operator(operator)
        operator_cached = self.cache.data.get("415")  # noqa
        self.assertEqual(operator, operator_cached)

    def test_bad_operator_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.cache.update_with_operator(operator="bad value")

    def test_can_lookup_prefix(self):
        found_operator = self.cache.lookup("415")
        self.assertEqual(found_operator, self.cache.data["415"])

    def test_lookup_returns_none_if_no_value_found(self):
        operator_not_found = self.cache.lookup("999")
        self.assertEqual(operator_not_found, None)

    def test_can_add_prefix(self):
        operator = Operator(
            name="Verizon",
            rates={
                "72": Decimal("0.99")
            }
        )
        self.cache.add_prefix(
            prefix="72",
            operator=operator
        )
        added_operator = self.cache.data["72"]
        self.assertEqual(added_operator, operator)

    def test_bad_operator_for_add_prefix_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.cache.add_prefix(
                prefix="999",
                operator="bad value"
            )

    def test_bad_prefix_type_for_add_prefix_raises_type_error(self):
        with  self.assertRaises(TypeError):
            self.cache.add_prefix(
                prefix=999,
                operator=Operator(
                    name="Verizon",
                    rates={
                        "72": Decimal("0.99")
                    }
                )
            )

    def test_bad_prefix_str_value_for_add_prefix_raises_type_error(self):
        with  self.assertRaises(ValueError):
            self.cache.add_prefix(
                prefix="bad value",
                operator=Operator(
                    name="Verizon",
                    rates={
                        "72": Decimal("0.99")
                    }
                )
            )

    def test_can_find_prefix_with_phone_number(self):
        prefix = self.cache.find_prefix(phone_number="415555978")
        self.assertEqual(prefix, "415")

    def test_not_match_with_find_phone_number_returns_none(self):
        no_match = self.cache.find_prefix("999")
        self.assertEqual(no_match, None)
