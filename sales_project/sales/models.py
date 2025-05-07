from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

LINE_CHOICES = [
    ('aditivo', 'Aditivo'),
    ('aqua', 'Aqua'),
    ('aves', 'Aves'),
    ('pet', 'Pet'),
    ('ruminantes', 'Ruminantes'),
    ('suinos', 'Suínos'),
    ('revenda', 'Revenda'),
    ('racoes', 'Rações Vaccinar'),
]

class Sale(models.Model):
    product_line = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    payment_term = models.IntegerField()
    payment_dates = models.JSONField()  # Armazena as datas de pagamento e comissões como JSON
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a venda a um usuário
    buyer = models.CharField(max_length=100)  # <-- Adicione esta linha

    def __str__(self):
        return f"{self.product_line} - {self.value}"
