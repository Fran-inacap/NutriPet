from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from recomendador.models import Registro
from solucion import decidir

class MotorReglasTestCase(TestCase):
    """1. Pruebas unitarias para los 4 resultados de la función decidir()"""

    def test_1_dato_invalido(self):
        """Edad fuera de rango (<= 0 o > 20) debe retornar ERROR"""
        res_negativo = decidir("perro", -5, "ninguno")
        res_excedido = decidir("perro", 25, "ninguno")
        self.assertTrue(res_negativo.startswith("ERROR"))
        self.assertTrue(res_excedido.startswith("ERROR"))

    def test_2_rechazo_especie_no_soportada(self):
        """Especie no soportada ('otra') debe retornar RECHAZADO"""
        res = decidir("otra", 3, "ninguno")
        self.assertTrue(res.startswith("RECHAZADO"))
        self.assertIn("Especie no soportada", res)

    def test_3_rechazo_sin_stock_alergeno(self):
        """Alérgeno pollo debe retornar RECHAZADO por falta de stock"""
        res = decidir("perro", 3, "pollo")
        self.assertTrue(res.startswith("RECHAZADO"))
        self.assertIn("Sin stock", res)

    def test_4_aceptado_recomendacion(self):
        """Caso válido debe retornar ACEPTADO con sugerencia"""
        res = decidir("perro", 3, "ninguno")
        self.assertTrue(res.startswith("ACEPTADO"))


class SeguridadYRolesTestCase(TestCase):
    """2. Pruebas para verificar el control de acceso según el rol del usuario"""

    def setUp(self):
        self.client = Client()
        
        # Crear grupos de permisos
        self.grupo_normal = Group.objects.create(name="normal")
        self.grupo_admin = Group.objects.create(name="admin")

        # Crear usuario con rol 'normal' (no autorizado para editar)
        self.user_normal = User.objects.create_user(username="usernormal", password="password123")
        self.user_normal.groups.add(self.grupo_normal)

        # Registro inicial en la BD
        self.registro = Registro.objects.create(
            nombre="Fido Original", especie="perro", edad=3, alergeno="ninguno", resultado="ACEPTADO"
        )

    def test_rechazo_rol_no_autorizado(self):
        """Un usuario sin rol 'admin' no debe poder modificar datos en la base de datos"""
        self.client.login(username="usernormal", password="password123")
        
        # Intentar modificar el registro vía POST a la vista de edición
        self.client.post(f"/editar/{self.registro.pk}/", {
            "nombre": "Fido Hackeado",
            "especie": "gato",
            "edad": 5,
            "alergeno": "trigo"
        })
        
        # Consultar la base de datos para asegurar que NO sufrió ningún cambio
        reg_db = Registro.objects.get(pk=self.registro.pk)
        self.assertEqual(reg_db.nombre, "Fido Original")
        self.assertEqual(reg_db.especie, "perro")


class BorradoLogicoTestCase(TestCase):
    """3. Pruebas para verificar el borrado lógico en el modelo"""

    def setUp(self):
        self.registro = Registro.objects.create(
            nombre="Pelusa", especie="gato", edad=2, alergeno="ninguno", resultado="ACEPTADO"
        )

    def test_borrado_logico(self):
        """El registro no se elimina de la base de datos, solo cambia su estado 'eliminado'"""
        # Simular borrado lógico
        self.registro.eliminado = True
        self.registro.save()

        # Verificar que el registro aún existe en la base de datos física
        reg_db = Registro.objects.get(pk=self.registro.pk)
        self.assertIsNotNone(reg_db)
        self.assertTrue(reg_db.eliminado)