import json
import os
from tabulate import tabulate

def decidir(especie, edad, alergeno):
    """Aplica la regla de decisión de 4 resultados exigida por el plan."""
    
    # Estandarización a minúsculas para evitar fallos por mayúsculas/minúsculas
    especie_norm = str(especie).lower().strip()
    alergeno_norm = str(alergeno).lower().strip()

    # Paso 1: Validar primero el dato inválido (REGLA OBLIGATORIA)
    if edad <= 0 or edad > 20:
        return "ERROR: Dato inválido. La edad debe estar entre 1 y 20 años."
    
    # Paso 2: Rechazo 1 (Especie no soportada)
    elif especie_norm in ["otra especie", "otra"]:
        return "RECHAZADO: Especie no soportada. El sistema solo evalúa perros y gatos."
    
    # Paso 3: Rechazo 2 (Sin alimento para el alérgeno pollo)
    elif alergeno_norm == "pollo":
        return "RECHAZADO: Sin stock de alimentos compatibles libres de pollo."
    
    # Paso 4: Aceptado (Recomendaciones de marca Josera)
    # Acepta: "ninguno", "sin alergia", "carne", "trigo"
    elif especie_norm in ["perro", "gato"] and alergeno_norm in ["carne", "carne de res", "trigo", "ninguno", "sin alergia"]:
        if especie_norm == "perro":
            if alergeno_norm in ["carne", "carne de res"]:
                return "ACEPTADO | Opción recomendada: Josera Salmon & Potato (Libre de carne de res)"
            elif alergeno_norm == "trigo":
                return "ACEPTADO | Opción recomendada: Josera SensiAdult / Josera Optiness (Grain-Free, sin trigo)"
            else:
                return "ACEPTADO | Opción recomendada: Josera Festival (Receta completa para perro)"
        
        elif especie_norm == "gato":
            if alergeno_norm in ["carne", "carne de res"]:
                return "ACEPTADO | Opción recomendada: Josera Marinesse (Con salmón, libre de carne de res)"
            elif alergeno_norm == "trigo":
                return "ACEPTADO | Opción recomendada: Josera NatureCat (100% libre de granos y trigo)"
            else:
                return "ACEPTADO | Opción recomendada: Josera DailyCat (Receta equilibrada para gato)"
            
    else:
        return "RECHAZADO: No cumple con los criterios de recomendación."