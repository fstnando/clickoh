from rest_framework import status

from tests.test_setup import TestSetUp


class ProductTestCase(TestSetUp):
    """
    Clase para realizar testing sobre productos
    """

    def test_create_product(self):
        """
        Metodo para controlar la creación de un producto
        """
        response = self.client.post(
            '/api/products/',
            {
                'id': 'F00001',
                'name': 'Manzanas',
                'price': 10.2,
                'stock': 100,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 'F00001')

        response = self.client.post(
            '/api/products/',
            {
                'id': 'F00002',
                'name': 'Bananas',
                'price': 22.2,
                'stock': 200,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 'F00002')

    def test_create_repited_product(self):
        """
        Metodo para controlar que no se pueda crear un producto que ya existe
        """
        self.test_create_product()
        response = self.client.post(
            '/api/products/',
            {
                'id': 'F00001',
                'name': 'Manzanas',
                'price': 10.2,
                'stock': 100,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('id' in response.data)
        self.assertEqual(len(response.data['id']), 1)
        self.assertTrue(response.data['id'][0].code == 'unique')

    def test_retrive_product(self):
        """
        Metodo para controlar la devolución de un producto
        """
        self.test_create_product()
        response = self.client.get(
            '/api/products/F00001/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Manzanas')
        self.assertEqual(response.data['price'], 10.2)
        self.assertEqual(response.data['stock'], 100)
