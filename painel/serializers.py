from rest_framework import serializers
from .models import (
    Categoria, Produto, ProdutoImagem, Testmonial, RedeSocial,
    InformacaoContato, Order, OrderItem
)

# CATEGORIAS E PRODUTOS

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoImagem
        fields = ['id', 'imagem', 'ordem']

class ProdutoSerializer(serializers.ModelSerializer):
    imagens = ProdutoImagemSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

# TESTEMUNHOS E CONTATO

class TestmonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testmonial
        fields = '__all__'

class RedesSociaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedeSocial
        fields = '__all__'

class ContatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoContato
        fields = '__all__'

# PEDIDOS

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'created_at', 'updated_at', 'status',
            'payment_id', 'transaction_id', 'cep', 'estado', 'cidade', 'bairro',
            'rua', 'numero', 'complemento', 'subtotal', 'shipping_cost', 'total', 'items'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'user', 'user_email', 'status', 'payment_id', 'transaction_id',
            'cep', 'estado', 'cidade', 'bairro', 'rua', 'numero', 'complemento',
            'subtotal', 'shipping_cost', 'total', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        order = Order.objects.create(**validated_data)

        if not items_data:
            produtos = Produto.objects.all() 

            for produto in produtos:
                OrderItem.objects.create(
                    order=order,
                    product_id=produto.id,
                    product_name=produto.nome,
                    price=produto.preco,
                    quantity=1, 
                )

        return order



class OrderItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    produto_preco = serializers.ReadOnlyField(source='produto.preco')
    produto_imagem = serializers.ImageField(source='produto.imagem_principal', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'produto', 'produto_nome', 'produto_preco', 
                 'produto_imagem', 'quantidade', 'preco', 'subtotal']
        read_only_fields = ['subtotal']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'email', 'telefone', 'endereco', 
                 'cidade', 'estado', 'cep', 'status', 'status_display',
                 'total', 'created_at', 'updated_at', 'items',
                 'created_at_formatted', 'updated_at_formatted']
    
    def get_created_at_formatted(self, obj):
        if obj.created_at:
            return f"{obj.created_at.day} de {self.get_month_name(obj.created_at.month)} de {obj.created_at.year}"
        return None
    
    def get_updated_at_formatted(self, obj):
        if obj.updated_at:
            return f"{obj.updated_at.day} de {self.get_month_name(obj.updated_at.month)} de {obj.updated_at.year}"
        return None
    
    def get_month_name(self, month_number):
        months = [
            'janeiro', 'fevereiro', 'março', 'abril', 
            'maio', 'junho', 'julho', 'agosto', 
            'setembro', 'outubro', 'novembro', 'dezembro'
        ]
        return months[month_number - 1]