import socket
import threading
import json
from protocolo import *
from game import Game

# Configuração do servidor - aceita conexões de qualquer IP
HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 12345

class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.game = Game()

players = []

def get_local_ip():
    """Obtém o IP local do servidor"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def recv_message(conn):
    try:
        data = conn.recv(4096).decode('utf-8')
        if not data:
            return None, None
        print(f"Dados recebidos: '{data}'")
        return parse_message(data)
    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        return None, None

def send_message(conn, msg):
    try:
        conn.send(msg.encode('utf-8'))
        print(f"Mensagem enviada: {msg[:50]}...")
        # Pequeno delay para evitar concatenação de mensagens
        import time
        time.sleep(0.1)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def send_map_update(player, message_text):
    """Envia mapas atualizados junto com mensagem"""
    def normalize(board):
        return [[cell if cell != "" else "" for cell in row] for row in board]

    payload = {
        "text": message_text,
        "own_map": normalize(player.game.map),
        "enemy_map": normalize(player.game.enemy_view)
    }
    send_message(player.conn, build_message(INFO, json.dumps(payload)))

def send_map(player, message_text):
    """Função compatível que usa send_map_update"""
    send_map_update(player, message_text)

def handle_game():
    p1, p2 = players
    current = 0
    opponent = 1

    send_map(p1, "Jogo iniciado! Você é o Player 1.")
    send_map(p2, "Jogo iniciado! Você é o Player 2.")

    while True:
        attacker = players[current]
        defender = players[opponent]

        # Informar quem é o turno atual usando o novo protocolo
        print(f" Enviando turno para Player {current + 1}")
        send_message(attacker.conn, build_turn_message())
        send_message(defender.conn, build_waiting_message())
        print(f" Aguardando ataque do Player {current + 1}")
        
        code, body = recv_message(attacker.conn)

        # Verificar se é uma mensagem de ataque (aceitar tanto "100" quanto "100 ATTACK")
        if not (code == "100" or code == ATAQUE):
            print(f" Código inválido recebido: '{code}', esperava ataque")
            send_map(attacker, "Esperava mensagem de ataque.")
            continue

        try:
            x, y = map(int, body.strip().split(','))
            if not (0 <= x <= 9 and 0 <= y <= 9):
                send_map(attacker, "Coordenadas devem estar entre 0-9.")
                continue
        except:
            send_map(attacker, "Coordenadas inválidas.")
            continue

        # Executar ataque com informações detalhadas
        hit, ship_type, ship_sunk = defender.game.attack(x, y)
        attacker.game.update_enemy_view(x, y, hit)

        # Construir e enviar mensagens específicas do protocolo
        if hit:
            if ship_sunk:
                # Navio foi afundado
                attacker_msg = build_hit_message(x, y, ship_type, True)
                defender_msg = build_message(SHIP_CODES[ship_type], f"Seu {SHIP_NAMES[ship_type]} foi afundado em ({x},{y})")
                print(f" {SHIP_NAMES[ship_type]} afundado em ({x},{y})!")
            else:
                # Acerto normal
                attacker_msg = build_hit_message(x, y)
                defender_msg = build_message(ATAQUE_ACERTO, f"Seu navio foi atingido em ({x},{y})")
            
            # Enviar mensagens de resultado
            send_message(attacker.conn, attacker_msg)
            send_message(defender.conn, defender_msg)
            
            # Enviar mapas atualizados após o resultado
            send_map_update(attacker, f"Acertou em ({x},{y}) - Continue!")
            send_map_update(defender, f"Atingido em ({x},{y}) - Aguarde")
            
            print(f" Player {current + 1} continua atacando (acerto)")
            
        else:
            # Erro/Miss
            attacker_msg = build_miss_message(x, y)
            defender_msg = build_message(ATAQUE_FALHOU, f"Oponente errou em ({x},{y})")
            
            # Enviar mensagens de erro
            send_message(attacker.conn, attacker_msg)
            send_message(defender.conn, defender_msg)
            
            # Enviar mapas atualizados após o resultado
            send_map_update(attacker, f"Errou em ({x},{y}) - Turno do oponente")
            send_map_update(defender, f"Oponente errou em ({x},{y}) - Seu turno!")
            
            # Alternar turno apenas quando erra
            current, opponent = opponent, current
            print(f"Turno alternado para Player {current + 1} (erro)")

        # Verificar vitória
        if defender.game.all_ships_destroyed():
            # Enviar mensagens de fim de jogo usando o novo protocolo
            send_message(attacker.conn, build_victory_message())
            send_message(defender.conn, build_defeat_message())
            
            # Mensagem final de fim de jogo para ambos
            send_message(attacker.conn, build_game_end_message())
            send_message(defender.conn, build_game_end_message())
            
            print(f"Jogo finalizado! Player {current + 1} venceu!")
            break

        # Após processar o ataque, informar sobre próximo turno
        # O turno só foi alternado se errou (lógica já executada acima)
        print(f"Próximo turno será do Player {current + 1}")

def accept_players():
    local_ip = get_local_ip()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        print("=" * 50)
        print(" SERVIDOR BATALHA NAVAL INICIADO ")
        print("=" * 50)
        print(f"IP do Servidor: {local_ip}")
        print(f"Porta: {PORT}")
        print(f"Aguardando jogadores...")
        print("=" * 50)

        while len(players) < 2:
            conn, addr = s.accept()
            print(f"[+] Jogador conectado de {addr[0]}:{addr[1]}")
            player = Player(conn, addr)

            raw = conn.recv(1024).decode('utf-8')
            code, body = parse_message(raw)
            if code != INFO:
                print(f"[-] Conexão rejeitada: protocolo inválido")
                conn.close()
                continue

            players.append(player)
            print(f"[✓] Jogador {len(players)}/2 conectado (IP: {addr[0]})")
            send_map(player, "Bem-vindo! Aguardando o outro jogador...")

        print("\n[🎮] Ambos jogadores conectados! Iniciando jogo...")
        game_thread = threading.Thread(target=handle_game)
        game_thread.start()

if __name__ == "__main__":
    accept_players()
