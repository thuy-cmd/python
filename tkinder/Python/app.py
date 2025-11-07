"""
This is a sample Python script demonstrating string manipulation.
String Methods Covered:
strip() remove whitespaces from the beginning and end of a string.
lstrip() remove whitespaces from the left side of a string.
rstrip() remove whitespaces from the right side of a string.
replace() replace a specified phrase with another specified phrase.
find() searches the string for a specified value and returns the position of where it was found.
split() splits the string at the specified separator and returns a list.
upper() converts a string to upper case.
lower() converts a string to lower case.
title() converts the first character of each word to upper case.
format() formats specified values in a string.
in and not in operators return True if a specified phrase is present in the string, otherwise False.
f-strings are string literals that have an f at the beginning and curly braces containing expressions that will be replaced with their values.
Number of string methods covered:
round() rounds a floating point number to a specified number of decimal places.
abs() returns the absolute value of a number.
pow() returns the value of x to the power of y.
max() returns the largest item in an iterable.
min() returns the smallest item in an iterable.
sum() returns the sum of all items in an iterable.
sorted() returns a new sorted list from the items in an iterable.
len() returns the number of items in an obje(ct.
int, float, bool() functions to convert values to integer, floating point number, or boolean.

"""
import math
command = ""
while command.lower() != "quit":
    num = math.ceil(math.pow(math.sqrt(50), 2))
    print(num)
    command = input("> ")
    if command.lower() == "guess":
        guess = int(input("Enter your guess (1-100): "))
        if guess < num:
            print("Too low!")
        elif guess > num:
            print("Too high!")
        else:
            print("Congratulations! You guessed it right.")
    elif command.lower() == "help":
        print("Type 'guess' to make a guess or 'quit' to exit the game.")
    elif command.lower() == "quit":
        print("Thanks for playing!")
    else:
        print("Invalid command. Please try again.")
