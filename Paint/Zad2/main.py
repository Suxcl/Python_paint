from tkinter import *
from tkinter import filedialog
'''
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

        
    
class tkinkerImage:
    def __init__(self):
        self.image = None    
    def setImage(self, image):
        self.image = image    
    

    
  
def exportFile():
    pass   
 
def loadPPM(file_path):
    with open(file_path, 'rb') as f:
        header = f.readline().decode().strip()
        
        if header not in {'P3', 'P6'}:
            raise ValueError("BAD PPM file")
        
        data = []
        size = f.readline().decode().strip().split(' ')
        width = int(size[0])
        height = int(size[1])
        max_val = f.readline().decode().strip()
        
        if header == "P3":
            for line in f:
                # data.extend(map(int, line.split()))
                data.append(list(map(int, line.split())))

        elif header == "P6":
                # data = list(f.read())
            pass

        pixels = []
        photo_image = PhotoImage(width=width, height=height)
        
        for j in range(len(data)):
            pixel_line = []
            for i in range(0, len(line),3):
                r,g,b = data[j][i], data[j][i+1], data[j][i+2]
                # pixel_line.append((r,g,b))
                photo_image.put("#%02x%02x%02x" % (r,g,b), (i, j))
            pixels.append(pixel_line)
        
        
        

        return photo_image
        
def ppm3(file):
    pixels = []
    size = file.readline().decode().strip().split(' ')
    width = int(size[0])
    height = int(size[1])
    max_val = file.readline().decode().strip()
    
    
    print("width, height",width, height)
    
    for i in range(height):
        pixel_row = []        
        line = file.readline().decode().strip()
        
        print("line ",line)
        print("len line: ", len(line) , "\n")
        # r, g, b = file.readline().decode().strip().split(' ')
        # pixel = (int(r), int(g), int(b))
        # pixel_row.append(pixel)
        # print(pixel)
        pixels.append(pixel_row)
    print(pixels)
    
def loadJPEG(file_path):
    pass

 
 
def importFile():
    file_path = filedialog.askopenfilename(
            filetypes=[("PPM Files", "*.ppm"), ("JPEG Files", "*.jpeg;*.jpg"), ("All Files", "*.*")]
        )
    
    if not file_path:
            print("no file selected")
            return
    
    file_ext = file_path.split('.')[-1].lower()
    print("File with ext : " , file_ext)
    if file_ext == 'ppm':
        image = loadPPM(file_path)
        setImage(image)
    elif file_ext in ('jpg', 'jpeg'):
        loadJPEG(file_path)
    else:
        print("Unsupported file type")
     
 
def saveJPEG():
    pass

def setImage(image):
    label.config(image=image)

root = Tk()
root.title("Paint - Sak Jakub")
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="import", command=importFile)
filemenu.add_separator()
filemenu.add_command(label="export jpeg", command=saveJPEG)

menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

# canvas = Canvas(root)
# canvas.pack()

label = Label(root)
label.pack()




mainloop()