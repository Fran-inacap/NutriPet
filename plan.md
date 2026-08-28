# Plan de Desarrollo - NutriPet

## Apartado de Negocio

### Problema
Muchos dueños de mascotas enfrentan dificultades para encontrar un alimento adecuado cuando sus mascotas tienen sensibilidades o alergias alimentarias. La búsqueda a ciegas provoca gastos elevados en consultas veterinarias y sacos de alimento descartados al causar malestar digestivo o cutáneo en la mascota.

### Solución
Una aplicación backend en Python que evalúa la especie, edad y alérgeno seleccionado mediante interfaz de menús para determinar la factibilidad de recomendación y entregar opciones de alimento seguras.

### Alcance
* **Dentro del alcance:** Selección de 1 mascota a la vez, validación de datos de entrada mediante menú/formulario, aplicación de regla de decisión de 4 resultados, almacenamiento persistente en `datos.json` y despliegue web en Django.
* **Fuera del alcance:** Cuentas de usuario, autenticación/login, historial de compras, pasarelas de pago e integración con APIs externas.

### Priorización MoSCoW
* **Must (MVP):**
  * Solicitar por consola datos de la mascota: nombre, especie, edad y alérgeno.
  * Ejecutar la regla de decisión con los 4 resultados especificados.
  * Guardar los registros evaluados dentro de `datos.json`.
  * Mostrar el historial estructurado en consola utilizando `tabulate`.
  * Visualizar la tabla de registros en una vista web con Django.
* **Should:** Opción para vaciar o reiniciar el archivo de registros `datos.json`.
* **Could:** Exportar la tabla de recomendaciones acumuladas a formato CSV.
* **Won't:** Cuentas de usuario con contraseña

---

## Apartado Técnico

### Datos de Entrada
* **nombre** (`str`): Nombre de la mascota.
* **especie** (`str`): Opción seleccionada ("Perro", "Gato", "Otra especie").
* **edad** (`int`): Edad en años o meses de la mascota.
* **alergeno** (`str`): Opción seleccionada ("Pollo", "Carne", "Trigo", "Sin alergia").

### Regla de Decisión (4 Resultados)
1. **Dato Inválido:** Si `edad <= 0` o `edad > 20`.
2. **Rechazo 1 (Especie no soportada):** Si `especie` es igual a "Otra especie". Inicialmente solo se soportará perro y gato.
3. **Rechazo 2 (Sin alimento que no posea  el alérgeno):** Si `alergeno` es igual a "Pollo" (no existen alternativas de alimento disponibles libres de pollo).
4. **Aceptado:** Si `especie` es "Perro" o "Gato", `edad > 0` y el `alergeno` cuenta con stock compatible ("Carne", "Trigo" o "Sin alergia").

### Paquete Externo
* **tabulate:** Paquete instalado vía `pip` que permite formatear y presentar la lista de diccionarios en consola con formato de tabla legible.

### Pantalla Web
* **Ruta:** `/resumen/`
* **Contenido:** Una vista de Django (`resumen.html`) que lee el archivo `datos.json` y despliega la tabla con las evaluaciones realizadas (nombre, especie, edad, alérgeno y resultado del sistema).