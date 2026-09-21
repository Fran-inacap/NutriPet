# Plan de Desarrollo - NutriPet

## Apartado de Negocio

### Problema
Muchos dueños de mascotas enfrentan dificultades para encontrar un alimento adecuado cuando sus mascotas tienen sensibilidades o alergias alimentarias. La búsqueda a ciegas provoca gastos elevados en consultas veterinarias y sacos de alimento descartados al causar malestar digestivo o cutáneo en la mascota.

### Solución
Una aplicación web en Django que evalúa la especie, edad y alérgeno seleccionado para determinar la factibilidad de recomendación y entregar opciones de alimento seguras de la línea Josera.

---

# Plan de Desarrollo — NutriPet (Evaluación 2)

## Alcance del Proyecto (Matriz MoSCoW)

### Must Have (Obligatorio - Implementado)
- **Base de Datos Relacional:** Migración de `datos.json` a SQLite mediante el modelo `Registro`.
- **Lógica Reutilizada:** Conservación del motor de reglas `decidir()` en `solucion.py`.
- **Operaciones CRUD:** Vistas para listar, crear, editar (recalculando el resultado) y eliminar.
- **Borrado Lógico:** Uso del campo `eliminado` para preservar la integridad del historial.
- **Autenticación y Roles:** Sistema de autenticación con control de acceso por grupos (`admin` y `normal`) mediante el decorador personalizado `@requiere_rol` a nivel de servidor.
- **Panel de Administración:** Configuración de `list_display`, `list_filter` y `search_fields` en Django Admin con mapeo de choices compatible.

### Should Have (Deseable - Implementado)
- Interfaz web estilizada con CSS para formularios, mensajes de alerta y tablas.

### Could Have (Posible en el futuro)
- Exportación del historial a archivos PDF o Excel.

### Won't Have (Fuera de alcance)
- Registro público de usuarios (los usuarios son creados y gestionados directamente por el administrador).
- Integración con bases de datos en la nube (PostgreSQL/MySQL).

---

## Apartado Técnico

### Datos de Entrada
* **nombre** (`str`): Nombre de la mascota.
* **especie** (`str`): Opción seleccionada (`"perro"`, `"gato"`, `"otra"`).
* **edad** (`int`): Edad en años de la mascota (rango válido: 1 a 20).
* **alergeno** (`str`): Opción seleccionada (`"ninguno"`, `"pollo"`, `"carne"`, `"trigo"`).

### Regla de Decisión (4 Resultados)
1. **Dato Inválido:** Si `edad <= 0` o `edad > 20`. Las vistas impiden guardar estos registros en la base de datos.
2. **Rechazo 1 (Especie no soportada):** Si `especie` es igual a `"otra"`. Solo se soportan perros y gatos.
3. **Rechazo 2 (Sin stock para alérgeno):** Si `alergeno` es `"pollo"` (no hay stock de alimentos hipoalergénicos libres de pollo).
4. **Aceptado:** Si `especie` es `"perro"` o `"gato"`, `edad` está en el rango válido y el `alergeno` es `"carne"`, `"trigo"` o `"ninguno"`.

#### Pantalla Web Principal
* **Ruta:** `/registros/`
* **Vista / Plantilla:** `lista.html` (Vista protegida `lista` en `recomendador/views.py`).
* **Contenido:** Despliega la tabla interactiva con el historial de evaluaciones leídas desde la base de datos (nombre, especie, edad, alérgeno y resultado del sistema), aplicando el control de acceso y opciones según el rol del usuario autenticado.