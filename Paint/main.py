from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import json
from shapes import *
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
    JPEG gotowe biliteki
    wydajne wczytywanie ppm6



skalowanie wartosci ppm3
1000

344

344/max*255
------------------------------------------------------------------------

'''


    
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
        #canvas.bind("<Button-2>", self.onMouse2)                # mouse 2 click bind
        canvas.bind("<MouseWheel>", self.onScroll)                  
        # canvas.bind("<ButtonRelease-1>", self.onReleaseMouse1)  # mouse 1 release bind
        #canvas.bind("<ButtonRelease-2>", self.onReleaseMouse2)  # mouse 1 release bind
        canvas.bind("<ButtonRelease-3>", self.onReleaseMouse3)  # mouse 3 release bind
        
      
        
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
        self.canvas.tag_bind(id, "<B2-Motion>")
        if(self.selected_shape.className() != "Line"):
            self.canvas.itemconfig(id, outline = "black", width = 1)
        self.selected_shape = None
        print("selected shape cleared")

    def setClickXY(self, x, y):
        self.click_x = x
        self.click_y = y 
        print("click", self.click_x, self.click_y) 
           
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
                self.drawCircleEntry(x1,y1, x2, y2)
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
                        showSelShapeVal(shape)
                        break
                print("selected shape ", self.selected_shape.canvas_id)
                self.canvas.tag_bind(item_id, "<B1-Motion>", self.onDragM1)
                self.canvas.tag_bind(item_id, "<B2-Motion>", self.onDragM2)
                if(self.selected_shape.className() != "Line"):
                    self.canvas.itemconfig(item_id, outline = "red", width = 2)
                break
        else:
            pass
    
    def onMouse2(self, event):
        if self.selected_shape == None:
            return 
        id = self.selected_shape.canvas_id
        self.canvas.tag_bind(id, "<B2-Motion>", self.onDragM2)
        print("on mouse 2 added tab gind")
        
    
        
    def onMouse3(self, event):
        x,y = event.x, event.y
        # self.setClickXY(x,y)
        
    
    # def onReleaseMouse1(self, event):
    #     if self.selected_shape != None:
    #         #canvas.tag_unbind(self.selected_shape.canvas_id, "<B1-Motion>")
    #         pass
            
    #     self.setClickXY(None, None)
    
    def onReleaseMouse2(self, event):
        if self.selected_shape == None:
            return 
        id = self.selected_shape.canvas_id
        self.canvas.tag_unbind(id, "<B3-Motion>")
        print("on mouse 2 removed tab gind")
    
    def onReleaseMouse3(self, event):
        self.clearDrawingPoints()
        self.clearSelectedShape()
        self.setClickXY(None, None)
        clearInputs()
    
    def onScroll(self, event):
        if(self.selected_shape == None):
            return
        if event.delta > 0: # scroll up
            self.selected_shape.resize(1)
        elif event.delta < 0: # scroll down
            self.selected_shape.resize(-1)   
        showSelShapeVal(self.selected_shape)
        x1,y1,x2,y2 = self.selected_shape.getCords()
        canvas.coords(self.selected_shape.canvas_id, x1,y1,x2,y2)
    
    
    def actionDraw(self):
        self.selected_action = "draw"
        self.clearSelectedShape()
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
        showSelShapeVal(self.selected_shape)
        self.setClickXY(event.x, event.y)
        print("event in drag: ", event.x, event.y)
        print("shape in drag 1: ", self.selected_shape.getCords())
        self.selected_shape.move(dx, dy)        
         
        print("shape in drag 2 : ", self.selected_shape.getCords())
        
    def onDragM2(self, event):
        dx = event.x - self.click_x
        dy = event.y - self.click_y
        print("shape in drag 3 : ", self.selected_shape.getCords())
        print("shape in drag 3 : ", dx, dy)
        id = self.selected_shape.canvas_id
        x = self.selected_shape.x0
        y = self.selected_shape.y0
        x1 = self.selected_shape.x1
        y1 = self.selected_shape.y1
        self.selected_shape.newCoords(x,y, x1+dx, y1+dy)
        self.canvas.coords(id, x,y,x+dx, y+dy)
        #self.setClickXY(event.x, event.y)

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

    # def drawCircleEntry(self, x, y, radius = 10, mouse = False, x2 = None, y2 = None):
    #     id = None
    #     if mouse == False:
    #         if (x == "" or y == "" or radius == ""):
    #             return
    #         x = int(x)
    #         y = int(y)
    #         radius = int(radius)
    #         id = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius)
    #     else:
    #         x = int(x)
    #         y = int(y)
    #         radius = int(radius)
    #         id = self.canvas.create_oval(x, y, x2, y2)
    #     circle = Circle(x, y, radius, id)
    #     self.shapes.append(circle)
    #     print("Circle drawn", circle.getCords())        
        
    def drawCircleEntry(self, x, y, x2, y2):
        x = int(x)
        y = int(y)
        # radius = int(radius)
        id = self.canvas.create_oval(x, y, x2, y2)
        circle = Circle(x, y, x2, y2, id)
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
            
    def editSelShape(self, x_1, y_1, x_2, y_2):
        if(self.selected_shape == None):
            return
        id = self.selected_shape.canvas_id
        self.selected_shape.newCoords(x_1, y_1, x_2, y_2)
        self.canvas.coords(id, x_1, y_1, x_2, y_2)
        # if self.selected_shape.className() == "Line":
        #     self.selected_shape.newCoords(x_1, y_1, x_2, y_2)
        #     self.canvas.coords(id, x_1, y_1, x_2, y_2)
        # if self.selected_shape.className() == "Rect":
        #     self.selected_shape.newCoords(x_1, y_1, x_2, y_2)
        #     self.canvas.coords(id, x_1, y_1, x_2, y_2)
        # if self.selected_shape.className() == "Circ":
        #     self.selected_shape.newCoords(x_1, y_1, x_2, y_2)
        #     self.canvas.coords(id, x0, y0, x1, y1)
        
# ==================== 
#       
# Tkinker application        
#        
# ====================       

def drawButton():
    x_1 = int(x1.get())
    y_1 = int(y1.get())
    x_2 = int(x2.get())
    y_2 = int(y2.get())
    shape = shape_combo.get()
    
    if(paint.selected_shape != None):
        paint.editSelShape(x_1, y_1, x_2, y_2)
        return
    if shape == "Line":
        paint.drawLineEntry(x_1, y_1, x_2, y_2)
    elif shape == "Rectangle": 
        paint.drawRectEntry(x_1, y_1, x_2, y_2)
    else: 
        paint.drawCircleEntry(x_1, y_1, x_2, y_2)


def update_inputs(event):
    
    for widget in input_frame.winfo_children():
        widget.grid_forget()
    
    labels = {
        "Line&Rect": ["x1:", "y1:", "x2:", "y2:"],
    }
    
    selected_shape = shape_combo_str.get()
    paint.comboShape(selected_shape)
    
    Label(input_frame, text=labels["Line&Rect"][0], bg="grey").grid(row=0, column=0, sticky="e")
    x1.grid(row=0, column=1, sticky="w")
    
    Label(input_frame, text=labels["Line&Rect"][1], bg="grey").grid(row=1, column=0, sticky="e")
    y1.grid(row=1, column=1, sticky="w")
    
    Label(input_frame, text=labels["Line&Rect"][2], bg="grey").grid(row=2, column=0, sticky="e")
    x2.grid(row=2, column=1, sticky="w")
    
    Label(input_frame, text=labels["Line&Rect"][3], bg="grey").grid(row=3, column=0, sticky="e")
    y2.grid(row=3, column=1, sticky="w")

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

def clearInputs():
    x1.delete(0, END)
    y1.delete(0, END)
    x2.delete(0, END)
    y2.delete(0, END)
    circle_radius.delete(0, END)
    circle_x.delete(0, END)
    circle_y.delete(0, END)
    

def showSelShapeVal(shape):
    clearInputs()
    
    shape_x1 = round(int(shape.x0))
    shape_y1 = round(int(shape.y0))
    shape_x2 = round(int(shape.x1))
    shape_y2 = round(int(shape.y1))
    print(shape_x1, shape_y1, shape_x2, shape_y2)
    x1.insert(0, shape_x1)
    y1.insert(0, shape_y1)
    x2.insert(0, shape_x2)
    y2.insert(0, shape_y2)
    if shape.className == "Circle":
        circle_x.insert(0, round(shape.x))
        circle_y.insert(0, round(shape.y))
        circle_radius.insert(0, round(shape.radius))
        
    
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