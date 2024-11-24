from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (ProductListView, CategoryListView, CategoryProductListView, ProductDetailView, AccountView,
                    search_query, add_to_cart, update_account, MyCartView, my_cart, delete_from_cart)

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),  # Umumiy mahsulotlar ro'yxati
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:category_id>/', CategoryProductListView.as_view(), name='category_products'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('account/', AccountView.as_view(), name='account'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('cart/', MyCartView.as_view(),  name='my_cart'),
    path('update-account/', update_account, name='update_account'),
    path('delete-from-cart/<int:cart_item_id>/', delete_from_cart, name='delete_from_cart'),
    path('my-cart/', my_cart, name='my_cart'),
    path('search?/', search_query, name='search')

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)