#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import time
from protocolo import *
from game import Game

def send_message(sock, msg):
    sock.send(msg.encode('utf-8'))

def receive_message(sock):
    """Recebe mensagem do servidor e retorna código e corpo"""
    try:
        data = sock.recv(8192)
        if not data:
            return None, None
        
        msg = data.decode('utf-8', errors='ignore')
        
        # Se há múltiplas mensagens, pegar apenas a primeira
        if msg.count('\n') > 1:
            lines = msg.split('\n')
            code = lines[0]
            body = lines[1] if len(lines) > 1 else ""
        else:
            code, body = parse_message(msg)
        
        return code, body
    except Exception as e:
        print(f"Erro na recepção: {e}")
        return None, None

def main():
    print("🚢 TESTE AUTOMATIZADO - CLIENTE 🚢")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            print("✓ Conectado ao servidor!")
            
            # Enviar mensagem inicial obrigatória
            init_msg = build_message(INFO, "Conectando")
            send_message(s, init_msg)
            print("✓ Mensagem inicial enviada!")
            
            # Configurar jogo
            game = Game()
            game.place_ships()
            
            # Lista de ataques automáticos - começar com posições que podem ter navios
            attacks = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2)]
            attack_index = 0
            consecutive_hits = 0  # Contador de acertos consecutivos
            
            # Loop principal do jogo
            while True:
                code, body = receive_message(s)
                if not code:
                    print("❌ Conexão perdida!")
                    break
                
                print(f"\n💬 Código: {code} | {body}")
                
                # Interpretar códigos do protocolo
                if code == RESPONSE_TURN or code == "205":
                    if attack_index < len(attacks):
                        x, y = attacks[attack_index]
                        attack_index += 1
                        print(f"🎯 Atacando automaticamente: ({x},{y})")
                        
                        attack_msg = build_attack_message(x, y)
                        send_message(s, attack_msg)
                        time.sleep(1)  # Dar tempo para processar
                    else:
                        print("🎯 Sem mais ataques automáticos!")
                        break
                        
                elif code == RESPONSE_WAITING or code == "201":
                    print("⏳ Aguardando ataques do oponente...")
                    
                elif code == ATTACK_HIT or code == "101":
                    consecutive_hits += 1
                    print(f"🎯 Acertei! ({consecutive_hits}º acerto consecutivo)")
                    
                elif code == ATTACK_MISS or code == "100":
                    if consecutive_hits > 0:
                        print(f"❌ Errei após {consecutive_hits} acertos consecutivos.")
                        consecutive_hits = 0
                    else:
                        print("❌ Errei.")
                        
                elif code in [SHIP_CARRIER, SHIP_BATTLESHIP, SHIP_CRUISER, SHIP_SUBMARINE, SHIP_FRIGATE, SHIP_TORPEDO]:
                    ship_name = get_ship_sunk_message(code[-1])  # Pega último char do código
                    print(f"💥 AFUNDEI UM NAVIO! {ship_name}")
                    consecutive_hits += 1
                    
                elif code == RESPONSE_VICTORY or code == "203":
                    print(f"� VITÓRIA! {body}")
                    break
                    
                elif code == RESPONSE_DEFEAT or code == "204":
                    print(f"💀 DERROTA! {body}")
                    break
                    
                elif code == RESPONSE_GAME_END or code == "202":
                    print(f"� FIM DE JOGO: {body}")
                    break
                    
                elif code == INFO or code == "300":
                    try:
                        payload = json.loads(body)
                        print(f"🎮 {payload['text']}")
                    except:
                        print(f"🎮 {body}")
                else:
                    print(f"[DEBUG] Código desconhecido: {code}")
                
                # Verificar fim do jogo
                if "venceu" in body.lower() or "perdeu" in body.lower():
                    print(f"\n🎮 FIM DE JOGO: {body}")
                    break
    
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
