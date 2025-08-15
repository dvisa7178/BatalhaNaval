# Tipos de mensagem base
ATTACK = "100 ATTACK"
RESPONSE = "200 RESPONSE"
INFO = "300 INFO"

# Códigos de ataque específicos
ATTACK_MISS = "100"      # Erro/Miss
ATTACK_HIT = "101"       # Acerto
ATTACK_CONSECUTIVE = "102"  # Acertos consecutivos
SHIP_CARRIER = "103"     # Afundou porta-aviões
SHIP_BATTLESHIP = "104"  # Afundou encouraçado
SHIP_CRUISER = "105"     # Afundou cruzador
SHIP_SUBMARINE = "106"   # Afundou submarino
SHIP_FRIGATE = "107"     # Afundou fragata
SHIP_TORPEDO = "108"     # Afundou torpedeiro

# Códigos de resposta específicos
RESPONSE_WAITING = "201"  # Aguardando oponente
RESPONSE_GAME_END = "202" # Fim de jogo
RESPONSE_VICTORY = "203"  # Vitória
RESPONSE_DEFEAT = "204"   # Derrota
RESPONSE_TURN = "205"     # Seu turno

# Mapeamento de navios para códigos
SHIP_CODES = {
    "A": SHIP_CARRIER,     # Porta-aviões
    "B": SHIP_BATTLESHIP,  # Encouraçado
    "C": SHIP_CRUISER,     # Cruzador
    "S": SHIP_SUBMARINE,   # Submarino
    "F": SHIP_FRIGATE,     # Fragata
    "T": SHIP_TORPEDO      # Torpedeiro
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
        code = SHIP_CODES.get(ship_type, ATTACK_HIT)
        ship_name = SHIP_NAMES.get(ship_type, "navio")
        return build_message(code, f"Afundou {ship_name} em ({x},{y})")
    else:
        return build_message(ATTACK_HIT, f"Acerto em ({x},{y})")

def build_miss_message(x, y):
    """Constrói mensagem de erro"""
    return build_message(ATTACK_MISS, f"Erro em ({x},{y})")

def build_waiting_message():
    """Constrói mensagem de aguardando oponente"""
    return build_message(RESPONSE_WAITING, "Aguardando ataques do oponente")

def build_turn_message():
    """Constrói mensagem de turno"""
    return build_message(RESPONSE_TURN, "Seu turno! Digite coordenadas x,y para atacar")

def build_victory_message():
    """Constrói mensagem de vitória"""
    return build_message(RESPONSE_VICTORY, "🎉 VOCÊ VENCEU! 🎉")

def build_defeat_message():
    """Constrói mensagem de derrota"""
    return build_message(RESPONSE_DEFEAT, "💥 VOCÊ PERDEU! 💥")

def build_game_end_message():
    """Constrói mensagem de fim de jogo"""
    return build_message(RESPONSE_GAME_END, "Jogo finalizado")

def get_ship_sunk_message(ship_type):
    """Retorna mensagem de navio afundado"""
    ship_name = SHIP_NAMES.get(ship_type, "navio")
    return f"🚢 {ship_name} afundado!"
