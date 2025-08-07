# Name:                 Jlee9325-assignment2b.py
# Author:               Justin Lee
# Date Created:         July 23th, 2025
# Date Last Modified:   August 6th, 2025

# Purpose:
#  Expand on Arnolds's eats - collect customers orders
#  allows delivery/pickup, applies discounts and tips, and prints the receipt

#adding systems and date and time for the txt file print out

import sys
from datetime import datetime

#these are my constants for the receipt this includes taxes, delivery, tips, etc

STUDENT_DISCOUNT_RATE = 0.15
HST_RATE = 0.13
DELIVERY_FEE = 7.00
FREE_DELIVERY = 25.00
TIP_OPTIONS = {1: 0.10, 2: 0.15, 3: 0.20}

#This is my Menu Dictionary Using classes

menu = {
    1: {"name": "Garlic Burger", "price": 12.69},
    2: {"name": "Cheese Pizza", "price": 15.99},
    3: {"name": "Snack Wrap", "price": 9.39},
    4: {"name": "Nacho Fries", "price": 7.99},
    5: {"name": "Poutine", "price": 9.79},
    6: {"name": "The Dawg","price": 6.49},
}

#adding my functions
#this is my welcome function
def show_welcome():
    print("Welcome to Arnold's Amazing Eats!")
    print("Place your meal for pick up or delivery.\n")

#this function triggers when nothing is inputed
def get_valid_input(prompt, validation_func, error_msg="Invalid input. Please Try Again."):
    while True:
        try:
            user_input = input(prompt).strip()
            if validation_func(user_input):
                return user_input
            print (error_msg)
        except Exception as e:
            print(f"Error: {str(e)}")

#this is the postal code function
def get_postal_code():
    code = input("Enter your postal code (7 characters):") .strip()
    while len(code) !=7:
        code = input("Postal code must be 7 characters, please try again") .strip()
    return code

#this is the function for customer information
def get_customer_info():
    info = {}
    print("\n=== Customer Information ===")
    info["first_name"] = get_valid_input("Enter your first name: ", validate_not_empty)
    info["last_name"] = get_valid_input("Enter your last name: ")
    info["phone_number"] = get_valid_input("Enter your phone number: ")
    info["delivery"] = input("Do you need delivery? (y/n): ").lower()
    while info["delivery"] not in ['y', 'n']:
        info["delivery"] = input("Please enter 'y' or 'n': ").lower()

    if info["delivery"] == 'y':
        info["street"] = get_valid_input("Enter your street address: ")
        info["unit"] = input("Enter your unit number (optional): ")
        info["city"] = get_valid_input("Enter your city: ")
        info["province"] = get_valid_input("Enter your Province: ")
        info["postal_code"] = get_postal_code()
        info["instructions"] = input("Any specific delivery instructions? ")
    return info

#This function is to show the menu
def show_menu():
    print("\nMenu:")
    for key, item in menu.items():
        print(f"{key}) {item['name']} - ${item['price']:.2f}")
    
#this function is to take orders
def take_order():
    order = {}
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter the number of the meal you'd like to order (1-6): "))
            if choice not in menu:
                print("Invalid choice. Try Again.")
                continue

            #this is for the amount of meals you would want    
            qty = int(input("\nHow many items of this item would you like? "))
            if qty <= 0:
                print("Quantity must be more than 0.")
                continue

            confirm = input(f"You Selected {qty} {menu[choice]['name']}(s)). Confirm? (y/n): ").lower()

            if confirm == 'y':
                order["meal"] = menu[choice]['name']
                order["price"] = menu[choice]['price']
                order["quantity"] = qty
                break
        except ValueError:
            print("Please enter valid numbers.")
    return order

#this function is for if the customer is a student or not, this infomation will be for the students discount
def is_student():
    answer = input("Are you a student? (y/n): ").lower()
    while answer not in ['y', 'n']:
        answer = input("Please enter 'y' or 'n': ").lower()
    return answer == 'y'

#this function is for tip percentage
def get_tip_percentage():
    print("1) 10% 2) 15% 3) 20%")
    try:
        choice = int(input("Choose your tip amount (1,2 or 3): "))
        return TIP_OPTIONS.get(choice,0.15) #this is the default percentage if option is invalid
    except ValueError:
        return 0.15
    
#this function is to calculate the totals of the meal
def calculate_total (order, student, delivery, tip_percent):
    item_total= order["price"] * order["quantity"]
    discount = item_total * STUDENT_DISCOUNT_RATE if student else 0
    subtotal = item_total - discount
    delivery_charge = DELIVERY_FEE if (delivery and subtotal < FREE_DELIVERY) else 0
    if delivery_charge and subtotal < FREE_DELIVERY:
        delivery_charge = DELIVERY_FEE
    tip = subtotal *tip_percent if delivery else 0
    tax = subtotal *HST_RATE
    total = subtotal + delivery_charge + tip + tax

    return {
        "item_total" : item_total,
        "discount" : discount,
        "subtotal" : subtotal,
        "delivery" : delivery_charge,
        "tip" : tip,
        "tax" : tax,
        "total" : total
    }

#this next function is for printing the receipt

def print_receipt(customer, order, costs, student, tip_percent):
    print ("\n\n===ARNOLD'S AMAZING EATS===")
    print("           RECEIPT\n")

    print(f"{customer['first_name']} {customer['last_name']}")

    if customer["delivery"] == 'y':
        full_address = f"{customer['street']}" + (f" Unit{customer['unit']}" if customer ['unit'] else"")
        print(full_address)
        print(f"{customer['city']}{customer['province']}, {customer['postal_code']}")
        print(f"{customer['instructions']}\n")
    else:
        print(f"Phone: {customer['phone']}\n")

    print(f"{'Order':<25}{'Item Amt':>10}{'Item Price':>15}{'Total':>12}")
    print(f"{order['meal']:<25}{order['quantity']:>10}{f'${order['price']:.2f}':>15}{f'${costs['item_total']:.2f}':>12}")

    if student:
        print(f"{'15% Student saving':>50}{f'-${costs['discount']:.2f}':>12}")

    print(f"{'Sub Total':>50}{f'${costs['subtotal']:.2f}':>12}")

    if customer["delivery"] == 'y':
        if costs["delivery"] == 0:
            print(f"{'Delivery (Waived)':>50}{f'${costs['delivery']:.2f}':>12}")
        else:
            print(f"{'Delivery':>50}{f'${costs['delivery']:.2f}':>12}")
        print(f"{f'Tips ({int(tip_percent*100)}%)':>50}{f'${costs['tip']:.2f}':>12}")

    print(f"{'Tax(13%)':>50}{f'${costs['tax']:.2f}':>12}")
    print(f"{'':>50}{'--------':>12}")
    print(f"{'TOTAL':>50}{f'${costs['total']:.2f}':>12}")
    print("\nThank you for your order!")

#The next couple of functions are for my validations

def validate_not_empty(input_str):
    return len(input_str.strip()) > 0

def validate_postal_code(code):
    return len(code.strip()) == 7

def validate_menu_choice(choice):
    try:
        return 1<= int(choice) <= 8
    except ValueError:
        return False
    
def validate_quantity(qty):
    try:
        return int(qty) > 0 
    except ValueError:
        return False
    
def validate_yn(response):
    return response.lower() in ['y','n']
 
    #this is the main function that 
def run_arnolds_amazing_eats():
    show_welcome()
    customer = get_customer_info()
    order = take_order()
    student = is_student()
    tip_percent = get_tip_percentage() if customer["delivery"] == 'y' else 0
    costs = calculate_total(order, student, customer["delivery"] == 'y', tip_percent)
    print_receipt(customer, order, costs, student, tip_percent)

run_arnolds_amazing_eats()

    