class Line: 
    def __init__(self, x0, y0, x1, y1, c_id):
        self.canvas_id = c_id
        self.x0 = int(x0)
        self.y0 = int(y0)
        self.x1 = int(x1)
        self.y1 = int(y1)

    def getCords(self):
        return self.x0, self.y0, self.x1, self.y1

    def resize(self, r):
        self.x0 = self.x0 - r
        self.y0 = self.y0 - r
        self.x1 = self.x1 + r
        self.y1 = self.y1 + r
    
    def newCenter(self, x, y):
        self.x0 = self.x0 + x
        self.y0 = self.y0 + y
        self.x1 = self.x1 + x
        self.y1 = self.y1 + y
    
    def newCoords(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    
    def move(self, dx, dy):
        dx = int(dx)
        dy = int(dy)
        self.x0 = self.x0 + dx
        self.y0 = self.y0 + dy
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy
    
    def __repr__(self):
        return f"Line({self.x0}, {self.y0}, {self.x1}, {self.y1}, {self.canvas_id})"
    
    def className(self):
        return "Line"
    
class Rectangle:
    def __init__(self, x0, y0, x1, y1, c_id):
        self.canvas_id = c_id
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def getCords(self):
        return self.x0, self.y0, self.x1, self.y1
    
    def newCenter(self, x, y):
        self.x0 = x
        self.y0 = y
        self.x1 = x
        self.y1 = y
    
    def newCoords(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    
    def move(self, dx, dy):
        self.x0 = self.x0 + dx
        self.y0 = self.y0 + dy
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy
    
    def resize(self, r):
        self.x0 = self.x0 - r
        self.y0 = self.y0 - r
        self.x1 = self.x1 + r
        self.y1 = self.y1 + r
    def __repr__(self):
        return f"Rect({self.x0}, {self.y0}, {self.x1}, {self.y1}, {self.canvas_id})"
    
    def className(self):
        return "Rect"

class Circle:
    def __init__(self, x0, y0, x1, y1, c_id):
        self.canvas_id = c_id
        # self.center_x = x
        # self.center_y = y
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        
    def move(self, dx, dy):
        self.x0 = self.x0 + dx
        self.y0 = self.y0 + dy
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy
    
    def newCenter(self, x, y):
        self.center_x = x
        self.center_y = y
    
    def resize(self, r):
        self.x0 = self.x0 - r
        self.y0 = self.y0 - r
        self.x1 = self.x1 + r
        self.y1 = self.y1 + r
    
    def getCords(self):
        return self.x0, self.y0, self.x1, self.y1
    
    def className(self):
        return "Circ"
    
    def __repr__(self):
        return f"Circ({self.center_x}, {self.center_y}, {self.r}, {self.canvas_id})"
    