from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Cart, CartItem
from django.contrib.auth.decorators import login_required



from .models import Item, Category

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Customer, Cart, CartItem, Item

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль покупателя
            customer = Customer.objects.create(user=user)
            # Создаем корзину для пользователя
            Cart.objects.create(customer=customer)
            
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def profile_view(request):
    customer = get_object_or_404(Customer, user=request.user)
    return render(request, 'registration/profile.html', {'customer': customer})

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Cart, CartItem, Item

def get_user_cart(user):
    """Получаем корзину для авторизованного пользователя"""
    customer, created = Customer.objects.get_or_create(user=user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    return cart

@login_required
def cart_view(request):
    """Отображение корзины (только для авторизованных)"""
    cart = get_user_cart(request.user)
    return render(request, "container.html", {"cart": cart})

@login_required
def add_to_cart(request, item_id):
    """Добавление товара в корзину (только для авторизованных)"""
    item = get_object_or_404(Item, id=item_id)
    cart = get_user_cart(request.user)
    
    # Проверяем наличие товара на складе
    if item.stock <= 0:
        messages.error(request, f'Товар "{item.name}" временно отсутствует на складе.')
        return redirect("item_list")
    
    # Проверяем, не превышает ли количество доступный запас
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        if cart_item.quantity >= item.stock:
            messages.warning(request, f'Нельзя добавить больше товара "{item.name}". Доступно: {item.stock} шт.')
            return redirect("item_list")
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество товара "{item.name}" увеличено!')
    else:
        messages.success(request, f'Товар "{item.name}" добавлен в корзину!')

    return redirect("item_list")

@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины (только для авторизованных)"""
    cart = get_user_cart(request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    item_name = cart_item.item.name
    cart_item.delete()
    
    messages.success(request, f'Товар "{item_name}" удален из корзины!')
    return redirect("cart_view")

@login_required
def clear_cart(request):
    """Очистка корзины (только для авторизованных)"""
    cart = get_user_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена!')
    return redirect("cart_view")

@login_required
def update_cart_quantity(request, item_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        cart = get_user_cart(request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity <= 0:
            cart_item.delete()
            messages.success(request, f'Товар "{cart_item.item.name}" удален из корзины!')
        elif new_quantity > cart_item.item.stock:
            messages.error(request, f'Недостаточно товара на складе. Доступно: {cart_item.item.stock} шт.')
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{cart_item.item.name}" обновлено!')
    
    return redirect("cart_view")