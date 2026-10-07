import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage")
django.setup()

from django.test import TestCase, Client
from plantas import Planta

class PlantasTestCase(TestCase):
    """
    Conjunto de testes automatizados para verificar as operações do Gestor de Plantas.
    """
    def setUp(self) -> None: 
        self.client = Client()

    def test_fluxo_gerenciamento_plantas(self) -> None:
        payload = {
            "nome": "Samambaia",
            "especie": "Nephrolepis exaltata",
            "frequencia_rega_dias": 2
        }
        response_criar = self.client.post(
            "/criar/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response_criar.status_code, 201)
        self.assertIn("id", response_criar.json())

        response_listar = self.client.get("/")
        self.assertEqual(response_listar.status_code, 200)
        plantas = response_listar.json()
        self.assertEqual(len(plantas), 1)
        self.assertEqual(plantas[0]["nome"], "Samambaia")
        self.assertEqual(plantas[0]["frequencia_rega_dias"], 2)

        response_invalido_nome = self.client.post(
            "/criar/",
            data=json.dumps({"especie": "Ficus"}),
            content_type="application/json"
        )
        self.assertEqual(response_invalido_nome.status_code, 400)

        response_invalido_frequencia = self.client.post(
            "/criar/",
            data=json.dumps({"nome": "Suculenta", "frequencia_rega_dias": -5}),
            content_type="application/json"
        )
        self.assertEqual(response_invalido_frequencia.status_code, 400)