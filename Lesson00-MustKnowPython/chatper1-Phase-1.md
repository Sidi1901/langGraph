
### Data types

data types

| Type     | Example     |
| -------- | ----------- |
| int      | 10          |
| float    | 10.5        |
| str      | "Hello"     |
| bool     | True, False |
| NoneType | None        |


Example

name = "Sid"
age = 25
salary = 50000.50
is_active = True

Checking type
print(type(age))

Multiple Assignment
x, y, z = 10, 20, 30

Dynamic Typing

Python variables can change type.

x = 10
x = "hello"


### Input, Output, and Type Conversion

1. Output (print)

Used to display data.

print("Hello World")

2. Input (input)

Used to take input from the user.

name = input("Enter your name: ")

print(name)

Note: input() Always Returns a String


4. Type Conversion
String → Integer
age = int(input("Enter age: "))
String → Float
salary = float(input("Enter salary: "))
Integer → String
age = 25

text = str(age)


#### Operators

1. Arithmetic Operators
a = 10
b = 3

print(a + b)   # 13 - Addition operator
print(a - b)   # 7 - Subtraction operator
print(a * b)   # 30 - Multiplication operator
print(a / b)   # 3.3333333333333335 - Float Division operator
print(a // b)  # 3 - Integer division (floor division) operator
print(a % b)   # 1 - Modulo operator (remainder)
print(a ** b)  # 1000 - Exponentiation operator

2. Comparison Operators

Comparison operators return True or False.

a = 10
b = 20

print(a == b)
print(a != b)
print(a > b)
print(a < b)
print(a >= b)
print(a <= b)


3. Logical Operators
and

Both conditions must be True.

age = 25

print(age > 18 and age < 60)

or

At least one condition must be True.

print(10 > 5 or 10 < 3)

not

Reverses the result.

is_admin = True

print(not is_admin)

4. Membership Operators

Checks whether a value exists in a collection.

in
servers = ["rhel8", "rhel9", "ubuntu"]

print("rhel9" in servers)

not in
servers = ["rhel8", "rhel9"]

print("windows" not in servers)

#### Control Flow

1. if

Execute code only if a condition is True.

age = 20

if age >= 18:
    print("Adult")

2. if-else

Choose between two paths.

age = 15

if age >= 18:
    print("Adult")
else:
    print("Minor")


3. if-elif-else

Check multiple conditions.

score = 85

if score >= 90:
    print("Grade A")
elif score >= 80:
    print("Grade B")
elif score >= 70:
    print("Grade C")
else:
    print("Grade D")

4. Ternary Operator (One-Line if-else)
age = 20

result = "Adult" if age >= 18 else "Minor"

#### Loops

1. for Loop

Used when you want to iterate over a collection.

servers = ["rhel8", "rhel9", "ubuntu"]

for server in servers:
    print(server)

2. range()

Generates a sequence of numbers.

for i in range(5):
    print(i)

type - 

range(start, stop)
range(2, 6) → 2, 3, 4, 5

range(start, stop, step)
for i in range(0, 10, 2):
    print(i) → 0 2 4 6 8


3. while Loop

Runs while a condition is True.

count = 1

while count <= 5:
    print(count)
    count += 1

4. break

Stops the loop immediately.

for i in range(10):
    if i == 5:
        break

    print(i)

5. continue

Skips the current iteration.

for i in range(5):
    if i == 2:
        continue

    print(i)

6. pass

Placeholder. Does nothing.

for i in range(5):
    if i == 2:
        pass

    print(i)

### Functions

1. Defining a Function
def greet():
    print("Hello")

2. Function with Return Value and arguments
def add(a, b):
    return a + b

3. Default Arguments
def greet(name="Guest"):
    print(f"Hello {name}")

greet()  // Guest
greet("Sid") // Sid

3. *args

Accepts multiple positional arguments.

def add(*args):
    print(args) # (10, 20, 30)

add(10, 20, 30)

4. **kwargs

Accepts multiple keyword arguments.

def create_user(**kwargs):
    print(kwargs) # {'name': 'Sid', 'age': 25}

create_user(name="Sid", age=25)


5. Type Hints (Important for GenAI)
def add(a: int, b: int) -> int:
    return a + b

This tells readers and tools:

a is an int
b is an int
return value is an int