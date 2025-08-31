import json

def load_app_config():
    """Carrega todas as configurações do arquivo config.json."""
    with open('config.json', 'r') as f:
        return json.load(f)

# Carrega a configuração uma vez quando o módulo é importado
APP_CONFIG = load_app_config()

# Disponibiliza configurações específicas para fácil acesso
REMETENTE_EMAIL = APP_CONFIG.get('REMETENTE_EMAIL')
VALOR_PORTAO = APP_CONFIG.get('VALOR_PORTAO')
TABELA_PRECOS_RAW = APP_CONFIG.get('TABELA_PRECOS', {})

# Processa a tabela de preços (lógica que estava no orcamento_service)
TABELA_PRECOS = {tuple(k.split(';')): v for k, v in TABELA_PRECOS_RAW.items()}