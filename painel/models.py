from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(blank=True, default="produtos/no-image.jpg")
    categoria = models.ForeignKey(
        Categoria, related_name="produtos", on_delete=models.CASCADE
    )
    disponivel = models.BooleanField(default=True)
    estoque = models.PositiveIntegerField(default=10)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    destaque = models.BooleanField(default=False)

    class Meta:
        ordering = ("nome",)
        index_together = (("id", "slug"),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detalhe_produto", args=[self.id, self.slug])

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]
        indexes = (models.Index(fields=["id", "slug"]),)


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto, related_name="imagens", on_delete=models.CASCADE
    )
    imagem = models.ImageField(upload_to="produtos/")
    ordem = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ["ordem"]

    def __str__(self):
        return f"Imagem de {self.produto.nome} ({self.ordem})"


class Testmonial(models.Model):
    nome = models.CharField(max_length=200, blank=True)
    testmonial = models.TextField()
    city = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class InformacaoContato(models.Model):
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10, verbose_name="CEP")
    email = models.EmailField()

    telefone_regex = RegexValidator(
        regex=r"^\(\d{2}\)\s\d{5}-\d{4}$",
        message="O telefone deve estar no formato: '(99) 99999-9999'",
    )
    telefone = models.CharField(validators=[telefone_regex], max_length=17)

    class Meta:
        verbose_name = "Informação de Contato"
        verbose_name_plural = "Informações de Contato"

    def __str__(self):
        return f"{self.email} - {self.telefone}"

    def endereco_completo(self):
        return f"{self.endereco}, {self.cidade} - {self.estado}"


class RedeSocial(models.Model):
    TIPOS_CHOICES = (
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("twitter", "Twitter"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
        ("pinterest", "Pinterest"),
        ("tiktok", "TikTok"),
        ("outro", "Outro"),
    )

    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)
    url = models.URLField(verbose_name="URL")

    class Meta:
        verbose_name = "Rede Social"
        verbose_name_plural = "Redes Sociais"
        ordering = ["tipo", "tipo"]

    def __str__(self):
        return f" {self.tipo}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pendente"),
        ("processing", "Em processamento"),
        ("shipped", "Enviado"),
        ("completed", "Concluído"),
        ("canceled", "Cancelado"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=255, blank=True)
    user_email = models.EmailField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido {self.id} - {self.user_email or 'Sem email'} - {self.get_status_display()}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
