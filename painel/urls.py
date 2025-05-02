from django.urls import path, re_path, include
from . import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import TestmonialViewSet, ProdutoViewSet
from painel import views
app_name = 'painel'

# Configuração do router para ViewSets
router = DefaultRouter()
router.register(r'testmonials', TestmonialViewSet)
router.register(r'produtos', ProdutoViewSet)

# Definindo a documentação da API para o app Loja
schema_view = get_schema_view(
    openapi.Info(
        title="BODE CHIQUE API",
        default_version='v1',
        description="API para gerenciamento de produtos maçônicos",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@lojamacomica.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    # Order detail view
    path('api/orders_detail/<uuid:order_id>/', views.order_detail, name='order_detail'),
    
    # Order views with login required protection
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    
    # Documentação Swagger e ReDoc do app Loja
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API para administração de produtos
    path('api/produtos/', views.administracao_produtos, name='administracao_produtos'),
    path('api/produtos/criar/', views.criar_produto, name='criar_produto'),
    path('api/produtos/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('api/produtos/<int:id>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('produto/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    
    # API para administração dos Depoimentos 
    path('api/testmonials-lista/', views.api_lista_testmonials, name='api_lista_testmonials'),
    path('api/testmonial/<int:id>/', views.api_detalhe_testmonial, name='api_detalhe_testmonial'),
    path('api/testmonial/criar/', views.api_criar_testmonial, name='api_criar_testmonial'),
    path('api/testmonial/<int:id>/editar/', views.api_editar_testmonial, name='api_editar_testmonial'),
    path('api/testmonial/<int:id>/excluir/', views.api_excluir_testmonial, name='api_excluir_testmonial'),
    
    # Administração de informações de contato 
    path('contato/', views.ContatoView.as_view(), name='contato'),
    path('api/contato/', views.contato_json, name='contato_json'),
    
    # API para pedidos
    path('api/orders/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('api/orders/update/', views.OrderUpdateView.as_view(), name='update_order'),
    path('api/orders/<str:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('api/order_list/', views.order_list, name='order_list'),


    # Rotas do Router para ViewSets
    path('api/', include(router.urls)),
]