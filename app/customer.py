from dataclasses import dataclass
import math

from app.car import Car
from app.shop import Shop


@dataclass
class Customer:
    name: str
    product_cart: dict
    location: list[int]
    money: int | float
    car: Car

    def have_money(self) -> str:
        return f"{self.name} has {self.money} dollars"

    def trip_cost(self, shop: Shop, fuel_price: float) -> int | float:
        distance = math.sqrt(
            (self.location[0] - shop.location[0]) ** 2
            + (self.location[1] - shop.location[1]) ** 2)
        fuel = distance / 100 * self.car.fuel_consumption
        return round(fuel * fuel_price * 2, 2)

    def product_cost(self, shop: Shop) -> int | float:
        if not shop.products:
            return 0
        product_price = 0
        for key, value in self.product_cart.items():
            if key in shop.products:
                product_price += value * shop.products[key]
            else:
                raise KeyError(f"There is no {key} in {shop.name}")
        return product_price

    def total_cost(self, shop: Shop, fuel_price: float) -> int | float:
        trip_calculate = self.trip_cost(shop, fuel_price)
        product_calculate = self.product_cost(shop)
        return trip_calculate + product_calculate
