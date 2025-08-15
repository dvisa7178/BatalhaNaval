#!/bin/bash

echo "🚢 BATALHA NAVAL - CONFIGURADOR UBUNTU 🚢"
echo "========================================"

# Dar permissões de execução
chmod +x server.py
chmod +x cliente_ubuntu.py

echo "1) Iniciar Servidor"
echo "2) Conectar como Cliente"
echo "3) Sair"
echo
read -p "Escolha uma opção: " opcao

case $opcao in
    1)
        echo "Iniciando servidor..."
        python3 server.py
        ;;
    2)
        echo "Iniciando cliente..."
        python3 cliente_ubuntu.py
        ;;
    3)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        ;;
esac
