# NutriPet/serializers.py
from rest_framework import serializers
from .models import RecomendacionAlimenticia # Ajusta según tu modelo

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionAlimenticia
        fields = ['id', 'nombre_mascota', 'especie', 'edad_meses', 'alergias', 'recomendacion', 'creado']
        read_only_fields = ['recomendacion', 'creado']

    def validate_edad_meses(self, valor):
        if valor < 0:
            raise serializers.ValidationError("La edad de la mascota no puede ser negativa.")
        return valor