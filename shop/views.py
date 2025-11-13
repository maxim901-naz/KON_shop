from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Cart, CartItem
from django.contrib.auth.decorators import login_required



from .models import Item, Category

def item_list(request):
    """
    Главная страница - ВСЕ товары
    URL: /
    """
    items = Item.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'items': items,
        'categories': categories,
        'title': 'Все товары'
    }
    return render(request, 'item_list.html', context)

def category_detail(request, slug):
    """
    Товары определенной категории
    URL: /category/slug/
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    items = Item.objects.filter(category=category, is_available=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'category': category,
        'items': items,
        'categories': categories,
        'title': category.name
    }
    return render(request, 'item_list.html', context)

def item_detail(request, pk):
    """
    Детальная страница товара
    URL: /item/1/
    """
    item = get_object_or_404(Item, pk=pk, is_available=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'item': item,
        'categories': categories,
    }
    return render(request, 'item_detail.html', context)

def home(request):
    return render(request,"home.html")

def info(request):
    return render(request,"info.html")

def get_cart(request):
    """Получаем корзину по сессии"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()  # Создаём сессию, если её нет
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_view(request):
    """Отображение корзины"""
    cart = get_cart(request)
    return render(request, "container.html", {"cart": cart})

def add_to_cart(request, item_id):
    """Добавление товара в корзину"""
    item = get_object_or_404(Item, id=item_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")

def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.delete()
    
    return redirect("cart_view")

def clear_cart(request):
    """Очистка корзины"""
    cart = get_cart(request)
    cart.items.all().delete()
    return redirect("cart_view")