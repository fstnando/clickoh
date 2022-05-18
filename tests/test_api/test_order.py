import requests
from rest_framework import status

from tests.test_setup import TestSetUp
from tests.factories.product_factories import ProductFactory

product_factory = ProductFactory()

from api.models import Order


class OrderTestCase(TestSetUp):
    """
    Clase para realizar testing sobre ordenes
    """

    def setUp(self):
        """
        Metodo que pisa el metodo de inicializacion agregando los productos
        """
        super().setUp()
        self.products = product_factory.create_products(100)

    def test_create_order(self):
        """
        Metodo para controlar la creación de una orden
        """
        cantidad = self.products[0].stock
        response = self.client.post(
            '/api/orders/',
            {
                'id': 1,
                'date_time': '2022-01-01T08:00:00-03:00',
                'details': [
                    {
                        'product': self.products[0].id,
                        'cuantity': 10,
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.products[0].refresh_from_db()
        self.assertEqual(self.products[0].stock, cantidad - 10)

    def test_create_order_without_details(self):
        """
        Metodo para controlar la creación de una orden sin detalles
        """
        response = self.client.post(
            '/api/orders/',
            {
                'date_time': '2022-01-01T08:00:00-03:00',
                'details': [
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('details' in response.data)
        self.assertEqual(len(response.data['details']), 1)
        self.assertEqual(response.data['details'][0].code, 'invalid')

    def test_update_order(self):
        """
        Metodo para controlar la actualización de una orden
        """
        self.test_create_order()
        order = Order.objects.get(id=1)
        cantidad = self.products[0].stock
        response = self.client.put(
            '/api/orders/1/',
            {
                'date_time': '2022-01-01T10:00:00-03:00',
                'details': [
                    {
                        'id': order.orderdetail_set.all()[0].id,
                        'product': self.products[0].id,
                        'cuantity': 20,
                    }
                ]
            },
            format='json'
        )
        self.products[0].refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.products[0].stock, cantidad - 10)

    def test_update_order_change_product(self):
        """
        Metodo para controlar la actualización de una orden cuando cambia el
        producto en uno de los detalles
        """
        self.test_create_order()
        order = Order.objects.get(id=1)
        cantidad1 = self.products[0].stock
        cantidad2 = self.products[1].stock
        response = self.client.put(
            '/api/orders/1/',
            {
                'date_time': '2022-01-01T10:00:00-03:00',
                'details': [
                    {
                        'id': order.orderdetail_set.all()[0].id,
                        'product': self.products[1].id,
                        'cuantity': 20,
                    }
                ]
            },
            format='json'
        )
        self.products[0].refresh_from_db()
        self.products[1].refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.products[0].stock, cantidad1 + 10)
        self.assertEqual(self.products[1].stock, cantidad2 - 20)

    def test_delete_order(self):
        """
        Metodo para controlar la eliminación de una orden
        """
        self.test_create_order()
        response = self.client.delete(
            '/api/orders/1/',
            {},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_action_get_total(self):
        """
        Metodo para controlar la acción get_total de ordenes
        """
        self.test_create_order()
        order = Order.objects.get(id=1)
        total = round(self.products[0].price * 10, 2)
        response = self.client.get(
            '/api/orders/1/get_total/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], total)

    def test_action_get_total_usd(self):
        """
        Metodo para controlar la acción get_total_usd de ordenes
        """
        self.test_create_order()
        order = Order.objects.get(id=1)
        total = round(self.products[0].price * 10, 2)
        response = self.client.get(
            '/api/orders/1/get_total_usd/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data2 = response.json()
        encontrado = False
        valor = 0.0
        for el in data2:
            if ('casa' in el and 'nombre' in el['casa'] and
                'venta' in el['casa'] and
                el['casa']['nombre'] == 'Dolar Blue'):

                try:
                    valor = float(el['casa']['venta'].replace('.', ''
                        ).replace(',', '.'))
                    encontrado = True
                    break
                except:
                    pass
        self.assertEqual(encontrado, True)
        self.assertEqual(data['total'], round(total / valor, 2))
