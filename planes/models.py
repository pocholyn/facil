from django.db import models
from django.core.validators import MinValueValidator
from core.models import AreaVenta
from django.db import IntegrityError

class Plan(models.Model):
    # Relación con el área de venta
    area_venta = models.ForeignKey(
        AreaVenta, 
        on_delete=models.PROTECT,
        verbose_name="Área de Venta"
    )
    
    # Monto del plan (moneda con 2 decimales)
    plan = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Plan ($)"
    )
    
    # Año del plan
    anno = models.IntegerField(
        verbose_name="Año"
    )
    
    # Mes del plan (1-12)
    mes = models.IntegerField(
        choices=[
            (1, "Enero"),
            (2, "Febrero"),
            (3, "Marzo"),
            (4, "Abril"),
            (5, "Mayo"),
            (6, "Junio"),
            (7, "Julio"),
            (8, "Agosto"),
            (9, "Septiembre"),
            (10, "Octubre"),
            (11, "Noviembre"),
            (12, "Diciembre")
        ],
        verbose_name="Mes"
    )
    
    class Meta:
        # Asegurar que no haya duplicados de área-año-mes
        unique_together = ['area_venta', 'anno', 'mes']
        # Ordenar por año, mes y área
        ordering = ['-anno', '-mes', 'area_venta']
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return f"{self.area_venta} - {self.get_mes_display()} {self.anno}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Verificar si ya existe un plan con la misma área, año y mes
        if Plan.objects.filter(
            area_venta=self.area_venta,
            anno=self.anno,
            mes=self.mes
        ).exclude(id=self.id).exists():
            mes_nombre = dict(Plan._meta.get_field('mes').choices)[self.mes]
            raise ValidationError(
                f'Ya existe un plan para el área "{self.area_venta}" en {mes_nombre} de {self.anno}'
            )
