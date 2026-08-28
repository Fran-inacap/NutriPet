PROBLEMA

Muchas mascotas tienen alergias o sensibilidades a alimentos, por lo que solo pueden comer ciertas marcas o tipos, pero para llegar al alimento adecuado es un proceso largo y costoso ya que a menudo los dueños deben realizar un ejercicio de prueba y error con distintas comidas y en el proceso comprar sacos de comida que la mascota no puede comer.

SOLUCION

Una aplicación backend en Python que evalúa la especia, edad y alergía o sensibilidad de la mascota para determinar la factibilidad de recomendación y entregar opciones de alimento seguras para la mascota.

REGLA DE DECISIÓN

Dato inválido: la edad de la mascota es menor o igual a 0
RECHAZO 1 (especie no soportada): Selecciona la opción "Otra especie" en el menú desplegable.
RECHAZO 2 (sin alimento para el alérgeno): selecciona un alérgeno específico que no tenga alternativas de alimento sin él presente (por ejemplo, pollo)
ACEPTADO: Selecciona una especie soportada (perro, gato), una edad válida y un alérgeno con stock compatible.

MOSCOW

Temporalmente solo se soportarán las especie de perro y gato.



POC (proof of concept)
