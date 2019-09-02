import re
from typing import Optional, Match
from decimal import Decimal
from models import Operator

operator_table_expersion = r"\s*?Operator (?P<operator>.+):[\n](?P<rows>(\d+\s+\d.\d+\n?)+)"
operator_table_re = re.compile(operator_table_expersion)

row_expression = r"(?P<prefix>\d+)\s+?(?P<price>\d+.\d+)"
row_re = re.compile(row_expression)


def load_file_to_memory(file_path: str) -> Optional[str]:
    file_buffer = None
    with open(file_path) as f:
        # project states all data can be assumed to fit in memory
        file_buffer = f.read()
    return file_buffer


def operator_from_table(table: Match) -> Operator:
    operator_name = table.group("operator")
    operator = Operator(name=operator_name, rates=dict())
    raw_rows = table.group("rows")
    if raw_rows:
        row_matches = row_re.finditer(raw_rows)
        for row_match in row_matches:
            prefix = row_match.group("prefix")
            price = Decimal(row_match.group("price"))
            operator.rates[prefix] = price
    return operator


def txt_file(file_path: str) -> tuple:
    file_buffer = load_file_to_memory(file_path)
    if file_buffer:
        operator_tables = operator_table_re.finditer(file_buffer)
        operators = [operator_from_table(table) for table in operator_tables]

    return tuple(operators)
