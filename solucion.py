import json
import os
from tabulate import tabulate

def decidir(especie, edad, alergeno):
    """Aplica la regla de decisión de 4 resultados exigida por el plan."""
    # Paso 1: Validar primero el dato inválido (REGLA OBLIGATORIA)
    if edad <= 0 or edad > 20:
        return "ERROR: Dato inválido. La edad debe estar entre 1 y 20 años."
    
    # Paso 2: Rechazo 1 (Especie no soportada)
    elif especie == "Otra especie":
        return "RECHAZADO: Especie no soportada. El sistema solo evalúa perros y gatos."
    
    # Paso 3: Rechazo 2 (Sin alimento para el alérgeno)
    elif alergeno == "Pollo":
        return "RECHAZADO: Sin stock de alimentos compatibles libres de pollo."
    
    # Paso 4: Aceptado (Recomendaciones de marca Josera)
    elif especie in ["Perro", "Gato"] and alergeno in ["Carne", "Trigo", "Sin alergia"]:
        if especie == "Perro":
            if alergeno == "Carne":
                return "ACEPTADO | Opción recomendada: Josera Salmon & Potato (Libre de carne de res)"
            elif alergeno == "Trigo":
                return "ACEPTADO | Opción recomendada: Josera SensiAdult / Josera Optiness (Grain-Free, sin trigo)"
            else:
                return "ACEPTADO | Opción recomendada: Josera Festival (Receta completa para perro)"
        
        elif especie == "Gato":
            if alergeno == "Carne":
                return "ACEPTADO | Opción recomendada: Josera Marinesse (Con salmón, libre de carne de res)"
            elif alergeno == "Trigo":
                return "ACEPTADO | Opción recomendada: Josera NatureCat (100% libre de granos y trigo)"
            else:
                return "ACEPTADO | Opción recomendada: Josera DailyCat (Receta equilibrada para gato)"
            
    else:
        return "RECHAZADO: No cumple con los criterios de recomendación."

def main():
    print("=== SISTEMA NUTRIPET: EVALUACIÓN DE ALIMENTOS ===")
    
    nombre = input("Nombre de la mascota: ").strip()
    
    # Selección de Especie
    print("\nSelecciona la especie:")
    print("1. Perro")
    print("2. Gato")
    print("3. Otra especie")
    opcion_especie = input("Opción (1-3): ").strip()
    
    especies = {"1": "Perro", "2": "Gato", "3": "Otra especie"}
    especie = especies.get(opcion_especie, "Otra especie")
    
    # RECHAZO INMEDIATO: Si elige "Otra especie", cortamos el flujo de preguntas
    if especie == "Otra especie":
        edad = "N/A"
        alergeno = "N/A"
        resultado = decidir(especie, 1, "Sin alergia") # Gatilla directamente el Rechazo 1
    else:
        # Solicitar Edad
        try:
            edad = int(input("\nEdad en años: "))
        except ValueError:
            edad = -1 # Fuerza el dato inválido si ingresan letras/texto
            
        # NUEVO: Si la edad es inválida (<= 0 o >= 20), interrumpe el flujo aquí
        if edad <= 0 or edad > 20:
            alergeno = "N/A"
            resultado = decidir(especie, edad, "Sin alergia")
        else:
            # Solo si la edad es válida, solicita el alérgeno
            print("\nSelecciona el alérgeno principal:")
            print("1. Pollo")
            print("2. Carne")
            print("3. Trigo")
            print("4. Sin alergia")
            opcion_alergeno = input("Opción (1-4): ").strip()
            
            alergenos = {"1": "Pollo", "2": "Carne", "3": "Trigo", "4": "Sin alergia"}
            alergeno = alergenos.get(opcion_alergeno, "Sin alergia")
            
            resultado = decidir(especie, edad, alergeno)
    
    # Nuevo registro
    nuevo_registro = {
        "nombre": nombre,
        "especie": especie,
        "edad": edad,
        "alergeno": alergeno,
        "resultado": resultado
    }
    
    # Leer archivo datos.json si existe
    registros = []
    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []
                
    # Guardar en JSON
    registros.append(nuevo_registro)
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)
        
    # Mostrar en consola usando tabulate
    print("\n" + "="*60)
    print("          RESULTADO DE LA EVALUACIÓN")
    print("="*60)
    print(f"Mascota: {nombre} | Resultado:\n{resultado}\n")
    
    print("=== HISTORIAL ACUMULADO (datos.json) ===")
    print(tabulate(registros, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()