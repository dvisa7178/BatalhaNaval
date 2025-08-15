#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
from protocolo import *

def send_message(sock, msg):
    sock.send(msg.encode('utf-8'))
    print(f"[📤] Enviado: {msg}")

# Buffer global para mensagens incompletas
message_buffer = ""

def receive_message(sock):
    global message_buffer
    
    try:
        data = sock.recv(8192)
        if not data:
            return None, None
        
        # Adicionar dados ao buffer
        message_buffer += data.decode('utf-8', errors='ignore')
        
        # Processar mensagens completas no buffer
        while '\n' in message_buffer:
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
                        actual_body = body[:json_end]
                        remaining = body[json_end:]
                        message_buffer = remaining + message_buffer
                        return code, actual_body
                
                return code, body
            else:
                break
        
        # Se não há mensagem completa, aguardar mais dados
        return receive_message(sock)
        
    except Exception as e:
        print(f"Erro na recepção: {e}")
        return None, None

def main():
    print("🚢 CLIENTE SIMPLES DE TESTE 🚢")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            print("✓ Conectado ao servidor!")
            
            # Enviar mensagem inicial obrigatória
            init_msg = build_message(INFO, "Conectando")
            send_message(s, init_msg)
            
            attack_coords = [(1,1), (2,2), (3,3), (4,4), (5,5)]
            attack_index = 0
            
            # Loop principal do jogo
            while True:
                code, body = receive_message(s)
                if not code:
                    print("❌ Conexão perdida!")
                    break
                
                print(f"[INFO] Código: {code} | Corpo: {body}")
                
                # Interpretar códigos do protocolo
                if code == "205":  # RESPONSE_TURN
                    if attack_index < len(attack_coords):
                        x, y = attack_coords[attack_index]
                        attack_index += 1
                        print(f"🎯 Atacando: ({x},{y})")
                        
                        attack_msg = build_attack_message(x, y)
                        send_message(s, attack_msg)
                        time.sleep(0.5)
                    else:
                        print("🎯 Ataques esgotados!")
                        break
                        
                elif code == "201":  # RESPONSE_WAITING
                    print("⏳ Aguardando...")
                    
                elif code in ["100", "101", "103", "104", "105", "106", "107", "108"]:
                    print(f"📊 Resultado do ataque: {body}")
                    
                elif code in ["202", "203", "204"]:
                    print(f"🎮 Fim de jogo: {body}")
                    break
                    
                elif code == "300":  # INFO
                    print(f"📋 Info: {body}")
                    
                else:
                    print(f"❓ Código desconhecido: {code}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
