import json
from recomendador.models import Registro

try:
    with open("datos.json", encoding="utf-8") as f:
        datos = json.load(f)
        for r in datos:
            # Convertir la edad a numero de forma segura
            edad_raw = r.get("edad", 1)
            try:
                edad_val = int(edad_raw)
            except (ValueError, TypeError):
                edad_val = 1  # Valor por defecto si dice 'N/A' o texto

            Registro.objects.create(
                nombre=r.get("nombre", "Sin nombre"),
                especie=r.get("especie", "otra"),
                edad=edad_val,
                alergeno=r.get("alergeno", ""),
                resultado=r.get("resultado", "")
            )
    print("¡Datos de datos.json migrados exitosamente a la base de datos!")
except Exception as e:
    print(f"Error al migrar datos: {e}")