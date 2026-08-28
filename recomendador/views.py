from django.shortcuts import render

# Create your views here.
import json
import os
from django.shortcuts import render

def resumen_view(request):
    registros = []
    ruta_json = "datos.json"
    
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []

    return render(request, "resumen.html", {"registros": registros})