#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys

def test_server_connection(host, port):
    """Testa conexão com o servidor"""
    print(f"🔍 Testando conexão com {host}:{port}")
    
    try:
        # Criar socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 segundos timeout
        
        # Tentar conectar
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Conexão bem-sucedida com {host}:{port}")
            return True
        else:
            print(f"❌ Falha na conexão: Código de erro {result}")
            return False
            
    except socket.gaierror as e:
        print(f"❌ Erro DNS/IP: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def test_local_server():
    """Testa se consegue criar servidor local"""
    print("\n🔍 Testando criação de servidor local...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 12345))
        sock.listen(1)
        print("✅ Consegue criar servidor na porta 12345")
        sock.close()
        return True
    except Exception as e:
        print(f"❌ Não consegue criar servidor: {e}")
        return False

def get_local_ip():
    """Obtém IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print("🔧 DIAGNÓSTICO DE REDE - BATALHA NAVAL")
    print("=" * 50)
    
    # Mostrar IP local
    local_ip = get_local_ip()
    print(f"📍 IP local detectado: {local_ip}")
    
    # Testar servidor local
    test_local_server()
    
    # Solicitar IP do servidor para testar
    print("\n" + "=" * 50)
    server_ip = input("Digite o IP do servidor para testar: ").strip()
    if not server_ip:
        server_ip = "localhost"
    
    port = 12345
    
    # Testar conexão
    test_server_connection(server_ip, port)
    
    # Dar dicas adicionais
    print("\n📋 DICAS DE RESOLUÇÃO:")
    print("1. Verifique se o servidor está rodando")
    print("2. Verifique o firewall do Windows")
    print("3. Teste com localhost primeiro")
    print("4. Confirme se estão na mesma rede")
    print("5. Use 'ipconfig' (Windows) ou 'ifconfig' (Linux) para verificar IPs")

if __name__ == "__main__":
    main()
