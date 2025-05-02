from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria, Testmonial, RedeSocial, InformacaoContato, Order, OrderItem
from .forms import ProdutoForm
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import ProdutoSerializer, TestmonialsSerializer, OrderSerializer, OrderItemSerializer, OrderCreateSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
# Exemplo de View para listar produtos
def lista_produtos(request, categoria_slug=None):
    produtos = Produto.objects.all()
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = produtos.filter(categoria=categoria)
    return render(request, 'loja/lista_produtos.html', {'produtos': produtos})

def detalhe_produto(request, id, slug):
    produto = get_object_or_404(Produto, id=id, slug=slug)
    return render(request, 'loja/detalhe_produto.html', {'produto': produto})


@api_view(['GET'])
def administracao_produtos(request):
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def criar_produto(request):
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    serializer = ProdutoSerializer(produto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
def api_lista_testmonials(request):
    testmonials = Testmonial.objects.all().order_by('-created_at')
    serializer = TestmonialsSerializer(testmonials, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_detalhe_testmonial(request, id):
    testmonial = get_object_or_404(Testmonial, id=id)
    serializer = TestmonialsSerializer(testmonial)
    return Response(serializer.data)

@api_view(['POST'])
def api_criar_testmonial(request):
    serializer = TestmonialsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def api_editar_testmonial(request, id):
    testmonial = get_object_or_404(Testmonial, id=id)
    serializer = TestmonialsSerializer(testmonial, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_excluir_testmonial(request, id):
    testmonial = get_object_or_404(Testmonial, id=id)
    testmonial.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet for DRF
class TestmonialViewSet(viewsets.ModelViewSet):
    queryset = Testmonial.objects.all().order_by('-created_at')
    serializer_class = TestmonialsSerializer
    @action(detail=False, methods=['GET'])
    def recentes(self, request):
        testmonials_recentes = Testmonial.objects.all().order_by('-created_at')[:5]
        serializer = self.get_serializer(testmonials_recentes, many=True)
        return Response(serializer.data)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['GET'])
    def recentes(self, request):
        orders_recentes = Order.objects.all().order_by('-created_at')[:10]
        serializer = self.get_serializer(orders_recentes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def pendentes(self, request):
        orders_pendentes = Order.objects.filter(status='pending').order_by('-created_at')
        serializer = self.get_serializer(orders_pendentes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def estatisticas(self, request):
        total_orders = Order.objects.count()
        pedidos_por_status = {status: Order.objects.filter(status=status).count() 
                             for status, _ in Order.STATUS_CHOICES}
        
        faturamento_total = Order.objects.filter(status='paid').aggregate(
            total=Sum('total'))['total'] or 0
        
        return Response({
            'total_pedidos': total_orders,
            'pedidos_por_status': pedidos_por_status,
            'faturamento_total': faturamento_total
        })

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        queryset = OrderItem.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order__id=order_id)
        return queryset
def get_serializer_class(self):
    if self.action == 'create':
        return OrderCreateSerializer
    return OrderSerializer
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            
            imagens = request.FILES.getlist('imagens')
            for i, img in enumerate(imagens):
                ProdutoImagem.objects.create(
                    produto=produto,
                    imagem=img,
                    ordem=i
                )
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
        imagem_form = ProdutoImagemForm()
    
    return render(request, 'adicionar_produto.html', {
        'form': form,
        'imagem_form': imagem_form
    })

def contato_json(request):
    try:
        contato = InformacaoContato.objects.first()
        redes = RedeSocial.objects.filter(ativo=True)
        
        data = {
            'endereco': contato.endereco_completo(),
            'email': contato.email,
            'telefone': contato.telefone,
            'redes_sociais': [
                {
                    'tipo': rede.get_tipo_display(),
                    'url': rede.url,
                } for rede in redes
            ]
        }
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=True, methods=['POST'])
    def upload_imagens(self, request, pk=None):
        produto = self.get_object()
        arquivos = request.FILES.getlist('imagens')
        
        for i, arquivo in enumerate(arquivos):
            ordem = ProdutoImagem.objects.filter(produto=produto).count()
            ProdutoImagem.objects.create(
                produto=produto,
                imagem=arquivo,
                ordem=ordem + i
            )
        
        return Response({'status': 'imagens adicionadas'})
    
##View page pedidos

@login_required
def order_details(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)

        if request.user.email != order.user_email and not request.user.is_staff:
            raise Http404("Permission denied")
            
        return render(request, 'order_detail.html', {
            'order': order
        })
    except Exception as e:
        return render(request, 'error.html', {
            'error_message': str(e)
        })
    

@login_required
def order_list(request):
    # Filtrar pedidos com base no perfil do usuário
    if request.user.is_staff:
        # Administradores veem todos os pedidos
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Usuários comuns veem apenas seus próprios pedidos
        orders = Order.objects.filter(user_email=request.user.email).order_by('-created_at')
    
    # Adicionar paginação
    paginator = Paginator(orders, 10)  # 10 pedidos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'order_list.html', {
        'page_obj': page_obj,
        'is_admin': request.user.is_staff,
    })