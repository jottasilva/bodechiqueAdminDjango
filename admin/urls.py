from django.contrib import admin 
from django.urls import path, include 
from rest_framework import routers 
from painel.api import CategoriaViewSet, ProdutoViewSet, TestmonialViewSet, RedesSocialViewSet, InformacaoContatoViewSet, OrderViewSet 
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from rest_framework.permissions import AllowAny 
from django.conf import settings 
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Definindo a documentação da API (Swagger/ReDoc) 
schema_view = get_schema_view( 
    openapi.Info( 
        title="Documentação da API", 
        default_version='v1', 
        description="Endpoints da Loja", 
    ), 
    public=True, 
    permission_classes=(AllowAny,), 
) 
 
# Registrando as rotas da API 
router = routers.DefaultRouter() 
router.register(r'categorias', CategoriaViewSet) 
router.register(r'produtos', ProdutoViewSet) 
router.register(r'testmonials', TestmonialViewSet) 
router.register(r'redes-sociais', RedesSocialViewSet) 
router.register(r'contato', InformacaoContatoViewSet) 
router.register(r'orders', OrderViewSet) 
 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)),   
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
        #Rotas para autenticação
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)