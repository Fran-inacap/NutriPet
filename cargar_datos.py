import json
import os
import django

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NutriPet.settings')
django.setup()

from recomendador.models import Registro
from solucion import decidir

def mapear_especie(especie_raw):
    """
    Normaliza la cadena de especie del JSON a los choices exactos del modelo:
    'perro', 'gato' o 'otra'.
    """
    if not especie_raw:
        return 'otra'
    
    val = str(especie_raw).lower().strip()
    if 'perro' in val:
        return 'perro'
    elif 'gato' in val:
        return 'gato'
    else:
        return 'otra'

def mapear_alergeno(alergeno_raw):
    """
    Normaliza el alérgeno del JSON a los choices del modelo:
    'ninguno', 'pollo', 'carne' o 'trigo'.
    """
    if not alergeno_raw:
        return 'ninguno'
    
    val = str(alergeno_raw).lower().strip()
    if 'pollo' in val:
        return 'pollo'
    elif 'carne' in val:
        return 'carne'
    elif 'trigo' in val:
        return 'trigo'
    else:
        return 'ninguno'

def cargar_datos():
    ruta_json = 'datos.json'
    
    if not os.path.exists(ruta_json):
        print(f"Error: No se encontró el archivo {ruta_json}")
        return

    # 1. Limpiar registros previos con datos inconsistentes
    borrados, _ = Registro.objects.all().delete()
    print(f"Se eliminaron {borrados} registros antiguos e inconsistentes de la Base de Datos.")

    # 2. Leer JSON e insertar datos normalizados
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    creados = 0
    for item in datos:
        nombre = item.get('nombre', 'Sin Nombre')
        especie = mapear_especie(item.get('especie', ''))
        alergeno = mapear_alergeno(item.get('alergeno', ''))
        
        try:
            edad = int(item.get('edad', 0))
        except (ValueError, TypeError):
            edad = 0

        # Recalculamos el resultado usando el motor de reglas estandarizado
        resultado = decidir(especie, edad, alergeno)

        Registro.objects.create(
            nombre=nombre,
            especie=especie,
            edad=edad,
            alergeno=alergeno,
            resultado=resultado
        )
        creados += 1

    print(f"¡Éxito! Se han importado correctamente {creados} registros con valores mapeados.")

if __name__ == '__main__':
    cargar_datos()