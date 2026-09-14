import os
from django.contrib.auth.models import User, Group

# Crear grupos requeridos por la pauta
roles = ["admin", "normal", "viewer"]
for r in roles:
    Group.objects.get_or_create(name=r)

# Crear usuario lector de prueba
lector_pass = os.environ.get("PASS_LECTOR", "Lector2026!")
user_lector, created = User.objects.get_or_create(username="lector")
if created:
    user_lector.set_password(lector_pass)
    user_lector.save()

grupo_viewer = Group.objects.get(name="viewer")
user_lector.groups.add(grupo_viewer)

print("¡Grupos ('admin', 'normal', 'viewer') y usuario 'lector' configurados exitosamente!")