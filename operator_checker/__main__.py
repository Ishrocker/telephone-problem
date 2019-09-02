"""
Commandline interface

Run `python3 operator_checker -h` for more details
"""
import ingest
from conf import App
from argparse import ArgumentParser
from models import PrefixCache

parser = ArgumentParser(description=App.description)
parser.add_argument(
    "phone_numbers",
    metavar="N",
    type=str,
    nargs="+",
    help="Phone number(s) to look up rates for.")

parser.add_argument(
    "--file",
    type=str,
    help="path to a file containing operator pricing data.")

args = parser.parse_args()
operators = ingest.txt_file(args.file)
cache = PrefixCache.build_cache(operators)

for number in args.phone_numbers:
    prefix = cache.find_prefix(number)
    if prefix:
        op = cache.lookup(prefix)
        print(
            "operator:", op.name,
            "prefix:", prefix,
            "price", op.price_for_prefix(prefix)
        )
