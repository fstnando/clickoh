import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication, permissions

from .models import Product, Order, OrderDetail
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_destroy(self, instance):
        instance.reset_stock()
        instance.delete()

    @action(detail=True, methods=['get'])
    def get_total(self, request, pk=None):
        """
        Action get_total for orders.
        """
        order = self.get_object()
        total = order.get_total()
        total = round(total, 2)
        return Response({
            'total': total
        })

    @action(detail=True, methods=['get'])
    def get_total_usd(self, request, pk=None):
        """
        Action get_total_usd for orders.
        """
        errores = []

        url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            encontrado = False
            valor = 0.0
            for el in data:
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
        else:
            errores.append('La conexión con la api: www.dolarsi.com ha fallado')

        if valor <= 0.0:
            errores.append('El valor del dolar no puede ser 0')

        if errores:
            return Response(errores)
        else:
            order = self.get_object()
            total = order.get_total()
            total = round(total / valor, 2)

            return Response({
                'total': total
            })
