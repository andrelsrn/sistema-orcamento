import pytest
import json
from src.gerador_pdf import formatar_portoes


def test_formatar_portoes_single_gate():
    portoes_json = json.dumps({"portao_1": "single"})
    assert formatar_portoes(portoes_json) == "1 Single Gate"

def test_formatar_portoes_double_gate():
    portoes_json = json.dumps({"portao_1": "double"})
    assert formatar_portoes(portoes_json) == "1 Double Gate"

def test_formatar_portoes_multiplos_gates():
    portoes_json = json.dumps({"portao_1": "single", "portao_2": "double", "portao_3": "single"})
    # A implementação atual garante a ordem "Single" e depois "Double"
    assert formatar_portoes(portoes_json) == "2 Single Gates, 1 Double Gate"

def test_formatar_portoes_plural():
    portoes_json = json.dumps({"portao_1": "double", "portao_2": "double"})
    assert formatar_portoes(portoes_json) == "2 Double Gates"

def test_formatar_portoes_sem_portao():
    assert formatar_portoes("{}") == "Nenhum"
    assert formatar_portoes(None) == "Nenhum"
    assert formatar_portoes("") == "Nenhum"

def test_formatar_portoes_json_invalido():
    # A função deve retornar a string original se o JSON for inválido
    assert formatar_portoes("json invalido") == "json invalido"
