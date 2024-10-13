from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import json
# from layout import setup_layout
# todo
'''
------------------------------------------------------------------------
Projekt 1
Wymagania na najwyższą ocenę:

    Rysowanie trzech prymitywów: linii, prostokątu, okręgu
    Podawanie parametrów rysowania za pomocą pola tekstowego (wpisanie parametrów w pola tekstowe i zatwierdzenie przyciskiem)
    Rysowanie przy użyciu myszy (definiowanie punktów charakterystycznych kliknięciami)
    Przesuwanie przy użyciu myszy (uchwycenie np. za krawędź i przeciągnięcie)
    Zmiana kształtu / rozmiaru przy użyciu myszy (uchwycenie za punkty charakterystyczne i przeciągnięcie)
    Zmiana kształtu / rozmiaru przy użyciu pola tekstowego (zaznaczenie obiektu i modyfikacja jego parametrów przy użycia pola tekstowego)
    Serializacja i deserializacja narysowanych obiektów (zapis i odczyt z pliku)

Uwagi:

    Można wykorzystać biblioteki do rysowania.

TODO:
    zmiana kształtu przy uzyciu myszy i pola tesktowego
    połaczenie pola tekstowego z wybranym kształtem
    resizing linii

------------------------------------------------------------------------
Projekt 2
Wymagania na najwyższą ocenę:

    Wczytywanie i wyświetlanie plików graficznych w formacie PPM P3,
    Wczytywanie i wyświetlanie plików graficznych w formacie PPM P6,
    Wydajny sposób wczytywania plików (blokowy zamiast bajt po bajcie),
    Wczytywanie plików JPEG,
    Zapisywanie wczytanego pliku w formacie JPEG,
    Możliwość wyboru stopnia kompresji przy zapisie do JPEG,
    Skalowanie liniowe kolorów,
    Powiększanie obrazu i przy dużym powiększeniu możliwość przesuwania oraz wyświetlanie wartości pikseli R,G,B na każdym widocznym pikselu,
    Obsługa błędów (komunikaty w przypadku nieobsługiwanego formatu pliku oraz błędów w obsługiwanych formatach plików).

Uwagi:

    Zabronione stosowanie bibliotek do wczytywania plików PPM
    Dozwolone stosowanie bibliotek do wczytywania plików JPEG

------------------------------------------------------------------------

'''

class Line: 
    def __init__(self, x0, y0, x1, y1, c_id):
        self.canvas_id = c_id
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

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
        self.x0 = self.x0 + x
        self.y0 = self.y0 + y
        self.x1 = self.x1 + x
        self.y1 = self.y1 + y
    
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
    def __init__(self, x, y, r, c_id):
        self.canvas_id = c_id
        self.center_x = x
        self.center_y = y
        self.x0 = x - r
        self.y0 = y - r
        self.x1 = x + r
        self.y1 = y + r
        self.r = r
        
    def newCenter(self, x, y):
        self.center_x = x
        self.center_y = y
    
    def resize(self, r):
        self.x0 = self.center_x - r
        self.y0 = self.center_y - r
        self.x1 = self.center_x + r
        self.y1 = self.center_y + r
        self.r = self.r + r
    
    def getCords(self):
        return self.x0, self.y0, self.x1, self.y1
    
    def className(self):
        return "Circ"
    
    def __repr__(self):
        return f"Circ({self.center_x}, {self.center_y}, {self.r}, {self.canvas_id})"
    
    
class Paint:
    def __init__(self, canvas):
        self.canvas = canvas          # canvas
        self.shapes = []              # list of drawed shapes
    
        self.click_x = None           # click x
        self.click_y = None           # click y
        self.selected_shape = None    # shape selected for moving and scaling
        self.selected_action = None   # draw, move & scale action from buttons
        self.combo_shape = "Line"     # shape choosen for drawing
        
        self.first_point_x = None       # first point 
        self.first_point_y = None     
        self.second_point_x = None      # second point 
        self.second_point_y = None
        
        canvas.bind("<Button-1>", self.onMouse1)                # mouse 1 click bind 
        canvas.bind("<Button-3>", self.onMouse3)                # mouse 3 click bind
        canvas.bind("<MouseWheel>", self.onScroll)                  
        canvas.bind("<ButtonRelease-1>", self.onReleaseMouse1)  # mouse 1 release bind
        canvas.bind("<ButtonRelease-3>", self.onReleaseMouse3)  # mouse 3 release bind
        
    def setClickXY(self, x, y):
        self.click_x = x
        self.click_y = y 
        print("click", self.click_x, self.click_y)      
        
    def clearDrawingPoints(self):
        self.first_point_x = None
        self.first_point_y = None
        self.second_point_x = None
        self.second_point_y = None
        print("points cleared")
    
    def clearSelectedShape(self):
        if(self.selected_shape == None):
            return
        id = self.selected_shape.canvas_id
        self.canvas.tag_unbind(id, "<B1-Motion>")
        if(self.selected_shape.className() != "Line"):
            self.canvas.itemconfig(id, outline = "black", width = 1)
        self.selected_shape = None
        print("selected shape cleared")


    def setFirstPointXY(self, x, y):
        self.first_point_x = x
        self.first_point_y = y
        print("first point", self.first_point_x, self.first_point_y)
    def setSecondPointXY(self, x, y):
        self.second_point_x = x
        self.second_point_y = y
        print("second point", self.second_point_x, self.second_point_y)
        
    def onMouse1(self, event):
        x,y = event.x, event.y
        self.setClickXY(x,y)
        if(self.selected_action == "select"):
            self.mouseClickSelect(event)
        if(self.selected_action == "draw"):
            self.mouseClickDraw(event)
                        
    
    def mouseClickDraw(self, event):
        x,y = event.x, event.y
        self.setClickXY(x,y)                    # point needed for dragging elements
        if(self.first_point_x == None):
            self.setFirstPointXY(x,y)
        elif(self.second_point_x == None and self.first_point_x != None):
            self.setSecondPointXY(x,y)
            
        if(self.first_point_x != None and self.second_point_x != None):
            x1 = self.first_point_x
            y1 = self.first_point_y
            x2 = self.second_point_x
            y2 = self.second_point_y
            if(self.combo_shape == "Line"):
                self.drawLineEntry(x1, y1, x2, y2)
            elif(self.combo_shape == "Rectangle"):
                self.drawRectEntry(x1, y1, x2, y2)
            elif(self.combo_shape == "Circle"):
                self.drawCircleEntry(x,y, radius = 10, mouse = True, x2 = x2, y2 = y2)
            self.clearDrawingPoints()
    

    def mouseClickSelect(self, event):
        x,y = event.x, event.y
        if(self.selected_shape == None):
            clicked_items = self.canvas.find_closest(x,y)
            print("clicked items ",clicked_items)
            for item_id in clicked_items:
                for shape in self.shapes:
                    if shape.canvas_id == item_id:
                        self.selected_shape = shape
                        break
                print("selected shape ", self.selected_shape.canvas_id)
                self.canvas.tag_bind(item_id, "<B1-Motion>", self.onDragM1)
                if(self.selected_shape.className() != "Line"):
                    self.canvas.itemconfig(item_id, outline = "red", width = 2)
                break
        else:
            pass
    
    def onMouse3(self, event):
        x,y = event.x, event.y
        # self.setClickXY(x,y)
        
    
    def onReleaseMouse1(self, event):
        if self.selected_shape != None:
            #canvas.tag_unbind(self.selected_shape.canvas_id, "<B1-Motion>")
            pass
            
        self.setClickXY(None, None)
    
    def onReleaseMouse3(self, event):
        self.clearDrawingPoints()
        self.clearSelectedShape()
        self.setClickXY(None, None)
    
    def onScroll(self, event):
        if(self.selected_shape == None):
            return
        if event.delta > 0: # scroll up
            self.selected_shape.resize(1)
        elif event.delta < 0: # scroll down
            self.selected_shape.resize(-1)   
        
        
        x1,y1,x2,y2 = self.selected_shape.getCords()
        canvas.coords(self.selected_shape.canvas_id, x1,y1,x2,y2)
    
    
    def actionDraw(self):
        self.selected_action = "draw"
        print("selected_action: ", self.selected_action)
        
    def actionMove(self):
        self.selected_action = "select"
        print("selected_action: ", self.selected_action)

    def comboShape(self, shape):        
        self.combo_shape = shape
        print("ComboBox shape: ", self.combo_shape)

    def onDragM1(self, event):
        dx = event.x - self.click_x
        dy = event.y - self.click_y
           
        canvas.move(self.selected_shape.canvas_id, dx,dy)
        
        self.setClickXY(event.x, event.y)
        self.selected_shape.newCenter(event.x, event.y)
        
    def onDragM3(self, event):
        dx = event.x - self.click_x
        dy = event.y - self.click_y
        shape_y = self.selected_shape.center_y
        
        r = event.y - shape_y
        
        self.selected_shape.resize(r)
        x1,y1,x2,y2 = self.selected_shape.getCords()
        canvas.coords(self.selected_shape.canvas_id, x1,y1,x2,y2)
        self.setClickXY(event.x, event.y)

    def drawLineEntry(self, x1, y1, x2, y2):
        if(x1 == "" or y1 == "" or x2 == "" or y2 == ""):
            return
        id = self.canvas.create_line(x1, y1, x2, y2)
        line = Line(x1, y1, x2, y2, id)
        self.shapes.append(line)
        print("Line drawn", line.getCords())
    
    def drawRectEntry(self, x1, y1, x2, y2):
        if(x1 == "" or y1 == "" or x2 == "" or y2 == ""):
            return
        id = self.canvas.create_rectangle(x1, y1, x2, y2)
        rect = Rectangle(x1, y1, x2, y2, id)
        self.shapes.append(rect)
        print("Rectangle drawn", rect.getCords())

    def drawCircleEntry(self, x, y, radius = 10, mouse = False, x2 = None, y2 = None):
        id = None
        if mouse == False:
            if (x == "" or y == "" or radius == ""):
                return
            x = int(x)
            y = int(y)
            radius = int(radius)
            id = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius)
        else:
            id = self.canvas.create_oval(x, y, x2, y2)
        circle = Circle(x, y, radius, id)
        self.shapes.append(circle)
        print("Circle drawn", circle.getCords())        
        
    def importShapes(self, shapes):
        self.shapes = []
        for shape in shapes:
            shape_string = shape[5:]
            shape_name = shape[:4]
            shape_list = shape_string.replace(")", "").split(", ")
            # print("shape_list: ", shape_list)
            if shape_name == "Line":
                x1 = int(shape_list[0])
                y1 = int(shape_list[1])
                x2 = int(shape_list[2])
                y2 = int(shape_list[3])
                self.drawLineEntry(x1, y1, x2, y2)
            elif shape_name == "Rect":
                x1 = int(shape_list[0])
                y1 = int(shape_list[1])
                x2 = int(shape_list[2])
                y2 = int(shape_list[3])
                self.drawRectEntry(x1, y1, x2, y2)
            elif shape["type"] == "Circ":
                x = int(shape_list[0])
                y = int(shape_list[1])
                radius = int(shape_list[2])
                self.drawCircleEntry(x, y, radius)
            
        
# ==================== 
#       
# Tkinker application        
#        
# ====================       
        
def drawButton():
    shape = shape_combo.get()
    print("siema", shape)
    if(shape == "Line" or shape == "Rectangle"):    
        x_1 = x1.get()
        y_1 = y1.get()
        x_2 = x2.get()
        y_2 = y2.get()
        print("siema", x_1, y_1, x_2, y_2)
        if shape == "Line":
            paint.drawLineEntry(x_1, y_1, x_2, y_2)
        else: paint.drawRectEntry(x_1, y_1, x_2, y_2)
    else: paint.drawCircleEntry(circle_x.get(), circle_y.get(), circle_radius.get())

def update_inputs(event):
    # x1.delete(0, END)
    # y1.delete(0, END)
    # x2.delete(0, END)
    # y2.delete(0, END)
    # circle_radius.delete(0, END)
    # circle_x.delete(0, END)
    # circle_y.delete(0, END)
    
    for widget in input_frame.winfo_children():
        widget.grid_forget()
    
    labels = {
        "Line&Rect": ["x1:", "y1:", "x2:", "y2:"],
        "Circle": ["x:", "y:", "radius:"]
    }
    
    selected_shape = shape_combo_str.get()
    paint.comboShape(selected_shape)
    if selected_shape == "Line" or selected_shape == "Rectangle":
        
        Label(input_frame, text=labels["Line&Rect"][0], bg="grey").grid(row=0, column=0, sticky="e")
        x1.grid(row=0, column=1, sticky="w")
        
        Label(input_frame, text=labels["Line&Rect"][1], bg="grey").grid(row=1, column=0, sticky="e")
        y1.grid(row=1, column=1, sticky="w")
        
        Label(input_frame, text=labels["Line&Rect"][2], bg="grey").grid(row=2, column=0, sticky="e")
        x2.grid(row=2, column=1, sticky="w")
        
        Label(input_frame, text=labels["Line&Rect"][3], bg="grey").grid(row=3, column=0, sticky="e")
        y2.grid(row=3, column=1, sticky="w")
        
        Button(input_frame, text="Draw", command=drawButton, 
                                        width=12).grid(row=4, column=0, columnspan=2)

    elif selected_shape == "Circle":
        Label(input_frame, text=labels["Circle"][0], bg="grey").grid(row=0, column=0, sticky="e")
        circle_x.grid(row=0, column=1, sticky="w")
        
        Label(input_frame, text=labels["Circle"][1], bg="grey").grid(row=1, column=0, sticky="e")
        circle_y.grid(row=1, column=1, sticky="w")
        
        Label(input_frame, text=labels["Circle"][2], bg="grey").grid(row=2, column=0, sticky="e")
        circle_radius.grid(row=2, column=1, sticky="w")

        Button(input_frame, text="Draw", command= drawButton, width=12).grid(row=4, column=0, columnspan=2)

    
def importSerialize():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), 
                                                           ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                canvas_data = json.load(file)
                print("canvas data: ", canvas_data)
            paint.importShapes(canvas_data["shapes"])
        except Exception as e:
            print("somethink does not work", e)
        finally:
            print("File imported")
        
def exportSerialize():
    canvas_data = {
        "shapes": []
    }
    for shape in paint.shapes:
        canvas_data["shapes"].append(shape.__str__())
        
        print("shape: ", shape.__repr__())
            
    file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                                   filetypes=[("JSON Files", "*.json"), 
                                                              ("All Files", "*.*")])
    if file_path:
        with open (file_path, "w") as file:
            json.dump(canvas_data, file)
        print("File saved to: ", file_path)
        
root = Tk()
root.title("Paint - Sak Jakub")
# root.minsize(800, 600)

# main grid 1/2
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.rowconfigure(0, weight=1)

# left panel
left_panel = Frame(root, width=200, height=410, bg='grey')
left_panel.grid(column=0, row=0, sticky="nsew")

# right panel
right_panel = Frame(root, width=400, height=410)
right_panel.grid(column=1, row=0, columnspan=2, sticky="nsew")

# canvas on right panel
canvas = Canvas(right_panel, width=400, height=400,bg="white")
canvas.pack()

paint = Paint(canvas)

# choose_project_number = Button(left_panel, text="Choose project number", command=setup_layout)

draw_btn = Button(left_panel, text="Mouse Draw", command=paint.actionDraw, width=14)
draw_btn.pack()
move_btn = Button(left_panel, text="Mouse Select", command=paint.actionMove, width=14)
move_btn.pack()
shape_combo_label = Label(left_panel, text="Select shape", bg="grey", width=14)
shape_combo_label.pack()
shape_combo_str = StringVar()
shape_combo = Combobox(left_panel, textvariable=shape_combo_str, width=14)
shape_combo['values'] = ("Line", "Rectangle", "Circle")
shape_combo.pack()
shape_combo.current()

# text inputs
input_frame = Frame(left_panel, bg="grey")
input_frame.pack()

x1 = Entry(input_frame, width=10)
y1 = Entry(input_frame, width=10)
x2 = Entry(input_frame, width=10)
y2 = Entry(input_frame, width=10)

circle_x = Entry(input_frame, width=10)
circle_y = Entry(input_frame, width=10)
circle_radius = Entry(input_frame, width=10)

shape_combo.bind("<<ComboboxSelected>>", update_inputs)

# import export

import_btn = Button(left_panel, text="Import", command=importSerialize, width=14)
import_btn.pack(side="bottom")
export_btn = Button(left_panel, text="Export", command=exportSerialize, width=14)
export_btn.pack(side="bottom")


mainloop()