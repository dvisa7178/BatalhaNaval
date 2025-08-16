import random

class Game:
    def __init__(self):
        self.size = 10  # Aumentado para 10x10 como na imagem
        self.map = [["~"] * self.size for _ in range(self.size)]
        self.enemy_view = [["~"] * self.size for _ in range(self.size)]
        self.ships = {
            "A": 5,  # Porta-aviões
            "B": 4,  # Encouraçado
            "C": 3,  # Cruzador
            "S": 3,  # Submarino
            "F": 2,  # Fragata
            "T": 1   # Torpedeiro
        }
        self.placed_positions = set()
        self.place_ships_randomly()

    def place_ships_randomly(self):
        for symbol, size in self.ships.items():
            placed = False
            while not placed:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                direction = random.choice(["H", "V"])
                coords = []
                for i in range(size):
                    xi = x + i if direction == "H" else x
                    yi = y if direction == "H" else y + i
                    if xi >= self.size or yi >= self.size or (xi, yi) in self.placed_positions:
                        break
                    coords.append((xi, yi))
                else:
                    for xi, yi in coords:
                        self.map[yi][xi] = symbol
                        self.placed_positions.add((xi, yi))
                    placed = True

    def attack(self, x, y):
        """
        Ataca uma posição e retorna informações sobre o resultado
        Returns: (hit, ship_type, ship_sunk)
        """
        if self.map[y][x] in self.ships:
            ship_type = self.map[y][x]
            self.map[y][x] = "X"
            
            # Verificar se o navio foi completamente afundado
            ship_sunk = self.is_ship_sunk(ship_type)
            
            return True, ship_type, ship_sunk
        elif self.map[y][x] == "~":
            self.map[y][x] = "O"
            return False, None, False
        return False, None, False

    def is_ship_sunk(self, ship_type):
        """Verifica se um navio específico foi completamente afundado"""
        for row in self.map:
            for cell in row:
                if cell == ship_type:
                    return False  # Ainda há partes do navio intactas
        return True  # Navio completamente afundado

    def update_enemy_view(self, x, y, result):
        self.enemy_view[y][x] = "X" if result else "O"

    def all_ships_destroyed(self):
        for row in self.map:
            for cell in row:
                if cell in self.ships:
                    return False
        return True

    @staticmethod
    def print_map(board, title):
        """Imprime o mapa em formato de matriz para Ubuntu"""
        print(f"\n{title}")
        print("━" * 42)
        
        # Cabeçalho das colunas
        print("   ", end="")
        for x in range(10):
            print(f" {x} ", end="")
        print()
        
        # Linha separadora
        print("  ┌" + "───┬" * 9 + "───┐")
        
        # Imprimir cada linha
        for y in range(10):
            print(f" {y}│", end="")
            for x in range(10):
                cell = board[y][x] if y < len(board) and x < len(board[y]) else ""
                
                if cell == "" or cell is None or cell == "~":
                    print(" · ", end="")  # Água
                elif cell == "X":
                    print(" ✗ ", end="")  # Acerto
                elif cell == "O":
                    print(" ○ ", end="")  # Erro
                else:
                    print(f" {cell} ", end="")  # Navios
                
                if x < 9:
                    print("│", end="")
            print("│")
            
            # Linha separadora (exceto última)
            if y < 9:
                print("  ├" + "───┼" * 9 + "───┤")
        
        # Linha separadora final
        print("  └" + "───┴" * 9 + "───┘")
        
        # Legenda
        print("Legenda: · = Água | ✗ = Acerto | ○ = Erro")
        print("Navios: A=Porta-aviões B=Encouraçado C=Cruzador S=Submarino F=Fragata T=Torpedeiro\n")
        
    @staticmethod
    def print_map_simple(board, title):
        """Versão simples caso a versão com Unicode não funcione"""
        print(f"\n=== {title} ===")
        
        # Cabeçalho simples
        print("   0 1 2 3 4 5 6 7 8 9")
        
        for y in range(10):
            print(f" {y} ", end="")
            for x in range(10):
                cell = board[y][x] if y < len(board) and x < len(board[y]) else ""
                
                if cell == "" or cell is None:
                    print(". ", end="")
                elif cell == "X":
                    print("X ", end="")
                elif cell == "O":
                    print("O ", end="")
                else:
                    print(f"{cell} ", end="")
            print()
        
        print("Legenda: . = Agua | X = Acerto | O = Erro")
        print("Navios: A=Porta-avioes B=Encouracado C=Cruzador S=Submarino F=Fragata T=Torpedeiro\n")
