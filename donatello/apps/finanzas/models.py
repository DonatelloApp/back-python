from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Finanza(models.Model):
    TIPO_CHOICES = [
        ('income', 'Ingreso'),
        ('spend', 'Gasto'),
    ]
    id_finanza = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    id_usuario = models.IntegerField()
    #id_usuario = models.ForeignKey(User, on_delete=models.CASCADE) lo quito porque el idusuario viene del backend java, por lo tanto no es necesario q este relacionado con el user de admin de django
    motivo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Finanza #{self.id_finanza}: {self.tipo} - ${self.monto}"

    def clean(self):
        super().clean()
        if self.tipo == 'spend':
            if not self.motivo:
                raise ValidationError('Motivo es requerido si el tipo es "Gasto".')
            if not self.descripcion:
                raise ValidationError('Descripcion es requerida si el tipo es "Gasto".')
        else:
            self.motivo = None
            self.descripcion = None