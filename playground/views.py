from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product,OrderItem,Order

# Create your views here.

def say_hello(request):
    # querset = Product.objects.select_related('collection').filter(collection__title='Beauty')
    queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5]
    return render(request, 'hello.html',{'products':list(queryset)})
