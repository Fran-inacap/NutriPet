# NutriPet/api_views.py
from rest_framework import viewsets
from .models import RecomendacionAlimenticia
from .serializers import RecomendacionSerializer
from .permissions import SoloStaffBorra
from .solucion import calcular_recomendacion # Tu regla de negocio

class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = RecomendacionAlimenticia.objects.all().order_by("-creado")
    serializer_class = RecomendacionSerializer
    permission_classes = [SoloStaffBorra]

    def perform_create(self, serializer):
        # Extraer datos e invocar la regla de negocio
        especie = serializer.validated_data["especie"]
        edad = serializer.validated_data["edad_meses"]
        alergias = serializer.validated_data.get("alergias", "")
        
        resultado = calcular_recomendacion(especie, edad, alergias)
        serializer.save(recomendacion=resultado)