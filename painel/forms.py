from django import forms
from .models import Produto, ProdutoImagem, Order, OrderItem, Testmonial, InformacaoContato, RedeSocial
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'slug', 'categoria', 'descricao', 'preco', 'disponivel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

class ProdutoImagemForm(forms.ModelForm):
    imagens = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),
        required=False
    )
    class Meta:
        model = ProdutoImagem
        fields = ['imagem', 'ordem']

class TestmonialForm(forms.ModelForm):
    class Meta:
        model = Testmonial
        fields = ['nome', 'cargo', 'empresa', 'texto', 'avaliacao', 'imagem']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user_email', 
            'cep', 'estado', 'cidade', 'bairro', 'rua', 'numero', 'complemento',
            'subtotal', 'shipping_cost', 'total', 
            'payment_id', 'transaction_id', 'status'
        ]
        widgets = {
            'status': forms.Select(choices=[
                ('pending', 'Pendente'),
                ('processing', 'Em processamento'),
                ('shipped', 'Enviado'),
                ('completed', 'Concluído'),
                ('canceled', 'Cancelado')
            ])
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product_id', 'product_name', 'price', 'quantity']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = InformacaoContato
        fields = ['endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email']

class RedeSocialForm(forms.ModelForm):
    class Meta:
        model = RedeSocial
        fields = ['tipo', 'url', 'ativo']



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'price', 'quantity']

# Form para criar um OrderItem vinculado a um Order específico
class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'price', 'quantity']

# FormSet para gerenciar múltiplos OrderItems de um Order
OrderItemFormSet = forms.inlineformset_factory(
    Order, 
    OrderItem,
    form=OrderItemInlineForm,
    extra=1,
    can_delete=True
)