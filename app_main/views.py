from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, render, redirect

from app_users.forms import UpdateAccountForm
from .models import Category, Product, Cart
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductListView(ListView):
    model = Product
    template_name = 'app_main/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        search = self.request.GET.get('q', '')

        if search:
            return Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        else:
            return Product.objects.all()


def search_query(request):
    products = Product.objects.all()
    search = request.GET.get('q')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(category__title__icontains=search))
    return render(request, 'app_main/index.html', {'products': products, 'search': search})


class CategoryListView(ListView):
    model = Category
    template_name = 'app_main/categories.html'  # HTML shablon fayli
    context_object_name = 'categories'
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('q', '')

        if search:
            return Category.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        else:
            return Category.objects.all()


class CategoryProductListView(ListView):
    model = Product
    template_name = 'app_main/category_products.html'  # Mahsulotlar ro'yxati shabloni
    context_object_name = 'products'  # Shablon uchun mahsulotlar nomi

    def get_queryset(self):
        # Kategoriya ID asosida mahsulotlarni filtrlaymiz
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_main/detail.html'  # Template file name
    context_object_name = 'product'




# def index(request):
#     query = request.GET.get('q', '')  # Qidiruv so‘zini olish
#     products = Product.objects.all()  # Default bo‘yicha barcha mahsulotlar
#
#     if query:
#         products = products.filter(
#             Q(name__icontains=query) | Q(category__title__icontains=query)
#         )
#
#     return render(request, 'app_main/index.html', {'products': products, 'query': query})


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    template_name = 'app_main/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Foydalanuvchi ma'lumotlarini yuborish
        return context


@login_required(login_url='login')
# def add_to_cart(request, product_id):
#     # Mahsulotni olish
#     product = get_object_or_404(Product, id=product_id)
#
#     # Savatga qo'shish
#     cart_item, created = Cart.objects.get_or_create(
#         user_id=request.user,
#         product_id=product,
#         defaults={'quantity': 1}
#     )
#
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#
#     return JsonResponse({'message': 'Mahsulot savatga qo\'shildi'})
def add_to_cart(request, product_id):
    # Foydalanuvchining tanlagan mahsuloti
    product = get_object_or_404(Product, id=product_id)

    # Yoki mavjud bo'lsa, mavjud savat elementini yangilang
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        # Mavjud bo'lsa, miqdorni oshiramiz
        cart_item.quantity += 1
        cart_item.save()

    return redirect('my_cart')

def delete_from_cart(request, cart_item_id):
    # Savatchadagi mahsulotni topish
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    # Savatchadan o‘chirish
    cart_item.delete()

    # My Cart sahifasiga qaytarish
    return redirect('my_cart')

@login_required(login_url='login')
def change_cart_product_quantity(request, cart_product_id, action):
    cart_product = get_object_or_404(Cart, id=cart_product_id)
    cart_product.quantity += 1 if action == "increment" else -1
    cart_product.save()
    return redirect('cart')


class MyCartView(ListView):
    model = Cart
    template_name = 'app_main/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Foydalanuvchining savat mahsulotlarini olish
        return Cart.objects.filter(user=self.request.user).select_related('product')


def my_cart(request):
    # Foydalanuvchining savat mahsulotlarini olish
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    return render(request, 'app_main/cart.html', {'cart_items': cart_items})


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.get_total_price() for item in items)
    shipping_cost = 0

    context = {
        'cart_items': items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': total_price + shipping_cost,
    }
    return render(request, 'app_main/cart.html', context)


@login_required
def update_account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Foydalanuvchi ma'lumotlari yangilangandan so'ng profil sahifasiga qaytadi
    else:
        form = UpdateAccountForm(instance=request.user)

    return render(request, 'app_main/edit_account.html', {'form': form})