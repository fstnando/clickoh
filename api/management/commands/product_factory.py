from faker import Faker

from django.core.management.base import BaseCommand, CommandError

from api.models import Product

faker = Faker()


class Command(BaseCommand):
    help = 'Create fake products'

    def add_arguments(self, parser):
        parser.add_argument('cant', type=int)

    def handle(self, *args, **options):
        """
        Metodo para crear al azar una cierta cantidad de producto
        """
        numbers = set(faker.unique.random_int() for i in range(options['cant']))
        productos = []
        for el in numbers:
            productos.append(
                Product(**{
                    'id': str(el),
                    'name': faker.name(),
                    'price': faker.random_int(min=100, max=100000) / 100,
                    'stock': faker.random_int(min=100, max=1000),
                })
            )
        Product.objects.bulk_create(productos)

        self.stdout.write(self.style.SUCCESS('Successfully creation of products'))
