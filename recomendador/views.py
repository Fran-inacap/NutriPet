from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, redirect, get_object_or_404
from solucion import decidir  # Regla de decision de la ES1 intacta
from .models import Registro

def lista(request):
    """READ: Muestra los registros que no han sido borrados logicamente."""
    registros = Registro.objects.filter(eliminado=False)
    return render(request, "lista.html", {"registros": registros})

def crear(request):
    """CREATE: Procesa el formulario, aplica decidir() y guarda en la BD."""
    error = None
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        especie = request.POST.get("especie", "").strip()
        alergeno = request.POST.get("alergeno", "").strip()
        
        try:
            edad = int(request.POST.get("edad", ""))
            if not nombre or not especie:
                error = "El nombre y la especie son campos obligatorios."
            else:
                # Reutilizacion directa de la regla de decision
                resultado = decidir(especie, edad, alergeno)
                Registro.objects.create(
                    nombre=nombre,
                    especie=especie,
                    edad=edad,
                    alergeno=alergeno,
                    resultado=resultado
                )
                return redirect("lista")
        except ValueError:
            error = "La edad debe ser un número entero válido."

    return render(request, "form.html", {"accion": "Crear", "error": error})

def editar(request, pk):
    """UPDATE: Modifica un registro y RECALCULA la regla de decision."""
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    error = None

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        especie = request.POST.get("especie", "").strip()
        alergeno = request.POST.get("alergeno", "").strip()
        
        try:
            edad = int(request.POST.get("edad", ""))
            if not nombre or not especie:
                error = "El nombre y la especie son campos obligatorios."
            else:
                reg.nombre = nombre
                reg.especie = especie
                reg.edad = edad
                reg.alergeno = alergeno
                # Recalcular el resultado con decidir() para evitar datos inconsistentes
                reg.resultado = decidir(especie, edad, alergeno)
                reg.save()
                return redirect("lista")
        except ValueError:
            error = "La edad debe ser un número entero válido."

    return render(request, "form.html", {"accion": "Editar", "registro": reg, "error": error})

def eliminar(request, pk):
    """DELETE: Realiza el borrado logico del registro."""
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete()
        return redirect("lista")
    return render(request, "confirmar.html", {"registro": reg})