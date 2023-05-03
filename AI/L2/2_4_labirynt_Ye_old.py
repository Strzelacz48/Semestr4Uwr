from typing import Any, Set
import random

from enum import Enum

#kolejka do BFS-a
#queue = []

# - ściana labiryntu, nie można przejść G - cele, w któryh trzeba się znaleźć, B - punkty startowo-docelowe
# S - punkty startowe "spacja" - puste miejsce
#funkcje pomocnicze do ruszania sie po labiryncie
#=================================================================================================
def moveup(x: int, y: int) -> tuple:
    if(iswall(x, y - 1)):
        return (x,y)
    return (x, y - 1)

def movedown(x: int, y: int) -> tuple:
    if(iswall(x, y + 1)):
        return (x,y)
    return (x, y + 1)

def moveleft(x: int, y: int) -> tuple:
    if(iswall(x - 1, y)):
        return (x,y)
    return (x - 1, y)

def moveright(x: int, y: int) -> tuple:
    if(iswall(x + 1, y)):
        return (x,y)
    return (x + 1, y)

# funkcje pomocnicze do sprawdzania czy można przejść na dane pole
#===================================================================================================
def iswall(x: int, y: int) -> bool:
    return labirynt[y][x] == "#"

def isgoal(x: int, y: int) -> bool:
    return labirynt[y][x] == "G"

def isstart(x: int, y: int) -> bool:
    return labirynt[y][x] == "S"

def isblank(x: int, y: int) -> bool:
    return labirynt[y][x] == " "

#funkcja do stworzenia labiryntu
#===================================================================================================
def create_maze() -> list:
    maze = []
    with open("maze.txt") as f:
        for line in f:
            maze.append(line.strip())
    return maze

def init_S_list(maze: list) -> list:
    S_list = []
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "S" or char == "B":
                S_list.append((x, y))
    return S_list

def init_G_list(maze: list) -> list:
    G_list = []
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "G" or char == "B":
                G_list.append((x, y))
    return G_list

def init_B_list(maze: list) -> list:
    B_list = []
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "B":
                B_list.append((x, y))
    return B_list

def all_comandos_in_G() -> bool:
    for commando in commando_list:
        if commando not in G_list:
            return False
    return True

#funkcja do wyświetlania labiryntu
#===================================================================================================
def print_maze(maze: list) -> None:
    for line in maze:
        print(line)

#funkcja uzywajaca BFS do znalezienia sciezki do wyjscia
#===================================================================================================

def all_coomandos_in_G(current_positions) -> bool:
    for commando in current_positions:
        if commando not in G_list:
            return False
    return True


def moveAll(current_positions, move_function):
    for i in range(len(current_positions)):
        x,y = current_positions[i]
        current_positions[i] = move_function(x,y)
    return current_positions    

def BFS() -> bool:

    # tablica krotek w postaci (current_positions, history, moves_made)
    queue = [] 
    
    # lista z kopią obiektu commando_list: list[(int, int)]
    # przechowuje wszystkie stany, w jakich kiedykolwiek bylismy, bez powtorzen
    # może hashset będzie szybszy?
    visited = [commando_list.copy()] # mozna zrobic na zbior zeby bylo szybicej

    # ilość dotychczas dokonanych ruchów
    moves = 0 
    #najpierw zmmniejszyć niepewność
    
    #Funkcja na zmnieszenie niepewności
    
    #sprawdzić czy na wejściu nie jest dobrze
    if all_comandos_in_G():
        return True

    # POWINNO BYĆ LEPIEJ, JEŚLI KOLEJNOŚĆ BEDZIE LOSOWA
    
    queue.append((moveAll(commando_list.copy(), moveup), ["U"], 1))
    queue.append((moveAll(commando_list.copy(), movedown), ["D"], 1))
    queue.append((moveAll(commando_list.copy(), moveleft), ["L"], 1))
    queue.append((moveAll(commando_list.copy(), moveright), ["R"], 1))

    while(queue):
        # sprawdzenie pozycji komandosów, która jeszcze nigdy wcześniej nie wystąpiła:
        current_positions, history, moves_made = queue.pop(0)
        
        #print("queue size: ", len(queue))
        #print("moves made: ", moves_made)

        if moves_made >= MAX_MOVES:
            return False

        # układ pozycji komandosów, jakiego jeszcze nie próbowaliśmy
        if current_positions not in visited: 
            if all_coomandos_in_G(current_positions):
                print("".join(history))
                return True
            
            visited.append(current_positions)
            
            #rand = random(0,3)
            dir = [(moveAll(current_positions.copy(), moveup), history + ["U"], moves_made + 1),
                   (moveAll(current_positions.copy(), movedown), history+ ["D"], moves_made + 1),
                   (moveAll(current_positions.copy(), moveleft), history+ ["L"], moves_made + 1),
                   (moveAll(current_positions.copy(), moveright), history+ ["R"], moves_made + 1)]
            random.shuffle(dir)
            for i in range(4):
                queue.append(dir[i])
            '''
            # wszyscy komandosi równocześnie wykonują ten sam ruch
            queue.append((moveAll(current_positions.copy(), moveup), history + ["U"], moves_made + 1))
            queue.append((moveAll(current_positions.copy(), movedown), history+ ["D"], moves_made + 1))
            queue.append((moveAll(current_positions.copy(), moveleft), history+ ["L"], moves_made + 1))
            queue.append((moveAll(current_positions.copy(), moveright), history+ ["R"], moves_made + 1))        
            '''
    return False    


    



labirynt = create_maze() # lista napisów
S_list = init_S_list(labirynt) # punkty startowe 
commando_list = S_list.copy()  # obecne lokalizacje komandosow
G_list = init_G_list(labirynt) # punkty docelowe
B_list = init_B_list(labirynt) # punkty startowo-docelowe
#print_maze(labirynt)

MAX_MOVES = 150 # constant

BFS()

#Zminiejszanie niepeownośći to takie ruchy które mają zestackować komandosów na jednym polu przy ścianie
#