from django.db import models
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

class Planta(models.Model):
    """
    Modelo simplificado que representa uma planta e seus requisitos de cuidado.
    """
    nome = models.CharField(max_length=150)
    especie = models.CharField(max_length=150, blank=True)
    frequencia_rega_dias = models.IntegerField(default=3)
    ultima_rega = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "plantas"

    def __str__(self) -> str:
        return f"{self.nome} ({self.especie})"

def listar_plantas(request: HttpRequest) -> JsonResponse:
    """
    Retorna todas as plantas cadastradas no banco de dados.
    """
    plantas = list(Planta.objects.values("id", "nome", "especie", "frequencia_rega_dias"))
    return JsonResponse(plantas, safe=False, json_dumps_params={"ensure_ascii": False})

@csrf_exempt
def criar_planta(request: HttpRequest) -> JsonResponse:
    """
    Cria um novo registro de planta através de uma requisição POST com dados JSON.
    """
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            if not data.get("nome"):
                return JsonResponse({"erro": "O nome é obrigatório"}, status=400)
            
            try:
                frequencia = int(data.get("frequencia_rega_dias", 3))
                if frequencia <= 0:
                    return JsonResponse({"erro": "A frequência de rega deve ser maior que zero"}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({"erro": "Frequência de rega inválida"}, status=400)

            planta = Planta.objects.create(
                nome=data.get("nome"),
                especie=data.get("especie", "Desconhecida"),
                frequencia_rega_dias=frequencia
            )
            return JsonResponse({"id": planta.id, "status": "criado"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Método não permitido"}, status=405)