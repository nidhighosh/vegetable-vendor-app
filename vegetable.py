import json
from collections import defaultdict

# Step 1: Create the vegetable database
vegetable_db = defaultdict(list)
vegetable_db["Leafy"] = {"Spinach":30, "Lettuce":25, "Cabbage":30}
vegetable_db["Root"] = {"Beetroot":50, "Carrot":60, "elephant yam":100}
vegetable_db["Flower"] = {"Broccoli":50, "Cauliflower":30}
vegetable_db["Underground"] = {"Potato":30, "Onion":40, "Garlic":20}
vegetable_db["Fruity"] = {"Tomato":50, "Cucumber":60, "Capsicum":40}

# Step 2: Show available vegetables
print("Welcome to the Vegetable Vendor App!\n")
print("We have the following types of vegetables:\n")
for veg_type, items in vegetable_db.items():
    print(f"{veg_type} Vegetables: {', '.join(items)}")

# Step 3: Let user add to cart
cart = []
stack = []

print("\nPlease type one vegetable at a time to add to your cart.")
print("Type 'done' when you want to finish shopping.\n")

while True:
    user_input = input("Enter vegetable name 1 at a time: ").strip().capitalize()
    
    if user_input.lower() == "done":
        break

    # Step 4: Check availability using try-except
    try:
        found = False
        for items in vegetable_db.values():
            if user_input in items:
                found = True
                try:
                    qty = float(input(f"Enter quantity for {user_input} (in kg): "))
                    # Find the category for the vegetable
                    for category, items_dict in vegetable_db.items():
                        if user_input in items_dict:
                            price = items_dict[user_input]
                            break
                    subtotal = qty * price
                    item = {
                        "name": user_input,
                        "quantity": qty,
                        "price_per_kg": price,
                        "subtotal": subtotal
                    }
                    cart.append(item)
                    stack.append(item)
                    print(f"{user_input}({qty}kg) added to cart.")
                except ValueError:
                    print("Invalid quantity entered. Please enter a number for quantity.")
                    break
        if not found:
            raise ValueError(f"{user_input} is not available.")
    except ValueError as ve:
        print(ve)

# Step 5: Show final cart
print("\nYour cart contains:", cart)

# Step 6: Ask if user wants to finish
finish = input("\nWould you like to finish your purchase? (yes/no): ").strip().lower()

if finish == "yes":
    # Ask for delivery or pickup
    print("\nHow would you like to receive your order?")
    print("1. Pick-up")
    print("2. Home Delivery (₹20 extra)")
    delivery_choice = input("Enter 1 or 2: ").strip()

    delivery_method = "Pick-up"
    delivery_fee = 0

    if delivery_choice == "2":
        delivery_method = "Home Delivery"
        delivery_fee = 20
        print("₹20 delivery fee will be added.")

    try:
        # Save cart to JSON
        with open("order.json", "w") as f:
            json.dump({"cart": cart}, f, indent=2)
        print("\nOrder saved")

        # Load JSON back
        with open("order.json", "r") as f:
            order_data = json.load(f)

        # Prepare receipt (without date/time)
        receipt_lines = []
        receipt_lines.append("Receipt")
        receipt_lines.append(f" Delivery Method: {delivery_method}")
        receipt_lines.append("-" * 40)

        total = 0
        for i, item in enumerate(order_data["cart"], 1):
            name = item["name"]
            quantity = item["quantity"]
            price = item["price_per_kg"]
            subtotal = item["subtotal"]
            total += subtotal
            line = f"{i}. {name} - {quantity} kg ---> ₹{price}/kg = ₹{subtotal:.2f}"
            print(line)
            receipt_lines.append(line)

        if delivery_fee:
            total += delivery_fee
            receipt_lines.append(f"Delivery Fee: ₹{delivery_fee}")

        receipt_lines.append("-" * 40)
        #receipt_lines.append(f"Total Amount: ₹{total:.2f}")
        if delivery_fee:
            receipt_lines.append(f"Total Amount (including delivery): ₹{total:.2f}")
        else:
            receipt_lines.append(f"Total Amount: ₹{total:.2f}")
        receipt_lines.append("*" * 40)
        receipt_lines.append("         Thank You for Shopping!         ")
        receipt_lines.append("*" * 40)
        if delivery_fee:
            print(f"Total Amount (including delivery): ₹{total:.2f}")
        else:
            print(f"Total Amount: ₹{total:.2f}")

        # Print thank-you note
        print("\n" + "*" * 40)
        print("         Thank You for Shopping!         ")
        print("*" * 40)

        # Save to receipt.txt
        with open("receipt.txt", "w",encoding='utf-8') as receipt_file:
            for line in receipt_lines:
                receipt_file.write(line + "\n")

        print("Receipt also saved as 'receipt.txt'")
        print("\nYour order is confirmed.")

    except Exception as e:
        print("An error occurred while processing your order:", e)
else:
    print(" Order canceled.")