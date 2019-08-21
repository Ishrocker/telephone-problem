import random
import string


def prefix(length: int) -> str:
    """
    Random number of a given length as a string.

    String will have no leading zero.
    """
    prefix_buffer: list = []
    for i in range(length):
        if i == 0:
            prefix_buffer.append(
                random.choice(string.digits[1::])  # no leading zero
            )
        else:
            prefix_buffer.append(
                random.choice(string.digits)
            )
    return "".join(prefix_buffer)

if __name__ == "__main__":
    print(prefix(3))
    print(string.digits)
