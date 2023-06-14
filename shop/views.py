from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,CartItem,Order,OrderItem

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # 檢查使用者是否已登入
    if not request.user.is_authenticated:
        # 未登入，導向登入頁面或其他處理方式
        return redirect('login')

    # 將商品添加到購物車
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        # 如果商品已存在於購物車中，增加數量
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)
'''
def place_order(request):
    if request.method == 'POST':
        # 執行下單的邏輯
        order = Order.objects.create(user=request.user)
        # 其他處理訂單的邏輯...

        return redirect('order_confirmation.html')  # 重定向到訂單成功頁面

    else:
        cart_items = CartItem.objects.filter(user=request.user)
        context = {
            'cart_items': cart_items,
        }
        return render(request, 'place_order.html', context)
'''
'''
def place_order(request):
    if request.method == 'POST':
        # 創建新訂單
        order = Order.objects.create(user=request.user)
        order_id = order.id


        # 獲取購物車項目
        cart_items = CartItem.objects.filter(user=request.user)

        # 將購物車項目添加到訂單中
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        # 清空購物車
        cart_items.delete()

        return redirect('order_confirmation')  # 重定向到訂單成功頁面
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        order_total = calculate_order_total(cart_items)
        order=None
        context = {
            'order':order,
            'order_items': cart_items,
            'order_total': order_total
        }
        return render(request, 'place_order.html', context)
'''
def place_order(request):
    if request.method == 'POST':
        # 創建新訂單
        order = Order.objects.create(user=request.user)

        # 獲取購物車項目
        cart_items = CartItem.objects.filter(user=request.user)

        # 將購物車項目添加到訂單中
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        # 清空購物車
        cart_items.delete()

        return redirect('order_success')  # 重定向到訂單成功頁面
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        order_total = calculate_order_total(cart_items)
        context = {
            'order_items': cart_items,
            'order_total': order_total
        }
        return render(request, 'place_order.html', context)
def order_confirmation(request, order_id):
    # 根據訂單 ID 檢索訂單
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order,
    }

    return render(request, 'order_confirmation.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def calculate_order_total(cart_items):
    total = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
    return total

def order_success(request):
    return render(request, 'order_success.html')