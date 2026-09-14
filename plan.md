# Plan de Desarrollo - NutriPet

## Apartado de Negocio

### Problema
Muchos dueños de mascotas enfrentan dificultades para encontrar un alimento adecuado cuando sus mascotas tienen sensibilidades o alergias alimentarias. La búsqueda a ciegas provoca gastos elevados en consultas veterinarias y sacos de alimento descartados al causar malestar digestivo o cutáneo en la mascota.

### Solución
Una aplicación backend en Python que evalúa la especie, edad y alérgeno seleccionado mediante interfaz de menús para determinar la factibilidad de recomendación y entregar opciones de alimento seguras.

# Plan de Desarrollo — NutriPet (Evaluación 2)

## Alcance del Proyecto (Matriz MoSCoW)

### Must Have (Obligatorio - Implementado)
- **Base de Datos Relacional:** Migración de `datos.json` a SQLite mediante el modelo `Registro`.
- **Lógica Reutilizada:** Conservación de la regla de decisión `decidir()` intacta desde `solucion.py`.
- **Operaciones CRUD:** Implementación de vistas para listar, crear, editar (recalculando resultado) y eliminar.
- **Borrado Lógico:** Implementación del campo `eliminado` y `fecha_eliminacion` para preservar el historial.
- **Autenticación y Roles:** Sistema de login/logout y control de acceso basado en grupos (`admin`, `normal`, `viewer`) mediante decorador custom en el servidor.
- **Panel de Administración:** Configuración de `list_display`, `list_filter` y `search_fields` en Django Admin.

### Should Have (Deseable)
- Interfaz web estilizada mediante CSS nativo para formularios y mensajes de alerta.

### Could Have (Posible en el futuro)
- Exportación del historial en archivos PDF o Excel.

### Won't Have (Fuera de alcance)
- Registro público de usuarios (los usuarios son gestionados por el administrador)[cite: 3].
- Integración con bases de datos en la nube (PostgreSQL/MySQL).

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