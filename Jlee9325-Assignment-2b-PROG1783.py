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

#this is my welcome function
def show_welcome():
    print("Welcome to Arnold's Amazing Eats!")
    print("Place your meal for pick up or delivery.\n")

#this function triggers when nothing is inputed
def get_non_empty_input(prompt):
    value = input (prompt).strip()
    while value == "":
        value = input("This field cannot be empty. " + prompt).strip()
    return value

#this is the postal code function
def get_postal_code():
    code = input("Enter your postal code (7 characters):") .strip()
    while len(code) !=7:
        code = input("Postal code must be 7 characters, please try again") .strip()
    return code

#this is the function for customer information
def get_customer_info():
    info = {}
    info["first_name"] = get_non_empty_input("Enter your first name: ")
    info["last_name"] = get_non_empty_input("Enter your last name: ")
    info["phone_number"] = get_non_empty_input("Enter your phone number: ")
    info["delivery"] = input("Do you need delivery? (y/n): ").lower()
    while info["delivery"] not in ['y', 'n']:
        info["delivery"] = input("Please enter 'y' or 'n': ").lower()

    if info["delivery"] == 'y':
        info["street"] = get_non_empty_input("Enter your street address: ")
        info["unit"] = input("Enter your unit number (optional): ")
        info["city"] = get_non_empty_input("Enter your city: ")
        info["province"] = get_non_empty_input("Enter your Province: ")
        info["postal_code"] = get_postal_code()
        info["instructions"] = input("Any specidic delivery instructions? ")
    return info

#This function is to show the menu
def show_menu():
    print("\nmenu:")
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
    delivery_charge = 0
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
    print(f"{customer['first_name']}{customer['last_name']}")

    if customer["delivery"] == 'y':
        full_address = f"{customer['street']}" + (f" Unit{customer['unit']}" if customer ['unit'] else"")
        print(full_address)
        print(f"{customer['city']}{customer['province']}, {customer['postal_code']}")
        print(f"{customer['instructions']}\n")
    else:
        print(f"Phone: {customer['phone']}\n")

    