from rest_framework import viewsets
from .models import Categoria, Produto, Testmonial, RedeSocial, InformacaoContato, Order, OrderItem
from .serializers import (
    CategoriaSerializer, ProdutoSerializer, TestmonialsSerializer, 
    RedesSociaisSerializer, ContatosSerializer, OrderSerializer, OrderItemSerializer, OrderCreateSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class TestmonialViewSet(viewsets.ModelViewSet):
    queryset = Testmonial.objects.all().order_by('-created_at')
    serializer_class = TestmonialsSerializer

class RedesSocialViewSet(viewsets.ModelViewSet):
    queryset = RedeSocial.objects.all()
    serializer_class = RedesSociaisSerializer

class InformacaoContatoViewSet(viewsets.ModelViewSet):
    queryset = InformacaoContato.objects.all()
    serializer_class = ContatosSerializer

# Novos ViewSets para Order e OrderItem
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    lookup_field = 'transaction_id'
    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        transaction_id = self.kwargs.get('transaction_id')
        if transaction_id:
            queryset = queryset.filter(transaction_id=transaction_id)
        return queryset
    def perform_create(self, serializer):
        order = serializer.save()
        products = self.request.data.get('products', [])
        for product_data in products:
            product_id = product_data.get('id')
            quantity = product_data.get('quantity', 1)
            try:
                product = Produto.objects.get(id=product_id)
            except Produto.DoesNotExist:
                continue  

            OrderItem.objects.create(
                order=order,
                product_id=product.id,
                product_name=product.nome,
                price=product.preco,
                quantity=quantity
            )
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        queryset = OrderItem.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order__id=order_id)
        return queryset
    
    