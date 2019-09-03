from typing import Tuple, Dict, Optional
from dataclasses import dataclass, field
from decimal import Decimal


def raise_type_error(instance: object, prop: str, expected_type: str):
    err_msg = (
        f"Property `{prop}` of instance `{type(instance).__name__}` expected "
        f"to be of type {expected_type} but was type "
        f"`{type(getattr(instance, prop))}`"
    )
    raise TypeError(err_msg)


@dataclass
class Operator:
    name: str
    rates: Dict[str, Decimal]

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise_type_error(
                instance=self,
                prop="name",
                expected_type="str"
            )

        if not isinstance(self.rates, dict):
            raise_type_error(
                instance=self,
                prop="rates",
                expected_type="dict"
            )

        for prefix, price in self.rates.items():
            if not isinstance(prefix, str):
                raise ValueError(
                    f"Dict keys of property `rates` of instance "
                    f"`{type(self).__name__}` expected to be of type "
                    f"`str` but got key {prefix} of `{type(prefix)}`"
                )
            if not isinstance(price, Decimal):
                raise ValueError(
                    f"Dict values of property `rates` of instance "
                    f"`{type(self).__name__}` expected to be "
                    f"of type `Decimal` but got value {price} of type "
                    f"`{type(price)}`"
                )
            if price < Decimal("0"):
                raise ValueError(
                    f"Dict values of property `rates` of instance "
                    f"`{type(self).__name__}` expected to have positive "
                    f"values but got value: {price}"
                )


    def price_for_prefix(self, prefix: str) -> Optional[Decimal]:
        if not isinstance(prefix, str):
            raise TypeError(
                f"`prefix` expected to be of type `str` but got type "
                f"{type(prefix)}"
            )

        if not prefix.isdigit():
            raise ValueError(
                f"`prefix` expected to be a digit but got a prefix with "
                f"the value `{prefix}`"
            )

        return self.rates.get(prefix)

    def has_better_price_for_prefix(self, prefix: str, price: Decimal) -> bool:
        if not isinstance(price, Decimal):
            raise TypeError(
                f"`price` expected to be of type `Decimal` but got type "
                f"`{type(price)}`"
            )

        operator_price = self.price_for_prefix(prefix)
        return operator_price < price if operator_price else False


@dataclass
class PrefixCache:
    """ A mapping of prefixes to operators with the best price for each prefix.

    Example:

        >>> cache = PrefixCache()
        >>> cache.data.update({"415": Operator(name="TelCom", rates={"415": Decimal("1.99")})})
        >>> cache.find_prefix("415")
        '415'
        >>> cache.lookup("415")
        Operator(name='TelCom', rates={'415': Decimal('1.99')})
    """
    data: Dict[str, Operator] = field(default_factory=lambda: dict())

    def _update_prefix(self, prefix: str, operator: Operator):
        """ Update prefix with operator with best price. """
        cached_operator: Optional[Operator] = self.lookup(prefix)
        if cached_operator:
            cached_price = cached_operator.price_for_prefix(prefix)
            if cached_price:
                if operator.has_better_price_for_prefix(prefix, cached_price):
                    self.add_prefix(prefix=prefix, operator=operator)
        else:
            self.add_prefix(prefix=prefix, operator=operator)

    def find(self, number: str) -> Optional[str]:
        """ Find if a given number a prefix in cache. """
        if number in self.data:  # noqa
            return number
        else:
            return None

    def update_with_operator(self, operator: Operator):
        """ Updates `PrefixCache` with data from given operator. """
        if not isinstance(operator, Operator):
            raise TypeError(
                f"operator expected to be of type `Operator` but got type "
                f"{type(operator)}"
            )

        for prefix in operator.rates.keys():
            self._update_prefix(prefix=prefix, operator=operator)

    def lookup(self, prefix: str) -> Optional[Operator]:
        """ Given a prefix, returns operator with best price in `PrefixCache` """
        return self.data.get(prefix, None)  # noqa

    def add_prefix(self, prefix: str, operator: Operator):
        """ map given prefix to operator, overwriting exsisting cache for prefix entry. """
        if not isinstance(operator, Operator):
            raise TypeError(
                f"`operator` expected to be of type `str` but got type "
                f"`{type(operator)}`"
            )

        if not isinstance(prefix, str):
            raise TypeError(
                f"`prefix` is expected to be of type `str` but got type "
                f"`{type(prefix)}`"
            )

        if not prefix.isdigit():
            raise ValueError(
                "Value of `prefix` is expected to a string representation "
                "of a digit"
            )

        self.data[prefix] = operator  # noqa

    def find_prefix(self, phone_number: str) -> Optional[str]:
        """ Return prefix for `phone_number`.  Use `lookup` to fetch operator. """
        if not isinstance(phone_number, str):
            raise TypeError(
                f"`phone_number` expected to be of type `str` "
                f"but got type `{type(phone_number)}`"
            )

        if not phone_number.isdigit():
            raise ValueError(
                "Value of `phone_number` expected to be a string "
                "representation of a digit"
            )

        phone_number = phone_number
        match = None
        for i, _ in enumerate(phone_number, start=1):
            prefix = self.find(phone_number[:i])
            if prefix:
                match = prefix
            else:
                prefix_not_found = prefix is None  # readability
                if match and prefix_not_found:
                    return match
                else:
                    continue
        return match

    @classmethod
    def build_cache(klass: "PrefixCache", operators: Tuple[Operator, ...]) -> "PrefixCache":
        """ Build a `PrefixCache` from a tuple of `Operators`. """
        prefix_cache = klass()
        for operator in operators:
            prefix_cache.update_with_operator(operator)

        return prefix_cache
