from django.db.transaction import atomic

from rest_framework import serializers

from .models import Product, Order, OrderDetail


#class DefaultModelSerializer(serializers.HyperlinkedModelSerializer):
class DefaultModelSerializer(serializers.ModelSerializer):
    """
    Clase de la cual heredan las demas serializaciones
    """


class ProductSerializer(DefaultModelSerializer):
    """
    Clase para la serialización de productos
    """

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']


class OrderDetailSerializer(DefaultModelSerializer):
    """
    Clase para la serialización de detalles de ordenes
    """

    class Meta:
        model = OrderDetail
        fields = ['id', 'cuantity', 'product']


class OrderSerializer(DefaultModelSerializer):
    """
    Clase para la serialización de ordenes
    """

    details = OrderDetailSerializer(many=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'details']

    @atomic
    def update(self, instance, validated_data):
        """
        Metodo para actualizar ordenes
        """
        data = self._kwargs['data']

        instance.reset_stock()

        instance.date_time = data.get('date_time')
        instance.save()

        ids = set()
        for el in data.get('details'):
            el['product'] = Product.objects.get(id=el['product'])
            el['order'] = instance
            od = OrderDetail(**el)
            od.save()
            ids.add(od.id)

        instance.orderdetail_set.exclude(id__in=ids).delete()

        instance.update_stock()

        return instance

    @atomic
    def create(self, validated_data):
        """
        Metodo para crear ordenes
        """
        o = Order.objects.create(date_time=validated_data['date_time'])

        if 'details' in  validated_data:
            for el in validated_data['details']:
                el['product'] = Product.objects.get(id=el['product'])
                od = OrderDetail.objects.create(order=o, **el)
                od.save()

        o.update_stock()

        return o

    def validate(self, attrs):
        """
        Metodo para realizar las validaciones sobre las ordenes
        """
        data = self._kwargs['data']

        error = False
        errores = []
        productos_ids = set()
        productos = {}

        if 'details' in data:
            for i, el in enumerate(data['details']):
                errores.append({})
                if 'product' in el:
                    product = Product.objects.get(id=el['product'])
                    if product.id in productos_ids:
                        errores[i]['product'] = "Ya se encuentra el producto {}".format(product)
                        error = True
                    productos_ids.add(product.id)
                    productos[product.id] = product.stock

            for i, el in enumerate(data['details']):
                if 'id' in el:
                    od = OrderDetail.objects.get(id=el['id'])
                    if od.product.id in productos:
                        productos[od.product.id] = productos[od.product.id] + od.cuantity

                stock = productos[el['product']] - el['cuantity']
                if stock < 0:
                    errores[i]['cuantity'] = "No alcanza el stock del producto {}".format(od.product)
                    error = True

            if error:
                raise serializers.ValidationError({"details": errores})
        if len(productos_ids) == 0:
            raise serializers.ValidationError({"details": "Debe ingresar al menos un producto"})

        return data
