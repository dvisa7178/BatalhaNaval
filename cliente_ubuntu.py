import socket
import json
from protocolo import *
from game import Game

def send_message(sock, msg):
    sock.send(msg.encode('utf-8'))

# bufferpara mensagens incompletas
message_buffer = ""

def receive_message(sock):
    """Recebe mensagem do servidor e retorna cod e corpo"""
    global message_buffer
    
    try:
        data = sock.recv(8192)
        if not data:
            return None, None
        
        # add dados no buffer
        message_buffer += data.decode('utf-8', errors='ignore')
        
        # processa msgs completas no buffer
        while '\n' in message_buffer:
            lines = message_buffer.split('\n', 2)
            if len(lines) >= 2:
                code = lines[0]
                body = lines[1]
                if len(lines) > 2:
                    message_buffer = '\n'.join(lines[2:])
                else:
                    message_buffer = ""

                if body.startswith('{') and '}' in body:
                    json_end = body.find('}') + 1
                    if json_end < len(body):
                        # tem dados dps do JSON
                        actual_body = body[:json_end]
                        remaining = body[json_end:]
                        # add o resto no buffer
                        message_buffer = remaining + message_buffer
                        return code, actual_body
                
                return code, body
            else:
                # msg incompleta
                break
        

        return receive_message(sock)
        
    except Exception as e:
        print(f"Erro na recepção: {e}")
        return None, None

def main():
    print(" CLIENTE BATALHA NAVAL ")
    print("=" * 40)
    
    # Solicitar dados de conexão
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
            # Usar o host informado pelo usuário, não localhost fixo
            s.settimeout(10)  # Timeout de 10 segundos
            s.connect((host, port))
            print("✓ Conectado ao servidor!")
            
            # Enviar mensagem de conexão
            init_msg = build_message(INFO, "conectado")
            s.send(init_msg.encode('utf-8'))

            while True:
                code, body = receive_message(s)
                if not code:
                    print("Conexão encerrada pelo servidor.")
                    break

                # Interpretar códigos do protocolo
                print(f"[DEBUG] Código recebido: {code}")
                
                if code == ATAQUE_OPONENTE or code == "205":
                    print("\n🎯 Sua vez de atacar!")
                    coords = input("Digite coordenadas x,y (exemplo: 3,5): ")
                    try:
                        x, y = map(int, coords.strip().split(','))
                        if 0 <= x <= 9 and 0 <= y <= 9:
                            attack_msg = build_attack_message(x, y)
                            send_message(s, attack_msg)
                            print(f"✓ Ataque enviado: ({x},{y})")
                        else:
                            print("❌ Coordenadas devem estar entre 0-9!")
                            continue
                    except:
                        print("❌ Formato inválido! Use: x,y")
                        continue
                        
                elif code == ESPERANDO_OPONENTE or code == "201":
                    print(" Aguardando ataques do oponente...")
                    
                elif code == ATAQUE_ACERTO or code == "101":
                    print(f" {body}")
                    
                elif code == ATAQUE_FALHOU or code == "100":
                    print(f"❌ {body}")
                    
                elif code in [PORTA_AVIOES, ENCOURACADO, CRUZADOR, SUBMARINO, FRAGATA, TORPEDEIRO]:
                    print(f"💥 {body}")
                    
                elif code == VENCEU or code == "203":
                    print(f"� {body}")
                    
                elif code == PERDEU or code == "204":
                    print(f"💀 {body}")
                    
                elif code == FIM_PARTIDA or code == "202":
                    print(f"🎮 {body}")
                    break
                    
                elif code == INFO or code == "300":
                    # Mensagens INFO antigas (JSON)
                    try:
                        payload = json.loads(body)
                        print(f"\n[Servidor]: {payload['text']}")
                        
                        # Imprimir mapas se existirem
                        if 'own_map' in payload and 'enemy_map' in payload:
                            Game.print_map(payload["own_map"], "SEU TABULEIRO")
                            Game.print_map(payload["enemy_map"], "TABULEIRO INIMIGO")
                    except json.JSONDecodeError:
                        print(f"[Servidor]: {body}")
                else:
                    print(f"[DEBUG] Código desconhecido {code}: {body}")
                        
    except ConnectionRefusedError:
        print("❌ Conexão recusada pelo servidor.")
        print(f"🔍 Possíveis causas:")
        print(f"   • Servidor não está rodando em {host}:{port}")
        print(f"   • Firewall bloqueando a porta {port}")
        print(f"   • IP {host} incorreto ou inacessível")
        print(f"\n💡 Soluções:")
        print(f"   1. Execute 'python diagnose_network.py' para testar")
        print(f"   2. Verifique se ambos estão na mesma rede")
        print(f"   3. Tente com localhost primeiro")
    except socket.timeout:
        print("❌ Timeout na conexão.")
        print(f"🔍 O servidor {host}:{port} não respondeu em 10 segundos")
        print(f"💡 Verifique se o IP está correto e acessível")
    except socket.gaierror as e:
        print(f"❌ Erro de resolução de nome/IP: {e}")
        print(f"🔍 O IP {host} não é válido ou não pode ser resolvido")
        print(f"💡 Verifique se o IP está correto")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    main()

