from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.urls import reverse
from . import models


# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
        ]        
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering = 'product_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist')
        return format_html('<a href="{}?collection__id={}">{}</a>', url, collection.id, collection.product_count)
        # return collection.product_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory' ,'inventory_status', 'collection']
    list_editable = ['unit_price','inventory']
    list_per_page = 10
    list_filter = ['collection','last_update',InventoryFilter]

    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.')

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering = 'order_count')
    def orders(self, customer):
        url = reverse('admin:store_order_changelist')
        return format_html('<a href="{}?customer__id={}">{}</a>', url, customer.id, customer.order_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('order'))

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at', 'customer']
    ordering = ['id']
    autocomplete_fields = ['customer']
