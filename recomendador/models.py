from django.db import models
from django.utils import timezone

class Registro(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otra', 'Otra especie'),
    ]

    ALERGENO_CHOICES = [
        ('ninguno', 'Ninguno'),
        ('pollo', 'Pollo'),
        ('carne', 'Carne de Res'),
        ('trigo', 'Trigo'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    edad = models.IntegerField()
    alergeno = models.CharField(max_length=50, choices=ALERGENO_CHOICES, default='ninguno', blank=True)
    resultado = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)

    # Campos para borrado lógico
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - {self.resultado}"

    def soft_delete(self):
        """Marca el registro como eliminado en lugar de borrarlo físicamente."""
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()