from typing import Dict, List

class ProductClass:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity: int) -> None:
        if self.stock + quantity < 0:
            print(f"Ошибка: Недостаточно товара '{self.name}' на складе.")
        else:
            self.stock += quantity
            print(f"Обновлено количество '{self.name}': {self.stock}")

class OrderClass:
    def __init__(self):
        self.products: Dict[ProductClass, int] = {}

    def add_product(self, product: ProductClass, quantity: int) -> None:
        if product.stock < quantity:
            print(f"Ошибка: Недостаточно товара '{product.name}' на складе для добавления в заказ.")
            return
        if product in self.products:
            self.products[product] += quantity
        else:
            self.products[product] = quantity

        product.update_stock(-quantity)
        print(f"Добавлено в заказ: {quantity} шт. '{product.name}'")

    def remove_product(self, product: ProductClass, quantity: int) -> None:
        if product not in self.products:
            print(f"Ошибка: Товар '{product.name}' отсутствует в заказе.")
            return
        if self.products[product] < quantity:
            print(f"Ошибка: В заказе меньше товара '{product.name}', чем пытаетесь удалить.")
            return

        self.products[product] -= quantity
        product.update_stock(quantity)

        if self.products[product] == 0:
            del self.products[product]

        print(f"Удалено из заказа: {quantity} шт. '{product.name}', остаток в заказе {self.products[product]}")

    def return_product(self, product: ProductClass, quantity: int) -> None:
        if product not in self.products:
            print(f"Ошибка: Товар '{product.name}' отсутствует в заказе.")
            return
        if self.products[product] < quantity:
            print(f"Ошибка: В заказе меньше товара '{product.name}', чем пытаетесь вернуть.")
            return

        self.products[product] -= quantity
        product.update_stock(quantity)

        if self.products[product] == 0:
            del self.products[product]
        print(f"Возврат товара: {quantity} шт. '{product.name}'")

    def calculate_total_price(self) -> float:
        total_price = sum(product.price*quantity for product, quantity in self.products.items())
        return total_price

class StoreClass:
    def __init__(self):
        self.products: List[ProductClass] = []

    def add_product(self, product: ProductClass) -> None:
        self.products.append(product)
        print(f"Товар '{product.name}' добавлен в магазин.")

    def list_products(self) -> None:
        if not self.products:
            print("Магазин пуст.")
            return

        print("Список товаров в магазине:")
        for product in self.products:
            print(f"- {product.name}: {product.price} руб., на складе: {product.stock} шт.")

    def create_order(self) -> OrderClass:
        return OrderClass()

if __name__ == "__main__":
    store = StoreClass()

    apple=ProductClass("Apple", 10, 100)
    banana=ProductClass("Banana", 30, 50)

    store.add_product(apple)
    store.add_product(banana)

    store.list_products()

    order = store.create_order()
    order.add_product(apple, 10)
    order.add_product(banana, 5)

    print(f"Итоговая сумма заказа: {order.calculate_total_price()} руб.")

    order.remove_product(apple, 5)
    order.remove_product(banana, 2)

    print(f"Итоговая сумма заказа после изменений: {order.calculate_total_price()} руб.")


