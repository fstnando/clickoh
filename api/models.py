from django.db import models


class Product(models.Model):
    """
    Model for products
    """
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.name} [{self.stock}]"


class Order(models.Model):
    """
    Model for orders
    """
    date_time = models.DateTimeField()

    def __str__(self):
        return self.date_time.strftime('d/m/Y')

    def get_total(self):
        total = 0.0
        for el in self.orderdetail_set.select_related('product').all():
            total += el.cuantity * el.product.price
        return total

    def update_stock(self):
        for el in self.orderdetail_set.all():
            el.product.stock -= el.cuantity
            el.product.save()

    def reset_stock(self):
        for el in self.orderdetail_set.all():
            el.product.stock += el.cuantity
            el.product.save()


class OrderDetail(models.Model):
    """
    Model for order details
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cuantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.cuantity} - {self.product}"
