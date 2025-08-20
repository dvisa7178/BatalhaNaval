# Tipos de mensagem base
ATAQUE = "100 ATAQUE"
RESPOSTA = "200 RESPOSTA"
INFO = "300 INFO"

# Códigos de ataque específicos
ATAQUE_FALHOU = "100"      # Erro/Miss
ATAQUE_ACERTO = "101"       # Acerto
ATAQUES_SEQ = "102"  # Acertos consecutivos
PORTA_AVIOES = "103"     # Afundou porta-aviões
ENCOURACADO = "104"  # Afundou encouraçado
CRUZADOR = "105"     # Afundou cruzador
SUBMARINO = "106"   # Afundou submarino
FRAGATA = "107"     # Afundou fragata
TORPEDEIRO = "108"     # Afundou torpedeiro

# Códigos de resposta específicos
ESPERANDO_OPONENTE = "201"  # Aguardando oponente
FIM_PARTIDA = "202" # Fim de jogo
GANHOU = "203"  # Vitória
PERDEU = "204"   # Derrota
ATAQUE_OPONENTE = "205"     # Seu turno

# Mapeamento de navios para códigos
SHIP_CODES = {
    "A": PORTA_AVIOES,     # Porta-aviões
    "B": ENCOURACADO,  # Encouraçado
    "C": CRUZADOR,     # Cruzador
    "S": SUBMARINO,   # Submarino
    "F": FRAGATA,     # Fragata
    "T": TORPEDEIRO      # Torpedeiro
}

# Nomes dos navios
SHIP_NAMES = {
    "A": "Porta-aviões",
    "B": "Encouraçado", 
    "C": "Cruzador",
    "S": "Submarino",
    "F": "Fragata",
    "T": "Torpedeiro"
}

def build_message(code, body):
    return f"{code}\n{body}"

def parse_message(raw_msg):
    lines = raw_msg.split('\n', 1)
    code = lines[0]
    body = lines[1] if len(lines) > 1 else ""
    return code, body

def build_attack_message(x, y):
    """Constrói mensagem de ataque com coordenadas"""
    return build_message("100", f"{x},{y}")

def build_hit_message(x, y, ship_type=None, sunk=False):
    """Constrói mensagem de acerto"""
    if sunk and ship_type:
        code = SHIP_CODES.get(ship_type, ATAQUE_ACERTO)
        ship_name = SHIP_NAMES.get(ship_type, "navio")
        return build_message(code, f"Afundou {ship_name} em ({x},{y})")
    else:
        return build_message(ATAQUE_ACERTO, f"Acerto em ({x},{y})")

def build_miss_message(x, y):
    """Constrói mensagem de erro"""
    return build_message(ATAQUE_FALHOU, f"Erro em ({x},{y})")

def build_waiting_message():
    """Constrói mensagem de aguardando oponente"""
    return build_message(ESPERANDO_OPONENTE, "Aguardando ataques do oponente")

def build_turn_message():
    """Constrói mensagem de turno"""
    return build_message(ATAQUE_OPONENTE, "Seu turno! Digite coordenadas x,y para atacar")

def build_victory_message():
    """Constrói mensagem de vitória"""
    return build_message(GANHOU, "🎉 VOCÊ VENCEU! 🎉")

def build_defeat_message():
    """Constrói mensagem de derrota"""
    return build_message(PERDEU, "💥 VOCÊ PERDEU! 💥")

def build_game_end_message():
    """Constrói mensagem de fim de jogo"""
    return build_message(FIM_PARTIDA, "Jogo finalizado")

def get_ship_sunk_message(ship_type):
    """Retorna mensagem de navio afundado"""
    ship_name = SHIP_NAMES.get(ship_type, "navio")
    return f" {ship_name} afundado!"
