
import socket
import json
import random
import sys
import signal
from protocolo import *
from game import Game

def send_message(sock, msg):
    sock.send(msg.encode('utf-8'))

# buffer global para msgs incompletas
message_buffer = ""

def get_attack_coordinates_with_timeout():
    """
    Solicita coordenadas de ataque com timeout de 1 minuto.
    Se o usuário não responder a tempo, faz um ataque aleatório.
    """
    class TimeoutException(Exception):
        pass
    
    def timeout_handler(signum, frame):
        raise TimeoutException()
    
    def get_random_attack():
        #cordenadas rand
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        return x, y
    
    #windows
    if sys.platform == "win32":
        print("nao")
    
    
    else:
        # linux
        signal.signal(signal.SIGALRM, timeout_handler) #signal pra comunicação entre processos
        signal.alarm(60)  #60 segundos
        
        try:
            while True:
                coords = input("Digite coordenadas x,y (exemplo: 3,5): ").strip()
                
                # fora do formato
                if ',' not in coords:
                    print(" Formato inválido! Use o padrão x,y (exemplo: 3,5)")
                    continue
                
                try:
                    
                    parts = coords.split(',')
                    if len(parts) != 2:
                        print(" Formato inválido! Use exatamente x,y (exemplo: 3,5)")
                        continue
                    
                    x, y = map(int, parts)
                    
                    # Verificar se estão no range válido
                    if not (0 <= x <= 9 and 0 <= y <= 9):
                        print(" Coordenadas devem estar entre 0-9!")
                        continue
                    
                    #coordenada valida
                    signal.alarm(0)  # cncela timeout
                    return x, y, False
                    
                except ValueError:
                    print(" Coordenadas devem ser números! Use o padrão x,y (exemplo: 3,5)")
                    continue
                except Exception as e:
                    print(f" Erro inesperado: {e}. Tente novamente.")
                    continue
        
        except TimeoutException:
            # Timeout - fazer ataque aleatório
            x, y = get_random_attack()
            print(f"\n Timeout! Fazendo ataque aleatório em ({x},{y})")
            return x, y, True

def receive_message(sock):
    """Recebe mensagem do servidor e retorna código e corpo"""
    global message_buffer
    
    try:
        data = sock.recv(8192)
        if not data:
            return None, None
        
        # Adicionar dados ao buffer
        message_buffer += data.decode('utf-8', errors='ignore') #bytes p/string
        
        # Processar mensagens completas no buffer
        while '\n' in message_buffer:
            # Encontrar a primeira mensagem completa
            lines = message_buffer.split('\n', 2)
            if len(lines) >= 2:
                code = lines[0]
                body = lines[1]
                
                # Se há mais dados, manter no buffer
                if len(lines) > 2:
                    message_buffer = '\n'.join(lines[2:])
                else:
                    message_buffer = ""
                
                # Se o body parece ser JSON seguido de outro código, separar
                if body.startswith('{') and '}' in body:
                    json_end = body.find('}') + 1
                    if json_end < len(body):
                        # Há dados após o JSON
                        actual_body = body[:json_end]
                        remaining = body[json_end:]
                        # Adicionar o resto de volta ao buffer
                        message_buffer = remaining + message_buffer
                        return code, actual_body
                
                return code, body
            else:
                # Mensagem incompleta, aguardar mais dados
                break
        
        # Se chegou aqui, não há mensagem completa disponível
        # Tentar novamente na próxima chamada
        return receive_message(sock)
        
    except Exception as e:
        print(f"Erro na recepção: {e}")
        return None, None
    

def main():
    print(" CLIENTE BATALHA NAVAL ")
    print("=" * 40)
    
    #dados de conexão
    host = input("Digite o IP do servidor (ou Enter para localhost): ").strip()
    if not host:
        host = 'localhost'
    
    try:
        port = int(input("Digite a porta (ou Enter para 12345): ").strip() or "12345")
    except:
        port = 12345
    
    print(f"\nConectando a {host}:{port}...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(60)  # timeout para aguardar o segundo jogador
            s.connect((host, port))
            print("✓ Conectado ao servidor!")
            
            # Enviar mensagem de conexão
            init_msg = build_message(INFO, "conectado")
            s.send(init_msg.encode('utf-8'))
            
            # remover timeout 
            s.settimeout(None)

            while True:
                code, body = receive_message(s)
                if not code:
                    print("Conexão encerrada pelo servidor.")
                    break

                # Interpretar códigos do protocolo
                #print(f"[DEBUG] Código recebido: {code}")
                
                if code == ATAQUE_OPONENTE or code == "205":
                    print("\n Sua vez de atacar!")
                    print(" Você tem 1 minuto para atacar, senão será feito um ataque aleatório!")
                    
                    # Usar função com timeout
                    x, y, was_timeout = get_attack_coordinates_with_timeout()
                    
                    # Enviar ataque (seja manual ou automático)
                    attack_msg = build_attack_message(x, y)
                    send_message(s, attack_msg)
                    
                    if was_timeout:
                        print(f" Ataque automático enviado: ({x},{y})")
                    else:
                        print(f"✓ Ataque enviado: ({x},{y})")

                elif code == ESPERANDO_OPONENTE or code == "201":
                    print(" Aguardando ataques do oponente...")

                elif code == ATAQUE_ACERTO or code == "101":
                    print(f" {body}")

                elif code == ATAQUE_FALHOU or code == "100":
                    print(f" {body}")
                    
                elif code in [PORTA_AVIOES, ENCOURACADO, CRUZADOR, SUBMARINO, FRAGATA, TORPEDEIRO]:
                    print(f" {body}")

                elif code == GANHOU or code == "203":
                    print(f" {body}")

                elif code == PERDEU or code == "204":
                    print(f" {body}")
                    
                elif code == FIM_PARTIDA or code == "202":
                    print(f" {body}")
                    break
                    
                elif code == INFO or code == "300":
                    # Mensagens INFO (JSON)
                    try:
                        payload = json.loads(body)
                        message_text = payload.get('text', 'Mensagem do servidor')
                        print(f"\n[Servidor]: {message_text}")
                        
                        # Imprimir mapas se existirem
                        if 'own_map' in payload and 'enemy_map' in payload:
                            Game.print_map(payload["own_map"], "SEU TABULEIRO")
                            Game.print_map(payload["enemy_map"], "TABULEIRO INIMIGO")
                    except json.JSONDecodeError as e:
                        print(f"[Servidor]: {body}")
                        print(f"[DEBUG] Erro JSON: {e}")
                else:
                    print(f"[DEBUG] Código desconhecido {code}: {body}")
                        
    except ConnectionRefusedError:
        print(" Conexão recusada pelo servidor.")
        print(f" Possíveis causas:")
        print(f"   • Servidor não está rodando em {host}:{port}")
        print(f"   • Firewall bloqueando a porta {port}")
        print(f"   • IP {host} incorreto ou inacessível")
        print(f"\n Soluções:")
        print(f"   1. Verifique se ambos estão na mesma rede")
        print(f"   2. Tente com localhost primeiro")
    except socket.timeout:
        print(" Timeout na conexão.")
        print(f" O servidor {host}:{port} não respondeu em 60 segundos")
        print(f" Verifique se o IP está correto e acessível")
    except socket.gaierror as e:
        print(f" Erro de resolução de nome/IP: {e}")
        print(f" O IP {host} não é válido ou não pode ser resolvido")
        print(f" Verifique se o IP está correto")
    except Exception as e:
        print(f" Erro inesperado: {e}")
        print(f" Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    main()
