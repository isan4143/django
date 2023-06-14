from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,CartItem,Order,OrderItem

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('product_list')

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

def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    # 創建訂單
    order = Order.objects.create(user=request.user)
    
    # 將購物車項目轉換為訂單項目
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
    
    # 清空購物車
    cart_items.delete()
    
    # 可以進行其他處理，例如付款、發送確認郵件等
    
    return redirect('order_confirmation')

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
