from django.db import models
from django.utils import timezone

class Registro(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otra', 'Otra especie'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    edad = models.IntegerField()
    alergeno = models.CharField(max_length=50, blank=True, default='')
    resultado = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)

    # Campos para borrado lógico (no borra físicamente de la base de datos)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - {self.resultado}"

    def soft_delete(self):
        """Marca el registro como eliminado en lugar de borrarlo de la base de datos."""
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()