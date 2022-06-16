
import numpy as np
from numpy.core.fromnumeric import size


class Board_matrix:
    def __init__(self, size, default=0):
        self.size = size
        self.rows = size[0]
        self.cols = size[1]
        self.points = []
        self.default = default

        if not default:
            self.board = np.zeros((self.size), dtype=np.int16)
        else:
            self.board = np.full((self.size), default)


        # Consts
        self.CLOCK = 1
        self.ANTICLOCK = 0

    def print_board(self):
        for row in self.board:
            for element in row:
                print(f' {element} ', end='')
            print()
        print()

    def transpose_board(self):
        self.board = self.board.transpose()

    def rotate_board(self, dir):
        for point in self.points:
            if dir:
                point.i, point.j = point.j, self.cols-point.i-1
            else:
                point.i, point.j = self.cols-point.j-1, point.i
        self.board = np.rot90(self.board, 1, (dir, abs(1-dir)))

    def grow_board(self, size, diagonal=0):
        
        if not diagonal:
            a = np.full((size[0], self.cols), self.default)
            self. board = np.vstack([a, self.board])
            self.rows += size[0]

            a = np.full((self.rows, size[1]), self.default)
            self. board = np.hstack([a, self.board])
            self.cols += size[1]
        else: 
            a = np.full((size[0], self.cols), self.default)
            self. board = np.vstack([self.board, a])
            self.rows += size[0]

            a = np.full((self.rows, size[1]), self.default)
            self. board = np.hstack([self.board, a])
            self.cols += size[1]

    def displace_board(self, dir=(0,1)):
        for point in self.points:
            point.move(dir)

    def restart_board(self):
        self.board = np.full((self.rows, self.cols), self.default)

    def update_board(self):
        # self.restart_board()
        for point in self.points:
            self.board[point.i, point.j] = point.value


    def __str__(self):
        return f'({self.rows}, {self.cols})'



# ======= POINT CLASS ============
class Point(Board_matrix):
    def __init__(self, parent):
        self.Board_obj = parent
        self.i=None
        self.j=None
        self.value = None
        self.overValue = None
        self.Board_obj.points.append(self)


    def setPoint(self, i, j, value=1):
        self.i = i
        self.j = j
        self.value = value
        self.overValue = self.Board_obj.board[self.i,self.j]
        self.Board_obj.board[self.i,self.j] = self.value
    
    def getPoint(self):
        return (self.i, self.j)

    def moveTo(self, dir):
        self.move((dir[0]-self.i, dir[1]-self.j))

    def move(self, dir):
        self.Board_obj.board[self.i, self.j] = self.overValue

        self.i = (self.i+dir[0])%self.Board_obj.rows
        self.j = (self.j+dir[1])%self.Board_obj.cols
        self.overValue = self.Board_obj.board[self.i, self.j]
        self.Board_obj.board[self.i, self.j] = self.value


    def remove_point(self):
        self.Board_obj.board[self.i,self.j] = self.overValue
        self.Board_obj.points.pop(self.Board_obj.points.index(self))

    def __eq__(self, other):
        if self.i == other.i and self.j == other.j: return True
        else: return False

    def __str__(self):
        return f"({self.i}, {self.j}) = {self.value}"

    def __del__(self):
        self.remove_point()

class Body:
    
    def __init__(self, parent, points):
        self.body_points = points
        self.Board_obj = parent
        self.reference = points[0]
        

    def setPoints(self, coords):
        for i in range(len(self.body_points)):
            self.body_points[i].setPoint(*coords[i])
        
        self.Board_obj.update_board()


    def move(self, dir):
        self.Board_obj.restart_board()
        for point in self.body_points:
            point.i = (point.i+dir[0])%self.Board_obj.rows
            point.j = (point.j+dir[1])%self.Board_obj.cols
        self.Board_obj.update_board()

    def moveTo(self, dir):
        self.move((dir[0]-self.reference.i, dir[1]-self.reference.j))
        





# --------------------------------------
if __name__ == '__main__':
    import time, os
    myBoard = Board_matrix((10,40), default=' ')
    
    myBody = Body(myBoard, [Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard), Point(myBoard)])
    myBody.setPoints(((1,1,'#'), (2,2,'@'), (1,3,'#'), (3,1,'#'), (3,3,'#'), (2,1,'#'), (3,2,'#'), (2,3,'#'), (1,2,'#')))

    # myPoint = Point(myBoard)
    # myPoint.setPoint(2,2,'#')
    
    myBoard.print_board()
    os.system('pause')

    for k in range(40):
        os.system('cls')
        # myPoint.move((0,1))
        myBody.moveTo((3,k))
        myBoard.print_board()
        
        time.sleep(0.1)
    
    os.system('pause')
