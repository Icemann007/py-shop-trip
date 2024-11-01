import json
from datetime import datetime

from app.customer import Customer
from app.car import Car
from app.shop import Shop


def shop_trip() -> None:
    with open("app/config.json", "r") as f:
        data = json.load(f)

    fuel_price = data["FUEL_PRICE"]
    customers = []
    shops = []

    for customer in data["customers"]:
        customer_instance = Customer(
            customer["name"],
            customer["product_cart"],
            customer["location"],
            customer["money"],
            Car(
                customer["car"]["brand"],
                customer["car"]["fuel_consumption"]
            )
        )
        customers.append(customer_instance)

    for shop in data["shops"]:
        shop_instance = Shop(
            shop["name"],
            shop["location"],
            shop["products"]
        )
        shops.append(shop_instance)

    for customer in customers:
        min_cost = float("inf")
        choose_shop = ""
        total_product_price = 0
        print(customer.have_money())

        for shop in shops:
            price = customer.travel_calculation(shop, fuel_price)
            print(f"{customer.name}'s trip to the {shop.name} costs {price}")

            if price < min_cost:
                min_cost = price
                choose_shop = shop
        if min_cost > customer.money:
            print(f"{customer.name} doesn't have enough "
                  f"money to make a purchase in any shop")
            return
        else:
            print(f"{customer.name} rides to {choose_shop.name}")

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"\nDate: {current_time}"
              f"\nThanks, {customer.name}, for your purchase!")
        print("You have bought:")

        for key, value in customer.product_cart.items():
            product_price = value * choose_shop.products[key]
            if isinstance(product_price, float) and product_price.is_integer():
                product_price = int(product_price)
            print(f"{value} {key}s for {product_price} dollars")
            total_product_price += product_price

        print(f"Total cost is {total_product_price} dollars\n"
              f"See you again!\n\n"
              f"{customer.name} rides home\n"
              f"{customer.name} now has {customer.money - min_cost} dollars\n")
