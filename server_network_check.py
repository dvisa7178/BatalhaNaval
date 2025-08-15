#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import platform

def get_network_info():
    """Obtém informações de rede"""
    print("🌐 INFORMAÇÕES DE REDE")
    print("=" * 50)
    
    # IP local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"📍 IP local detectado: {local_ip}")
    except:
        print("❌ Não foi possível detectar IP local")
    
    # Hostname
    try:
        hostname = socket.gethostname()
        print(f"🏠 Hostname: {hostname}")
    except:
        print("❌ Não foi possível obter hostname")
    
    # Sistema operacional
    system = platform.system()
    print(f"💻 Sistema: {system}")
    
    return local_ip if 'local_ip' in locals() else None

def check_port_availability(port=12345):
    """Verifica se a porta está disponível"""
    print(f"\n🔍 VERIFICANDO PORTA {port}")
    print("=" * 50)
    
    try:
        # Tentar criar servidor na porta
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.bind(('0.0.0.0', port))
        sock.listen(1)
        print(f"✅ Porta {port} está disponível")
        sock.close()
        return True
    except socket.error as e:
        print(f"❌ Porta {port} não disponível: {e}")
        return False

def check_firewall_windows():
    """Verifica firewall do Windows"""
    if platform.system() != "Windows":
        return
    
    print(f"\n🛡️  VERIFICAÇÃO DE FIREWALL (WINDOWS)")
    print("=" * 50)
    
    try:
        # Verificar regras do firewall para a porta 12345
        result = subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'show', 'rule', 
            'name=all', 'dir=in', 'protocol=tcp', 'localport=12345'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "12345" in result.stdout:
            print("✅ Regra de firewall encontrada para porta 12345")
        else:
            print("❌ Nenhuma regra de firewall encontrada para porta 12345")
            print("\n💡 Para abrir a porta no firewall (executar como administrador):")
            print('netsh advfirewall firewall add rule name="Batalha Naval" dir=in action=allow protocol=TCP localport=12345')
    except Exception as e:
        print(f"❌ Erro ao verificar firewall: {e}")

def ping_test(target_ip):
    """Testa ping para um IP"""
    print(f"\n🏓 TESTE DE PING PARA {target_ip}")
    print("=" * 50)
    
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "3", target_ip]
    else:
        cmd = ["ping", "-c", "3", target_ip]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print(f"✅ Ping para {target_ip} bem-sucedido")
        else:
            print(f"❌ Ping para {target_ip} falhou")
            print("💡 Verifique se o IP está correto e acessível")
    except Exception as e:
        print(f"❌ Erro no teste de ping: {e}")

def main():
    print("🔧 DIAGNÓSTICO COMPLETO DE REDE")
    print("=" * 50)
    
    # Informações básicas
    local_ip = get_network_info()
    
    # Verificar porta
    check_port_availability()
    
    # Verificar firewall (Windows)
    check_firewall_windows()
    
    # Solicitar IP para testar
    if local_ip:
        print(f"\n🎯 TESTE DE CONECTIVIDADE")
        print("=" * 50)
        target = input(f"Digite um IP para testar conectividade (Enter para {local_ip}): ").strip()
        if not target:
            target = local_ip
        
        ping_test(target)
    
    print(f"\n📋 COMANDOS ÚTEIS:")
    print("=" * 50)
    if platform.system() == "Windows":
        print("• Ver configuração de rede: ipconfig /all")
        print("• Verificar portas: netstat -an | findstr :12345")
        print("• Desabilitar firewall temporariamente para teste")
    else:
        print("• Ver configuração de rede: ifconfig ou ip addr")
        print("• Verificar portas: netstat -an | grep :12345")
        print("• Verificar firewall: sudo ufw status")

if __name__ == "__main__":
    main()
