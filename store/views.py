from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review


# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'store/home.html', context)


# ─────────────────────────────────────────────
# PRODUCT LIST
# ─────────────────────────────────────────────
def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    sort = request.GET.get('sort')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if sort == 'low':
        products = products.order_by('price')
    elif sort == 'high':
        products = products.order_by('-price')
    elif sort == 'new':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'store/product_list.html', context)


# ─────────────────────────────────────────────
# PRODUCT DETAIL
# ─────────────────────────────────────────────
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all().order_by('-created_at')
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Review submitted!')
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'reviews': reviews,
        'related': related,
    }
    return render(request, 'store/product_detail.html', context)


# ─────────────────────────────────────────────
# CART
# ─────────────────────────────────────────────
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart')


# ─────────────────────────────────────────────
# CHECKOUT & ORDER
# ─────────────────────────────────────────────
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            total=cart.get_total(),
            payment_method=request.POST.get('payment_method', 'COD'),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Account created.')
            return redirect('home')
    return render(request, 'store/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ─────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────
@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'store/profile.html', {'orders': orders})
