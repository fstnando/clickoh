from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')
    search_fields = ('id', 'name')


class OrderDetailInlines(admin.StackedInline):
    model = OrderDetail
    autocomplete_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'get_cant_products', 'get_cuantity')
    list_filter = ('orderdetail__product', )
    inlines = [OrderDetailInlines]

    def get_cant_products(self, obj):
        return obj.orderdetail_set.all().count()
    get_cant_products.short_description = 'Cant.Products'

    def get_cuantity(self, obj):
        try:
            cant = obj.orderdetail_set.aggregate(cant=Sum('cuantity'))['cant']
        except:
            cant = 0
        return cant
    get_cuantity.short_description = 'Cuantity'

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if 'date_time' not in initial:
            initial['date_time'] = timezone.now()
        return initial

    def save_formset(self, request, form, formset, change):
        if change:
            form.instance.reset_stock()
        super().save_formset(request, form, formset, change)
        form.instance.update_stock()

    def delete_model(self, request, obj):
        obj.reset_stock()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.reset_stock()
        super().delete_queryset(request, queryset)
