# Informe de Uso de Inteligencia Artificial - NutriPet

## 1. Declaración de Uso
En el desarrollo del proyecto **NutriPet**, se utilizó un modelo de Inteligencia Artificial (Gemini) como asistente de desarrollo para la estructuración de la lógica de negocio, refactorización de código en Python y diseño de componentes en Django.

## 2. Prompts Clave Utilizados

### Prompt 1: Diseño del Plan de Negocio y Regla de Decisión
> *"Ayúdame a diseñar la regla de decisión en Python para evaluar recomendaciones de alimentos de mascotas con 4 resultados posibles: dato inválido (edad <= 0 o > 20), rechazo 1 (especie no soportada), rechazo 2 (sin stock para el alérgeno) y aceptado (con stock compatible). Debe guardar en JSON y mostrarse con tabulate."*

### Prompt 2: Refactorización del Flujo de Interrupción
> *"En el código de consola, quiero que el programa interrumpa la toma de datos inmediatamente si la especie seleccionada es 'Otra especie' o si la edad es un dato inválido, registrando el resultado en datos.json sin pedir los siguientes campos."*

### Prompt 3: Integración con Django
> *"Necesito crear una vista simple en Django que lea el archivo datos.json y renderice una tabla HTML limpia con el historial de evaluaciones en la ruta /resumen/."*

## 3. Validación y Ajustes Realizados por el Desarrollador
* **Ajuste de Rango de Edad:** Se ajustó la regla de decisión para que la edad permitida sea estrictamente de 1 a 20 años, marcando `> 20` como dato inválido.
* **Inclusión de Productos Específicos:** Se personalizó la respuesta del caso Aceptado para incluir productos reales de la marca **Josera** según la especie y alérgeno.
* **Manejo de Errores en JSON:** Se implementó un bloque `try/except` para prevenir caídas de lectura si `datos.json` se encuentra vacío o malformado.

# Registro de Uso de Inteligencia Artificial — NutriPet (Evaluación 2)

## Herramientas Utilizadas
- **IA Generativa / Asistente:** Gemini / ChatGPT (Modelo de asistencia técnica backend)[cite: 3].

## Prompts y Consultas Clave
1. *"¿Cómo estructurar el modelo Django con borrado lógico para reemplazar datos.json?"*[cite: 3]
2. *"¿Cómo implementar las vistas CRUD reutilizando la función decidir() de solucion.py sin duplicar código?"*[cite: 3]
3. *"¿Cómo proteger las vistas en Django usando un decorador personalizado que valide grupos de usuarios en el servidor?"*[cite: 3]

## Correcciones Aplicadas sobre las Respuestas de la IA
1. **Seguridad en la plantilla vs. Servidor:** Inicialmente la IA sugirió ocultar botones con `{% if %}` en el HTML, pero se corrigió para forzar la validación estricta a nivel de servidor con el decorador `@requiere_rol`[cite: 3].
2. **Reorganización del Modelo:** La IA sugirió crear un modelo de roles personalizado, pero se corrigió para utilizar la solución nativa de Django con `django.contrib.auth.models.Group`[cite: 3].
3. **Manejo de Tipos en Migración:** El script de migración inicial fallaba con valores `'N/A'`, por lo que se ajustó el manejo de excepciones `try/except` al convertir enteros[cite: 3].