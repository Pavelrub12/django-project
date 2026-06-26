from rest_framework import serializers
from .models import Product, Category, Manufacturer, Cart, CartItem, Profile, OrderItem, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name')
    
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    element_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'quantity', 'element_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Cart
        fields = ['user', 'username', 'create_date', 'items', 'total_price']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ['username', 'email', 'full_name', 'phone', 'address', 'role', 'favorite_category', 'city', 'postal_code']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'created_at', 'address', 'phone', 'total_price', 'items']