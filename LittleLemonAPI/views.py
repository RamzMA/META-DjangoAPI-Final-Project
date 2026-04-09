from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    UserSerializer,
    CartSerializer,
    OrderSerializer,
)
from datetime import date

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_delivery_crew(user):
    return user.groups.filter(name='Delivery crew').exists()

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['category']
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def managers(request):
    manager_group = Group.objects.get(name='Manager')

    if request.method == 'GET':
        managers = User.objects.filter(groups=manager_group)
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        manager_group.user_set.add(user)
        return Response({'message': f'{username} added to Manager group'}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def manager_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    manager_group = Group.objects.get(name='Manager')
    manager_group.user_set.remove(user)
    return Response({'message': f'{user.username} removed from Manager group'}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not is_manager(request.user) and not request.user.is_superuser:
        return Response({'message': 'Forbidden'}, status=403)

    delivery_group = Group.objects.get(name='Delivery crew')

    if request.method == 'GET':
        crew = User.objects.filter(groups=delivery_group)
        serializer = UserSerializer(crew, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        delivery_group.user_set.add(user)
        return Response({'message': f'{username} added to Delivery crew'}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew_detail(request, pk):
    if not is_manager(request.user) and not request.user.is_superuser:
        return Response({'message': 'Forbidden'}, status=403)

    user = get_object_or_404(User, pk=pk)
    delivery_group = Group.objects.get(name='Delivery crew')
    delivery_group.user_set.remove(user)
    return Response({'message': f'{user.username} removed from Delivery crew'}, status=200)

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'}, status=200)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or is_manager(user):
            return Order.objects.all()
        if is_delivery_crew(user):
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def create(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'message': 'Cart is empty'}, status=400)

        total = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total=total,
            date=date.today(),
            status=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )

        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or is_manager(user):
            return Order.objects.all()
        if is_delivery_crew(user):
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if is_delivery_crew(user):
            order.status = request.data.get('status', order.status)
            order.save()
            return Response({'message': 'Order status updated'})

        if is_manager(user) or user.is_superuser:
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id:
                crew = get_object_or_404(User, pk=delivery_crew_id)
                order.delivery_crew = crew
            order.status = request.data.get('status', order.status)
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)

        return Response({'message': 'Forbidden'}, status=403)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser and not is_manager(request.user):
            return Response({'message': 'Forbidden'}, status=403)
        return super().delete(request, *args, **kwargs)