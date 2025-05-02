from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Categoria, Produto, ProdutoImagem, Testmonial,RedeSocial, InformacaoContato, Order,OrderItem
class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 3  
@admin.register(Categoria)
class CategoriaAdmin(VersionAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Produto)
class ProdutoAdmin(VersionAdmin):
    list_display = ['nome', 'slug', 'preco', 'disponivel', 'estoque', 'destaque', 'criado', 'atualizado']
    list_filter = ['disponivel', 'destaque', 'criado', 'atualizado', 'categoria']
    list_editable = ['preco', 'disponivel', 'estoque', 'destaque']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome', 'descricao']
    inlines = [ProdutoImagemInline]

@admin.register(Testmonial)
class TestmonialAdmin(VersionAdmin):
    list_display = ['nome','testmonial','city' ,'created_at','updated_at']
    

@admin.register(InformacaoContato)
class InformacaoContatoAdmin(VersionAdmin):
    list_display = ('email', 'telefone', 'cidade', 'estado')
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
@admin.register(RedeSocial)
class RedeSocialAdmin(VersionAdmin):
    list_display = ('tipo', 'url')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product_id', 'product_name', 'price', 'quantity']
    readonly_fields = ['product_id', 'product_name', 'price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user_email', 'user']
    readonly_fields = ['id', 'created_at', 'updated_at', 'subtotal', 'total']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'user', 'user_email', 'status', 'created_at', 'updated_at')
        }),
        ('Endereço de Entrega', {
            'fields': ('cep', 'estado', 'cidade', 'bairro', 'rua', 'numero', 'complemento')
        }),
        ('Informações de Pagamento', {
            'fields': ('payment_id', 'transaction_id')
        }),
        ('Valores', {
            'fields': ('subtotal', 'shipping_cost', 'total')
        }),
    )

    def has_add_permission(self, request):
       
        return True

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['product_name', 'product_id', 'order__id', 'order__user_email']
    readonly_fields = ['order']
    
    def has_add_permission(self, request):
        return True


