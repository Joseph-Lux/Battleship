
from Ship import Ship

class Player:
    # NEEDS TO BE CHECKED
    def __init__(self):
        self.board = [[0 for col in range(10)] for row in range(10)]
        self.ships = []
        self.hits = 17

    # NEEDS TO BE CHECKED
    def addShip(self, ship):
        self.ships.append(ship)
        posX = ship.pos[0]
        posY = ship.pos[1]

        for i in range(ship.length):
            if ship.direction == 'right':
                x = i
                y = 0
            else:
                y = i
                x = 0
            # Assign the index of the ship in ships to the board
            # Such that the second boat in the ships array would 
            # have a row/column of 2's to represent it
            self.board[posX + x][posY + y] = len(self.ships)

    # NEEDS TO BE CHECKED
    def checkHit(self, pos):
        if self.board[pos[0]][pos[1]] > 0:
            self.ships[self.board[pos[0]][pos[1]] - 1].hitsTaken += 1
            self.board[pos[0]][pos[1]] = -self.board[pos[0]][pos[1]]
            self.hits -= 1
            return True
        else:
            self.board[pos[0]][pos[1]] = -6 
            return False
        
            
    




        
