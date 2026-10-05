from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from solucion import decidir  # Motor de reglas intacto
from .models import Registro

# --- DECORADOR DE ROLES EN SERVIDOR ---
def tiene_rol(user, *roles):
    return user.groups.filter(name__in=roles).exists() or user.is_superuser

def requiere_rol(*roles):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para realizar esta acción.")
            return redirect("lista")
        return wrapper
    return decorador


# --- VISTAS DE AUTENTICACIÓN ---
def vista_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("lista")
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def vista_logout(request):
    logout(request)
    return redirect("login")


# --- VISTAS PROTEGIDAS CON DECORADOR DE ROL ---
@login_required(login_url="login")
def lista(request):
    """READ: Permitido para todos los usuarios autenticados."""
    registros = Registro.objects.filter(eliminado=False)
    return render(request, "lista.html", {"registros": registros})


@requiere_rol("admin", "normal")
def crear(request):
    error = None
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        especie = request.POST.get("especie", "").strip().lower()
        alergeno = request.POST.get("alergeno", "").strip().lower()
        edad_raw = request.POST.get("edad", "").strip()

        # 1. VALIDACIÓN RIGUROSA EN EL SERVIDOR (Back-end)
        if not nombre:
            error = "El campo nombre es obligatorio."
        elif especie not in ["perro", "gato", "otra"]:
            error = "Especie no válida."
        elif alergeno not in ["ninguno", "pollo", "carne", "trigo"]:
            error = "Alérgeno no válido."
        else:
            try:
                edad = int(edad_raw)
                # Evaluamos la regla de negocio
                resultado = decidir(especie, edad, alergeno)

                # Si decidir() o la edad no son válidos, no guardamos en la BD
                if resultado.startswith("ERROR"):
                    error = resultado
                else:
                    Registro.objects.create(
                        nombre=nombre,
                        especie=especie,
                        edad=edad,
                        alergeno=alergeno,
                        resultado=resultado
                    )
                    return redirect("lista")

            except (ValueError, TypeError):
                error = "La edad debe ser un número entero válido."

    return render(request, "form.html", {
        "accion": "Crear", 
        "error": error,
        "registro": {
            "nombre": request.POST.get("nombre", ""),
            "especie": request.POST.get("especie", ""),
            "edad": request.POST.get("edad", ""),
            "alergeno": request.POST.get("alergeno", "")
        } if request.method == "POST" else None
    })


@requiere_rol("admin")
def editar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    error = None
    
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        especie = request.POST.get("especie", "").strip().lower()
        alergeno = request.POST.get("alergeno", "").strip().lower()
        edad_raw = request.POST.get("edad", "").strip()

        # VALIDACIÓN RIGUROSA EN EL SERVIDOR
        if not nombre:
            error = "El campo nombre es obligatorio."
        elif especie not in ["perro", "gato", "otra"]:
            error = "Especie no válida."
        elif alergeno not in ["ninguno", "pollo", "carne", "trigo"]:
            error = "Alérgeno no válido."
        else:
            try:
                edad = int(edad_raw)
                resultado = decidir(especie, edad, alergeno)

                if resultado.startswith("ERROR"):
                    error = resultado
                else:
                    reg.nombre = nombre
                    reg.especie = especie
                    reg.edad = edad
                    reg.alergeno = alergeno
                    reg.resultado = resultado
                    reg.save()
                    return redirect("lista")

            except (ValueError, TypeError):
                error = "La edad debe ser un número entero válido."

    return render(request, "form.html", {
        "accion": "Editar", 
        "error": error, 
        "registro": reg
    })


@requiere_rol("admin")
def eliminar(request, pk):
    """DELETE: Exclusivo para rol 'admin' mediante método POST."""
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete()
        return redirect("lista")
    return render(request, "confirmar.html", {"registro": reg})