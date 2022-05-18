from faker import Faker

from api.models import Product

faker = Faker()


class ProductFactory:
    """
    Clase para realizar factorias de productos
    """

    def create_products(self, cant):
        """
        Metodo para crear al azar una cierta cantidad de producto
        """
        numbers = set(faker.unique.random_int() for i in range(cant))
        productos = []
        for el in numbers:
            productos.append(
                Product.objects.create(**{
                    'id': str(el),
                    'name': faker.name(),
                    'price': faker.random_int(min=100, max=100000) / 100,
                    'stock': faker.random_int(min=100, max=1000),
                })
            )
        return productos
