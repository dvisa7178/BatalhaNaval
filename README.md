## BATALHA NAVAL

## Arquivos Principais

### Core do Jogo:
- `server.py` - Servidor do jogo
- `cliente_ubuntu.py` - Cliente otimizado para Ubuntu
- `game.py` - Lógica do jogo e impressão dos mapas
- `protocolo.py` - Protocolo de comunicação

### Utilitários:
- `start.sh` - Script de inicialização
- `debug_test.py` - Teste standalone

## Como Usar

### 1. Preparar o ambiente:
```bash
chmod +x start.sh
chmod +x server.py
chmod +x cliente_ubuntu.py
```

### 2. Iniciar o servidor:
```bash
python3 server.py
```
O servidor mostrará o IP para conexão.

### 3. Conectar clientes (em outro terminal ou PC):
```bash
python3 cliente_ubuntu.py
```

## Conexão entre PCs diferentes

1. **No PC servidor**: Execute `python3 server.py`
2. **Anote o IP mostrado** (ex: 192.168.1.100)
3. **No PC cliente**: Execute `python3 cliente_ubuntu.py`
4. **Digite o IP do servidor** quando solicitado

## Como Jogar

1. Dois jogadores devem se conectar
2. Cada um vê seu tabuleiro com navios posicionados aleatoriamente
3. No seu turno, digite coordenadas como: `3,5`
4. ✗ = Acerto | ○ = Erro | · = Água
5. Ganhe destruindo todos os navios do oponente!

## Tipos de Navios

- **A** = Porta-aviões (5 casas)
- **B** = Encouraçado (4 casas)  
- **C** = Cruzador (3 casas)
- **S** = Submarino (3 casas)
- **F** = Fragata (2 casas)
- **T** = Torpedeiro (1 casa)

## Resolução de Problemas

### Se os caracteres Unicode não aparecerem corretamente:
Edite `game.py` e troque na linha do cliente:
```python
Game.print_map(payload["own_map"], "SEU TABULEIRO")
```
por:
```python
Game.print_map_simple(payload["own_map"], "SEU TABULEIRO")
```

### Se houver problemas de conexão:
1. Verifique se o firewall permite conexões na porta 12345
2. Confirme que ambos estão na mesma rede
3. Use `ip addr` para verificar o IP correto

