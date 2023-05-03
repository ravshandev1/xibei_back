from rest_framework import generics
from rest_framework.response import Response
from .models import Category, SubCategory, Product, Cart, Users, Order, OrderProduct, Branch, Rate
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, CartSerializer, UserSerializer, \
    OrderSerializer, OrderProductSerializer, RateSerializer, BranchSerializer


class UserDetailView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = Users.objects.filter(telegram_id=pk).exists()
        if user:
            return Response({
                "user_id": Users.objects.get(telegram_id=pk).id,
            })
        else:
            return Response(False)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class RateView(generics.CreateAPIView):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()


class CartItemsView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = Users.objects.get(telegram_id=pk)
        queryset = Cart.objects.filter(user=user.id)
        return queryset


class CartClearView(generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if pk:
            user = Users.objects.filter(telegram_id=pk).first()
            cart_items = Cart.objects.filter(user=user.id)
            for cart in cart_items:
                cart.delete()
            return Response({
                'user_id': user.id,
            })
        else:
            return Response({
                'message': f'{pk}',
            }, status=404)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BranchListView(generics.ListAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()


class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = SubCategory.objects.filter(category=pk)
        return queryset


class SubCategoryDetailView(generics.RetrieveAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Product.objects.filter(subcategory=pk)
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CartCreateListView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class OrderCreateListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderGetView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = Users.objects.get(telegram_id=pk)
        order = Order.objects.filter(user=user.id).order_by('-id')[0]
        return Response({
            'order_id': order.id,

        })


class OrderProductView(generics.ListCreateAPIView):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()
