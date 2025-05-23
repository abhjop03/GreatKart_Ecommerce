from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.


def store(request, category_slug=None):
    print("Category slug:", category_slug)
    products = None
    category = None
    
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        
    context = {
        'products': products,
        'product_count': product_count,
    }
    print("Products:", products)
    print("Product count:", product_count)
    return render(request, 'store/store.html', context=context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
    }
    print("Category slug:", category_slug)
    print("Product slug:", product_slug)
    print("Single product:", single_product)
    return render(request, 'store/product_detail.html', context=context)


