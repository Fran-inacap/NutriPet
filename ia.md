# Informe de Uso de Inteligencia Artificial - NutriPet

## 1. Declaración de Uso
En el desarrollo del proyecto **NutriPet**, se utilizó Inteligencia Artificial (Gemini / ChatGPT) como asistente técnico para la estructuración de la lógica de negocio, refactorización de código en Python y diseño de componentes en Django.

---

## 2. Auditoría de Interacciones y Correcciones Aplicadas

### Interacción 1: Seguridad y Protección de Vistas
* **Consulta (Prompt):**
  > "¿Cómo proteger las vistas en Django usando un decorador personalizado que valide grupos de usuarios en el servidor y cómo ocultar los botones de Editar/Eliminar en la plantilla HTML?"
* **Respuesta de la IA:**
  Sugirió validar únicamente en la plantilla HTML con directivas `{% if request.user.is_staff %}` para ocultar las opciones de edición y eliminación según el perfil.
* **Corrección y Justificación Técnica:**
  Se rechazó la validación exclusiva en la plantilla porque un usuario no autorizado podía eludirla ingresando directamente la URL `/editar/1/`. Se implementó el decorador personalizado `@requiere_rol("admin")` en `views.py` para forzar la validación estricta a nivel de servidor.

---

### Interacción 2: Modelo de Usuarios y Gestión de Roles
* **Consulta (Prompt):**
  > "¿Cómo estructurar el modelo Django para manejar roles de usuario y permisos sin complicar la arquitectura?"
* **Respuesta de la IA:**
  Sugirió crear un modelo de roles personalizado extendiendo `AbstractUser` o con una relación `OneToOneField`.
* **Corrección y Justificación Técnica:**
  Se simplificó la arquitectura rechazando el modelo personalizado e implementando la solución nativa de Django mediante `django.contrib.auth.models.Group` ("admin" y "normal"), garantizando mantenibilidad y menor sobrecarga.

---

### Interacción 3: Normalización de Datos en Migración (`cargar_datos.py`)
* **Consulta (Prompt):**
  > "¿Cómo migrar el historial previo de `datos.json` al modelo Django usando un script de carga automatizado?"
* **Respuesta de la IA:**
  Entregó un script que insertaba directamente las cadenas del JSON a la base de datos sin transformación previa.
* **Corrección y Justificación Técnica:**
  El script inicial fallaba al convertir enteros cuando encontraba valores `'N/A'` o textos inconsistentes como `"Otra especie"`, impidiendo que los registros se pudieran editar en `/admin/`. Se agregaron las funciones `mapear_especie()` y `mapear_alergeno()` con manejo de excepciones `try/except` para limpiar los campos y sincronizarlos con los `choices` del modelo Django.

---

### Interacción 4: Estructura del Formulario y Campo Alérgeno
* **Consulta (Prompt):**
  > "¿Cómo capturar el alérgeno en `form.html` sin usar ModelForm pero asegurando que coincida con el motor de reglas?"
* **Respuesta de la IA:**
  Sugirió un campo `<input type="text" name="alergeno">` de texto libre.
* **Corrección y Justificación Técnica:**
  Se reemplazó el `input` por un menú desplegable `<select>` con las 4 opciones normalizadas (`ninguno`, `pollo`, `carne`, `trigo`) para evitar que diferencias tipográficas o de capitalización corrompieran la evaluación en `solucion.py`.