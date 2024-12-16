from tkinter import *
from tkinter import filedialog, messagebox
import io

from PIL import Image as pil_image
from PIL import ImageTk as pil_imageTk

from ppm import *
from WindowCompression import CompressionWindow
from WindowConverter import ConverterWindow
'''
------------------------------------------------------------------------
Projekt 2
Wymagania na najwyższą ocenę:


# Wczytywanie i wyświetlanie plików graficznych w formacie PPM P3, 
# Wczytywanie i wyświetlanie plików graficznych w formacie PPM P6,
# Wydajny sposób wczytywania plików (blokowy zamiast bajt po bajcie),
# Wczytywanie plików JPEG,
# Zapisywanie wczytanego pliku w formacie JPEG,
# Możliwość wyboru stopnia kompresji przy zapisie do JPEG,
# Skalowanie liniowe kolorów,
# Powiększanie obrazu i przy dużym powiększeniu możliwość przesuwania oraz wyświetlanie wartości 
# pikseli R,G,B na każdym widocznym pikselu,
# Obsługa błędów (komunikaty w przypadku nieobsługiwanego formatu pliku oraz błędów w obsługiwanych formatach plików).

Uwagi:
Zabronione stosowanie bibliotek do wczytywania plików PPM
Dozwolone stosowanie bibliotek do wczytywania plików JPEG


------------------------------------------------------------------------

'''



class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x800")
        self.root.title("Paint - Sak Jakub")
        self.root.update()
        
        # menubar at the top
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="import", command=self.importFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="export jpeg", command=self.exportJPEG)
        self.menubar.add_cascade(label="Zad2", menu=self.filemenu)
        
        # self.windowMenu = Menu(self.menubar, tearoff=0)
        # self.windowMenu.add_command(label="converter", command=self.openConverterWindow)
        # self.windowMenu.add_command(label="cuber", command=self.openCubeWindow)
        # self.menubar.add_cascade(label="Zad3", menu=self.windowMenu)
        self.root.config(menu=self.menubar)
        
        # divide window
        
        self.left_frame = Frame(self.root, width=290, height=800, bg="lightblue")
        self.left_frame.pack(side=LEFT, fill=BOTH)
        self.left_frame.pack_propagate(False)
        self.right_frame = Frame(self.root, width=800, height=800, bg="white")
        self.right_frame.pack(side=RIGHT, fill=BOTH)
        self.right_frame.pack_propagate(False)
        
        #
        # left frame
        #
        
        # Pixel info
        self.pixel_label = Label(self.left_frame, text="RGB: (---, ---, ---)", bg="lightblue")
        self.pixel_label.pack(side=TOP)
        
        self.rgb_frame = Frame(self.left_frame, bg="lightblue")
        self.rgb_frame.pack(side=TOP, fill=X)

        Label(self.rgb_frame, text="R:").pack(side=LEFT, padx=2)
        self.r_spinbox = Spinbox(self.rgb_frame, from_=0, to=255, width=5)
        self.r_spinbox.pack(side=LEFT)

        Label(self.rgb_frame, text="G:").pack(side=LEFT, padx=2)
        self.g_spinbox = Spinbox(self.rgb_frame, from_=0, to=255, width=5)
        self.g_spinbox.pack(side=LEFT)

        Label(self.rgb_frame, text="B:").pack(side=LEFT, padx=2)
        self.b_spinbox = Spinbox(self.rgb_frame, from_=0, to=255, width=5)
        self.b_spinbox.pack(side=LEFT)

        self.change_button = Button(self.rgb_frame, text="Change", command=self.setPixelColor)
        self.change_button.pack(side=LEFT, padx=10)

        
        #
        # right frame
        #
    
        self.canvas = Canvas(self.right_frame, bg="white")
        
        self.scroll_x = Scrollbar(self.right_frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=BOTTOM, fill=X)

        self.scroll_y = Scrollbar(self.right_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        
        
        #
        #   self images
        #
        self.original_image = None          
        self.PILImage = None
        self.image_tk = None                
        self.image_id = None
        
        self.selected_pixel = None
        
        self.image_ext = None
        
        # Mouse binds
        # self.canvas.bind("<MouseWheel>", self.onMouseWheel)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Motion>", self.showPixelInfo)
        self.canvas.bind("<Button-1>", self.selectPixel)

        # scale factor
        
        self.scale_factor = 1.0
        
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        
    def setImage(self, photo_image):
        self.scale_factor = 1.0
        self.original_image = photo_image
        self.image_tk = photo_image
        self.image_id = self.canvas.create_image(0,0, anchor=NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        
    
    def onMouseWheel(self, event):
        if event.delta > 0:         # Scroll up - zoom in
            self.scale_factor *= 1.1
        else:                       # Scroll down - zoom out
            self.scale_factor /= 1.1
        self.resizeImage()

    
    def zoom(self, event):
        if(self.original_image==None): 
            return
        # if self.image_ext == 'ppm':
        #     scale_step = 0.1
        #     if event.delta > 0:  # Scroll up to zoom in
        #         # self.scale_factor += scale_step
        #         self.scale_factor = self.scale_factor * 1.1
        #     elif event.delta < 0:  # Scroll down to zoom out
        #         # self.scale_factor -= scale_step
        #         self.scale_factor = self.scale_factor / 1.1
        #         if self.scale_factor < 0.1:  
        #             self.scale_factor = 0.1   
            
        #     if self.scale_factor < 1:  
        #         scale = int(1 / self.scale_factor)
        #         self.current_image = self.original_image.subsample(scale, scale)
        #     else:  
        #         scale = int(self.scale_factor)
        #         self.current_image = self.original_image.zoom(scale, scale)

        #     # Update the image on the canvas
        #     self.canvas.itemconfig(self.image_id, image=self.current_image)
        # elif self.image_ext == 'jpg':
        scale_step = 0.1
        if event.delta > 0:  # Zoom in
            self.scale_factor += 0.1
        else:  # Zoom out
            self.scale_factor -= 0.1
        new_width = int(self.PILImage.width * self.scale_factor)
        new_height = int(self.PILImage.height * self.scale_factor)
        if new_width < 0 or new_height < 0: return
            
        zoomed_image = self.PILImage.resize((new_width, new_height), Image.Resampling.NEAREST)            
        self.image_tk = ImageTk.PhotoImage(zoomed_image)

        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))  
    
    def setPixelColor(self):
        if self.selected_pixel is None:
            return

        r = int(self.r_spinbox.get())
        g = int(self.g_spinbox.get())
        b = int(self.b_spinbox.get())

        # Update the pixel in the image
        self.PILImage.putpixel(self.selected_pixel, (r, g, b))
        
        new_width = int(self.PILImage.width * self.scale_factor)
        new_height = int(self.PILImage.height * self.scale_factor)
        if new_width < 0 or new_height < 0: return
        zoomed_image = self.PILImage.resize((new_width, new_height), Image.Resampling.NEAREST)            
        self.image_tk = ImageTk.PhotoImage(zoomed_image)
        
        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))  # Adjust scroll region
    
    def showPixelInfo(self, event):
        if self.original_image is None: return
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        img_x = int(canvas_x / self.scale_factor)
        img_y = int(canvas_y / self.scale_factor)

        if 0 <= img_x < self.original_image.width() and 0 <= img_y < self.original_image.height():
            rgb = self.PILImage.getpixel((img_x, img_y))
            self.pixel_label.config(text=f"RGB: {rgb}")
        else:
            self.pixel_label.config(text="RGB: (---, ---, ---)")

    
    def selectPixel(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        img_x = int(canvas_x / self.scale_factor)
        img_y = int(canvas_y / self.scale_factor)
        
        if 0 <= img_x < self.original_image.width() and 0 <= img_y < self.original_image.height():
            self.selected_pixel = (img_x, img_y)
            rgb = self.PILImage.getpixel((img_x, img_y))
            
            self.r_spinbox.delete(0, END)
            self.r_spinbox.insert(0, rgb[0])
            self.g_spinbox.delete(0, END)
            self.g_spinbox.insert(0, rgb[1])
            self.b_spinbox.delete(0, END)
            self.b_spinbox.insert(0, rgb[2])
        
            
    
    
    def importFile(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PPM Files", "*.ppm"), ("JPEG Files", "*.jpeg;*.jpg"), ("All Files", "*.*")]
        )
    
        if not file_path:
                print("no file selected")
                return
        
        self.canvas.delete("all")  
        
        
        file_ext = file_path.split('.')[-1].lower()
        
        print("File with ext : " , file_ext)
        
        if file_ext == 'ppm':
            image = loadPPM(file_path)
            self.image_ext = 'ppm'      
            image.write("temp.png")                  
            PIL_image = Image.open("temp.png")
            self.PILImage = PIL_image      
            self.setImage(image)
                
        elif file_ext in ('jpg', 'jpeg'):
            img = pil_image.open(file_path)
            self.PILImage = img
            img = pil_imageTk.PhotoImage(img)
            self.image_ext = 'jpg'
            self.setImage(img)
            
        else:
            messagebox.showerror("Error", "Unsupported file type")
            
    
    def openCompressionWindow(self):
        result = None

        def on_save(value):
            nonlocal result
            result = value
        
        
        comp_winow = CompressionWindow(self.root, on_save)
        self.root.wait_window(comp_winow)
        
        return result
    
    def openConverterWindow(self):
        ConverterWindow(self.root)
        
    def openCubeWindow(self):
        # ConverterWindow(self.root)
        pass
    
    def exportJPEG(self):
        comrpession = 20
        
        
        if(self.image_tk==None):
            messagebox.showerror("Error", "No image to export")
            return
        
        filename = filedialog.asksaveasfilename(
            initialfile = 'image.jpg',
            defaultextension = ".jpg",
            filetypes=[("JPEG Files", "*.jpeg;*.jpg"),("All Files","*.*"),("Text Documents","*.txt")]
        )
        if not filename:
            messagebox.showerror("Error", "No file selected")
            return
        
        image = pil_imageTk.getimage(self.image_tk)         # convert tkinerk PhotoImage to PIL Image
        image = image.convert('RGB')                        # conver to rgb
        
        # Compression Window
        comrpession = self.openCompressionWindow()


        buffer = io.BytesIO()
        image.save(buffer, format='jpeg', optimize=True, quality=comrpession)
        buffer.seek(0)
        compressed_image = pil_image.open(buffer)
        
        
        compressed_image.save(filename)                                # save a jpeg
           

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

