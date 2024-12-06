from tkinter import *
from tkinter import filedialog
import io
import threading
import numpy
from threading import Thread
from multiprocessing import Pool
from PIL import Image, ImageTk


from ppm import *



class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title("Paint - Sak Jakub")
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="import", command=self.importFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="export jpeg", command=self.exportJPEG)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        root.config(menu=self.menubar)
        
        
        self.canvas = Canvas(root, width=800, height=800)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        
        self.original_image = None          
        self.PILImage = None
        self.image_tk = None                
        self.image_id = None
        
        self.TK_photo_image = None
        
        # Mouse binds
        # self.canvas.bind("<MouseWheel>", self.onMouseWheel)
        self.canvas.bind("<MouseWheel>", self.zoom)
        # scale factor
        
        self.scale_factor = 1.0
        
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        
    def setImage(self, photo_image):
        self.scale_factor = 1.0
        self.original_image = photo_image
        self.image_tk = photo_image
        self.image_id = self.canvas.create_image(0,0, anchor=NW, image=self.image_tk)
        
    
    def onMouseWheel(self, event):
        if event.delta > 0:         # Scroll up - zoom in
            self.scale_factor *= 1.1
        else:                       # Scroll down - zoom out
            self.scale_factor /= 1.1
        self.resizeImage()
    
    def resizeImage(self):
        self.PILImage = Image.open(io.BytesIO(self.original_image))
        new_width = int(self.original_image.width() * self.scale_factor)
        new_height = int(self.original_image.height() * self.scale_factor)
        self.image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
        
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_id, image=self.image_tk)
        self.canvas.config(width=self.image_tk.width(), height=self.image_tk.height())
    
    def zoom(self, event):
        if(self.original_image==None): 
            return
        
        scale_step = 0.1
        if event.delta > 0:  # Scroll up to zoom in
            self.scale_factor += scale_step
        elif event.delta < 0:  # Scroll down to zoom out
            self.scale_factor -= scale_step
            if self.scale_factor < 0.1:  # Prevent too much zoom out
                self.scale_factor = 0.1   

        new_width = int(self.original_image.width() * self.scale_factor)
        new_height = int(self.original_image.height() * self.scale_factor)
        
        if self.scale_factor < 1:  # Use subsample for downsizing
            scale = int(1 / self.scale_factor)
            self.current_image = self.original_image.subsample(scale, scale)
        else:  # Use zoom for enlarging
            scale = int(self.scale_factor)
            self.current_image = self.original_image.zoom(scale, scale)

        # Update the image on the canvas
        self.canvas.itemconfig(self.image_id, image=self.current_image)
    
    def importFile(self):
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
            self.setImage(image)
        elif file_ext in ('jpg', 'jpeg'):
            self.loadJPEG(file_path)
        else:
            print("Unsupported file type")
        



    
    def exportJPEG():
        pass   

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

