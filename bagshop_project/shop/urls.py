from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    # Главная и каталог
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Корзина
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Заказы
    path('checkout/', views.checkout, name='checkout'),
    
    # Аутентификация
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Профиль
    path('profile/', views.profile_view, name='profile'),
    
    # API
    path('api/', include(router.urls)),
    path('api/me/', views.api_me, name='api_me'),
    path('api-auth/', include('rest_framework.urls')),

    path('settings/', views.settings_view, name='settings'),
]