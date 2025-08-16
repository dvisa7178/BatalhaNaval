# Tipos de mensagem base
ATAQUE = "100 ATAQUE"
RESPOSTA = "200 RESPOSTA"
INFO = "300 INFO"

# Códigos de ataque 
ATAQUE_FALHOU = "100"      # errou
ATAQUE_ACERTO = "101"       # acertou
ATAQUES_SEQ = "102"  # acertos em sequencia
PORTA_AVIOES = "103"     # afundou porta avioes
ENCOURACADO = "104"  # afundou encouraçado
CRUZADOR = "105"     # afundou cruzador
SUBMARINO = "106"   # afundou submarino
FRAGATA = "107"     # afundou fragata
TORPEDEIRO = "108"     #afundou torpedeiro

# Códigos de resposta 
ESPERANDO_OPONENTE = "201"  # esperando oponente atacar
FIM_PARTIDA = "202" # fim do jogo
VENCEU = "203"  # ganhou
PERDEU = "204"   # perdeu
ATAQUE_OPONENTE = "205"     # teu turno

# Mapeamento de navios para códigos
SHIP_CODES = {
    "A": PORTA_AVIOES,     # porta avioes
    "B": ENCOURACADO,  # encouraçado
    "C": CRUZADOR,     # cruzador
    "S": SUBMARINO,   # submarino
    "F": FRAGATA,     # fragata
    "T": TORPEDEIRO      # torpedeiro
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
    """cria msg de ataque"""
    return build_message("100", f"{x},{y}")

def build_hit_message(x, y, ship_type=None, sunk=False):
    """cria msg de sucesso"""
    if sunk and ship_type:
        code = SHIP_CODES.get(ship_type, ATAQUE_ACERTO)
        ship_name = SHIP_NAMES.get(ship_type, "navio")
        return build_message(code, f"Afundou {ship_name} em ({x},{y})")
    else:
        return build_message(ATAQUE_ACERTO, f"Acerto em ({x},{y})")

def build_miss_message(x, y):
    """cria msg de erro"""
    return build_message(ATAQUE_FALHOU, f"Erro em ({x},{y})")

def build_waiting_message():
    return build_message(ESPERANDO_OPONENTE, "Aguardando ataques do oponente")

def build_turn_message():
    return build_message(ATAQUE_OPONENTE, "Seu turno! Digite coordenadas x,y para atacar")

def build_victory_message():
    """ cria msg de vitroia"""
    return build_message(VENCEU, "🎉 VOCÊ VENCEU! 🎉")

def build_defeat_message():
    """cria msg derrota"""
    return build_message(PERDEU, "💥 VOCÊ PERDEU! 💥")

def build_game_end_message():
    """msg  fim de jogo"""
    return build_message(FIM_PARTIDA, "Jogo finalizado")

def get_ship_sunk_message(ship_type):
    """msg navio afundado"""
    ship_name = SHIP_NAMES.get(ship_type, "navio")
    return f"🚢 {ship_name} afundado!"
