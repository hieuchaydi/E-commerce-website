
from rest_framework import serializers
from .models import User, Category, Product, Cart, Order, OrderItem, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    seller = UserSerializer(read_only=True)
    price = serializers.FloatField()  # Ensure price is serialized as a number

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'image', 
                  'category', 'category_id', 'seller', 'created_at', 'updated_at']
        read_only_fields = ['seller']

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'created_at', 'total_price']
        read_only_fields = ['user', 'created_at', 'total_price']

    def get_total_price(self, obj):
        return float(obj.total_price)  # Convert to float for consistency

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    total_price = serializers.FloatField()  # Ensure total_price is serialized as a number

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'shipping_address', 
                  'created_at', 'updated_at', 'items']
        read_only_fields = ['user', 'total_price', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
