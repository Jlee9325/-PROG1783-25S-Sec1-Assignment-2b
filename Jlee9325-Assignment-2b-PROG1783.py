# Name:                 Jlee9325-assignment2b.py
# Author:               Justin Lee
# Date Created:         July 23th, 2025
# Date Last Modified:   July 23rd, 2025

# Purpose:
#  Expand on Arnolds's eats - collect customers orders
#  allows delivery/pickup, applies discounts and tips, and prints the receipt



#these are my constants for the receipt this includes taxes, delivery, tips, etc

STUDENT_DISCOUNT_RATE = 0.15
HST_RATE = 0.13
DELIVERY_FEE = 7.00
FREE_DELIVERY = 25.00
TIP_OPTIONS = {1: 1.00, 2: 2.00, 3: 5.00}

#This is my Menu Dictionary adding 4 more items from 2

menu = {
    1: {"name": "Garlic Burger", "price": 12.69},
    2: {"name": "Cheese Pizza", "price": 15.99},
    3: {"name": "Snack Wrap", "price": 9.39},
    4: {"name": "Nacho Fries", "price": 7.99},
    5: {"name": "Poutine", "price": 9.79},
    6: {"name": "The Dawg","price": 6.49},
}

#adding my functions

def show_welcome():
    print("Welcome to Arnold's Amazing Eats!")
    print("Place your meal for pick up or delivery.\n")

#this function triggers when nothing is inputed
def get_non_empty_input(prompt):
    value = input (prompt).strip()
    while value == "":
        value = input("This field cannot be empty. " + prompt).strip()
    return value