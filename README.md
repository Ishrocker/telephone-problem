### Run tests
Standing in the root dir of the project run

```bash
python3 -m unittest discover
```

### Run app
Standing in the root dir of the project run

```bash
python3 operator_checker 14155559485 --file ./operator_checker/dummy_data.txt
```

Accepts as positional arguments the phone number(s) or prefix(s) to lookup

--file is expected to be a file with data formatted as the excersise states:

```
Operator NameOfSomeOperator:
prefix value
prefix value

Operator NameOfSomeOperator:
prefix value
prefix value
```

Only limit to the size of the file is the memory of your machine.
Excersise states that data should be assumed to fit in memory.

For more information use:

```bash
python3 operator_checker --help
```

### Routing of telephone calls

Some telephone operators have submitted their price lists including price per
minute for different phone number prefixes. The price lists look like this:

#### Operator A:

1  0.9

268  5.1

46  0.17

4620  0.0

468  0.15

4631  0.15

4673  0.9

46732  1.1

#### Operator B:

1  0.92

44  0.5

46  0.2

467  1.0

48  1.2

And so on...

The left column represents the telephone prefix (country + area code) and
the right column represents the operators price per minute for a number
starting with that prefix. When several prefixes match the same number, the
longest one should be used. If you, for example, dial +46-73-212345 you
will have to pay $ 2.1/min with Operator A and $ 1.0/min with Operator B.

If a price list does not include a certain prefix you cannot use that
operator to dial numbers starting with that prefix. For example it is not
possible to dial +44 numbers with operator A but it is possible with
Operator B.

### The Goal

The goal with this exercise is to write a program that can handle any number
of price lists (operators) and then can calculate which operator that is
cheapest for a certain number. You can assume that each price list can have
thousands of entries but they will all fit together in memory.

Telephone numbers should be inputted in the same format as in price lists,
for example “68123456789”. The challenge is to find the cheapest operator
for that number.

### Instructions

- Use your favorite language to solve the exercise.
- Put your focus on code design and readability.
- Do not use a database or create a GUI.
- Plus is given to effective solutions.
- The code should have unit tests.
