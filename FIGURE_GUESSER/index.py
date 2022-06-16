import numpy as np
from numpy.lib.function_base import angle

class Vector:
    def __init__(self, end, start=np.array([0,0])):
        self.vector = np.array(end)-start
        self.x = self.vector[0]
        self.y = self.vector[1]
        self.mod = (self.x**2 + self.y**2)**(1/2)
        self.slope = abs(self.y)/abs(self.x)
        self.alpha = np.arctan(self.slope)/np.pi*180
        if self.x < 0 and self.y > 0: self.alpha += 90
        elif self.x < 0 and self.y < 0: self.alpha += 180
        elif self.x > 0 and self.y < 0: self.alpha = 360-self.alpha

    
    def escalar_product(self, other):
        return ((self.x*other.x)**2 + (self.y*other.y)**2)**(1/2)

    def compare_angle(self, other):
        return np.around(np.arccos((self.escalar_product(other))/(self.mod*other.mod))/np.pi*180, 2)

    def getComponents(self):
        return self.x, self.y

        


    def __str__(self):
        return f"({self.x}, {self.y})"

def getShape(matrix):
    Y, X = np.where(matrix == 1)
    xy = list(zip(X,Y))
    points = []
    while xy:
        pun = [(p[0]**2+p[1]**2)*(p[0]%(len(xy)/2) + p[1]%(len(xy)/2))*2*p[0] for p in xy]
        print(pun)
        points.append(xy.pop(np.argmin(pun)))

    print(points)

    vectors = []
    for i in range(len(points)):
        vectors.append(Vector(points[(i+1)%len(points)], points[i]))
        

    print(*[v for v in vectors])


    if len(vectors) == 3:
        getTriangle(vectors)

    if len(vectors) >= 4:
        getPoligon(vectors)



def getTriangle(vectors):

    angles = [np.around(np.arccos( (vectors[(i+1)%3].mod**2 + vectors[(i+2)%3].mod**2 - vectors[i].mod**2) / (2 * vectors[(i+1)%3].mod * vectors[(i+2)%3].mod) )/np.pi*180, 2) for i in range(3)]

    print(angles)
    

    if 90 in angles:
        print('Its a triangle rectangle')
        return
    elif any([90<angle for angle in angles]):
        print('Its a triangle obtuse')
        return
    else:
        if len(set(angles)) == 2:
            print('Its a triangle isosceles')
            return
        else:
            print('Its a triangle acutangule')
            return

def getPoligon(vectors):
    if len(vectors) == 4:
        if vectors[0].compare_angle(vectors[1]) == 90:
            print('Its a square')
            return
        for i in range(4): 
            if vectors[i].mod == vectors[(i+1)%4].mod and vectors[(i+2)%4].mod == vectors[(i+3)%4].mod and vectors[i].mod != vectors[(i+2)%4].mod:
                print('Its a diamond')
                return
        for i in range(4): 
            if abs(vectors[i].slope) == abs(vectors[(i+2)%len(vectors)].slope) and abs(vectors[(i+1)%len(vectors)].slope) == abs(vectors[(i+3)%len(vectors)].slope): 
                print('Its a trapezoid')
                return
        for i in range(4): 
            print(vectors[i].mod)
            print(vectors[(i+1)%4].mod)
            if vectors[i].mod == vectors[(i+2)%4].mod and vectors[(i+1)%4].mod == vectors[(i+3)%4].mod and vectors[i].mod != vectors[(i+1)%4].mod:
                print('Its a romboid')
                return
        

        print('Its a 4 side poligon')

    if len(vectors) == 5:
        print('its a pentagon')



        
    

matrix = np.array([[0,0,0,0],
                   [0,0,1,0],
                   [1,0,0,0],
                   [1,1,0,0]])

if __name__ == '__main__':
    print(matrix)
    getShape(matrix)

