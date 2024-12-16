'''
Projekt 4
Wymagania na najwyższą ocenę:

a. Przekształcenia punktowe

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i wykonywanie na nim poniższych operacji:
Dodawanie (dowolnych podanych przez użytkownika wartości),
Odejmowanie (dowolnych podanych przez użytkownika wartości),
Mnożenie (przez dowolne podane przez użytkownika wartości),
Dzielenie (przez dowolne podane przez użytkownika wartości),
Zmiana jasności (o dowolny podany przez użytkownika poziom),
Przejście do skali szarości (na dwa sposoby)


b. Metody polepszania jakości obrazów

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i aplikowanie do niego poniższych filtrów:
Filtr wygładzający (uśredniający),
Filtr medianowy,
Filtr wykrywania krawędzi (sobel),
Filtr górnoprzepustowy wyostrzający,
Filtr rozmycie gaussowskie,
Splot maski dowolnego rozmiaru i dowolnych wartości elementów maski (opcjonalne za dodatkowe punkty)
Filtr wygładzający:
⎡⎣⎢111111111⎤⎦⎥

Filtr wykrywania krawędzi (pionowy i poziomy):
⎡⎣⎢−1−2−1000121⎤⎦⎥
⎡⎣⎢10−120−210−1⎤⎦⎥

Filtr górnoprzepustowy wyostrzający:
⎡⎣⎢−1−1−1−19−1−1−1−1⎤⎦⎥

Filtr Gaussa:
    121
    242
    121


Uwagi:
Zabronione stosowanie bibliotek do implementacji przekształceń punktowych i filtrów
'''


import colorsys
import tkinter as tk
from tkinter import filedialog, messagebox
import io
from PIL import Image,ImageTk,ImageEnhance
import numpy as np
from threads import CustomThread


class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x800")
        self.root.title("Paint - Sak Jakub")
        self.root.update()
        
        # menubar at the top
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="import", command=self.importFile)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        # divide window
        
        self.left_frame = tk.Frame(self.root, width=290, height=800, bg="lightblue")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)
        self.right_frame = tk.Frame(self.root, width=800, height=800, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)
    
        # tkinker
        
        self.r_frame = tk.Frame(self.left_frame)
        self.r_frame.pack()
        self.g_frame = tk.Frame(self.left_frame)
        self.g_frame.pack()
        self.b_frame = tk.Frame(self.left_frame)
        self.b_frame.pack()
        
            
        self.r_drop_val = tk.StringVar()
        self.g_drop_val = tk.StringVar()
        self.b_drop_val = tk.StringVar()
        self.r_drop_val.set("+")
        self.g_drop_val.set("+")
        self.b_drop_val.set("+")
        
        self.r_drop = tk.OptionMenu(self.r_frame, self.r_drop_val, "+", "-", "*", "/")
        self.g_drop = tk.OptionMenu(self.g_frame, self.g_drop_val, "+", "-", "*", "/")
        self.b_drop = tk.OptionMenu(self.b_frame, self.b_drop_val, "+", "-", "*", "/")
        
        self.r_entry = tk.Entry(self.r_frame)
        self.g_entry = tk.Entry(self.g_frame)
        self.b_entry = tk.Entry(self.b_frame)
        
        
        self.r_drop.pack(side=tk.LEFT)
        self.r_entry.pack(side=tk.LEFT)
        self.g_drop.pack(side=tk.LEFT)
        self.g_entry.pack(side=tk.LEFT)
        self.b_drop.pack(side=tk.LEFT)
        self.b_entry.pack(side=tk.LEFT)
        
        self.update_button = tk.Button(self.left_frame, text="Update", command=self.updateValues)
        self.update_button.pack()
        
        
        # Brightness slider

        self.brightness_slider = tk.Scale(self.left_frame, 
                                          from_=0.1, to=2.0, 
                                          resolution=0.1, 
                                          orient=tk.HORIZONTAL, 
                                          label="Brightness",
                                          command=self.changeBrightness)
        
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack()
        
        # gray Button #1
        
        self.gray_button_1 = tk.Button(self.left_frame, text="Gray", command=self.gray1)
        self.gray_button_1.pack()
        
        # gray Button #2
        
        self.gray_button_2 = tk.Button(self.left_frame, text="Gray", command=self.gray2)
        self.gray_button_2.pack()
        
        # Filtr Wygladzający
        
        self.smooth_button = tk.Button(self.left_frame, text="Smooth", command=self.smooth)
        self.smooth_button.pack()
        
        # Filtr medianowy,
        
        self.median_button = tk.Button(self.left_frame, text="Median", command=self.median)
        self.median_button.pack()
        
        # Filtr wykrywania krawędzi (sobel),
        
        self.sobelVertical_button = tk.Button(self.left_frame, text="Sobel Vertical", command=self.sobelVertical)
        self.sobelVertical_button.pack()
        
        self.sobelHorizontal_button = tk.Button(self.left_frame, text="Sobel Horizontal", command=self.sobelHorizontal)
        self.sobelHorizontal_button.pack()
        
        # Filtr górnoprzepustowy wyostrzający,
        
        self.highpass_button = tk.Button(self.left_frame, text="Highpass", command=self.highpass)
        self.highpass_button.pack()
        # Filtr rozmycie gaussowskie,
        
        self.gauss_button = tk.Button(self.left_frame, text="Gauss", command=self.gaussian)
        self.gauss_button.pack()
        
        # Splot maski dowolnego rozmiaru i dowolnych wartości elementów maski (opcjonalne za dodatkowe punkty)
        
        self.customFilter_button = tk.Button(self.left_frame, text="Custom Filter", command=self.customFilter)
        self.customFilter_button.pack()
        
        # back to Original Button - reverse to original PIL image
        
        self.cancel_button = tk.Button(self.left_frame, text="Cancel changes", command=self.cancelChanges)
        self.cancel_button.pack()
        
        #
        # right frame Canvas with Scrollbars
        #
    
        self.canvas = tk.Canvas(self.right_frame, bg="white")
        
        self.scroll_x = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.scroll_y = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        
        
        #
        #   self images
        #
        self.original_PILImage = None
        self.PILImage = None
        self.original_photoimage = None          
        self.image_tk = None                
        self.image_id = None
        
        
        
        
        
        # Mouse binds    
        self.canvas.bind("<MouseWheel>", self.zoom)
    

        # scale factor
        
        self.scale_factor = 1.0
        
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))


        
    def setImage(self, photo_image):
        self.scale_factor = 1.0
        self.original_photoimage = photo_image
        self.image_tk = photo_image
        self.image_id = self.canvas.create_image(0,0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))            
    def zoom(self, event):
        if(self.original_photoimage==None): 
            return
        
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
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))      
    def importFile(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*")]
        )
    
        if not file_path:
                print("no file selected")
                return
        
        self.canvas.delete("all")      
        try:
            img = Image.open(file_path)
            self.PILImage = img
            self.original_PILImage = img
            img = ImageTk.PhotoImage(img)
            self.setImage(img)
        except:
            self.PILImage = None
            messagebox.showerror("Error while loading image", "Unsupported file type")          
    def updateValues(self):
        # if self.original_photoimage==None: 
        #     return
        r_entry = self.r_entry.get()
        g_entry = self.g_entry.get()
        b_entry = self.b_entry.get()
        rgb = [r_entry,g_entry,b_entry]
        
        for a in range(0,3):
            if rgb[a] == "": 
                rgb[a] = None
            else:
                if not rgb[a].isdigit():
                    messagebox.showerror("Error", "RGB values must be integers")
                    return
                rgb[a] = int(rgb[a])
                if not 0 < rgb[a] < 255:
                    messagebox.showerror("Error", "RGB values must be between 0 and 255")
                    return
        
        img_array = np.array(self.PILImage)
        
        width, height = self.PILImage.size
        res_img = Image.new("RGB", (width, height))
        
        r_operator = self.r_drop_val.get()
        g_operator = self.g_drop_val.get()
        b_operator = self.b_drop_val.get()
        operators = [r_operator, g_operator, b_operator]
        
        for x in range(width):
            for y in range(height):
                r, g, b = self.PILImage.getpixel((x, y))
                rgb_to_change = [r, g, b]
                for a in range(0,3):
                    if rgb[a]:
                        entry_value = int(rgb[a])
                        if operators[a] == "+":
                            rgb_to_change[a] = rgb_to_change[a] + entry_value
                        elif operators[a] == "-":
                            rgb_to_change[a] = rgb_to_change[a] - entry_value
                        elif operators[a] == "*":
                            rgb_to_change[a] = rgb_to_change[a] * entry_value
                        elif operators[a] == "/":
                            rgb_to_change[a] = rgb_to_change[a] // entry_value
                        if rgb_to_change[a] > 255:
                            rgb_to_change[a] = 255
                        if rgb_to_change[a] < 0:
                            rgb_to_change[a] = 0
                r,g,b = rgb_to_change
                res_img.putpixel((x, y), (r, g, b))
                        
        
        # img = Image.fromarray(pixel_matrix)
        self.PILImage = res_img
        self.image_tk = ImageTk.PhotoImage(res_img)
        
        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
                
    def changeBrightness(self, event):
        if self.original_photoimage==None: 
            return
    
        width, height = self.original_PILImage.size
        brightness_factor = float(self.brightness_slider.get())
        img_array = list(self.original_PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
        threads = []
        data_pixels = []
        
        def BrightnessWorker(line, brightness_factor):
            line_pixels = []
            for x in range(len(line)):
                r,g,b = line[x]
                
                r = int(r * brightness_factor)
                g = int(g * brightness_factor)
                b = int(b * brightness_factor)
                rgb = [r,g,b]
                
                for a in range(0,3):
                    if rgb[a] < 0:
                        rgb[a] = 0
                    elif rgb[a] > 255:
                        rgb[a] = 255
                
                line_pixels.append((rgb[0], rgb[1], rgb[2]))
            return line_pixels
        
        for x in range(0, len(img_array), width):
            end_of_line = x+width
            line = img_array[x:end_of_line]
            if end_of_line > len(img_array):
                line = img_array[x:]
            threads.append(CustomThread(target = BrightnessWorker, args=(line, brightness_factor,)))
            threads[-1].start()
        
        for x in range(len(threads)):
            ret_val = threads[x].join()
            data_pixels.extend(ret_val)
        threads = []
        
        res_img.putdata(data_pixels)
            
        self.PILImage = res_img
        self.image_tk = ImageTk.PhotoImage(res_img)
        
        # enhancer = ImageEnhance.Brightness(self.PILImage)
        # brightness_factor = float(self.brightness_slider.get())
        # bright_img = enhancer.enhance(brightness_factor)
        # self.image_tk = ImageTk.PhotoImage(bright_img)
        
        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def cancelChanges(self):
        if self.original_photoimage==None: 
            return
        self.brightness_slider.set(1.0)
        self.r_entry.delete(0, tk.END)
        self.g_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.PILImage = self.original_PILImage
        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photoimage)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def gray1(self):
        if self.original_photoimage==None: 
            return
        
        img_array = list(self.PILImage.getdata())

        width, height = self.PILImage.size
        res_img = Image.new("RGB", (width, height))
        threads = []
        ret_data = []
        
        # Luminence formula
        r_weight = 0.2989
        g_weight = 0.5870
        b_weight = 0.1140
        
        def GrayWorker(line):
            line_pixels = []
            for x in range(len(line)):
                r,g,b = line[x]
                gray_val = int(r * r_weight + g * g_weight + b * b_weight)
                line_pixels.append((gray_val, gray_val, gray_val))
            return line_pixels
        
        for x in range(0, len(img_array), width):
            end_of_line = x+width
            line = img_array[x:end_of_line]
            if end_of_line > len(img_array):
                line = img_array[x:]
            threads.append(CustomThread(target = GrayWorker, args=(line,)))
            threads[-1].start()
        
        for x in range(len(threads)):
            ret_val = threads[x].join()
            ret_data.extend(ret_val)
        res_img.putdata(ret_data)
        
        threads = []
        
        # for x in range(width):
        #     for y in range(height):
        #         r, g, b = self.PILImage.getpixel((x, y))
                
        #         gray_val = int(r * r_weight + g * g_weight + b * b_weight)
                
        #         res_img.putpixel((x, y), (gray_val, gray_val, gray_val))

         
        # r_array = r_weight * img_array[:, :, 0] 
        # g_array = g_weight * img_array[:, :, 1]
        # b_array = b_weight * img_array[:, :, 2]
        
        # gray_array = r_array + g_array + b_array
        
        # gray_image = Image.fromarray(gray_array.astype(np.uint8))
        self.PILImage = res_img
        self.image_tk = ImageTk.PhotoImage(res_img)
        
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    def gray2(self):
        if self.original_photoimage==None: 
            return
        # Desaturation
        
        pixel_matrix = np.array(self.PILImage, dtype=np.uint8)
        
        width, height = self.PILImage.size
        res_img = Image.new("RGB", (width, height))
        
        for x in range(width):
            for y in range(height):
                r, g, b = self.PILImage.getpixel((x, y))
                
                # h,s,v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                # grey_val = int(v * 255)
                
                grey_val = (max(r,g,b) + min(r,g,b)) // 2
                
                res_img.putpixel((x, y), (grey_val, grey_val, grey_val))

        
        
        self.PILImage = res_img
        
        self.image_tk = ImageTk.PhotoImage(res_img)
        
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
    
    def applyFilter(self, filter):
        matrix = filter
        matrix_size = len(matrix)
        more_pixels = matrix_size // 2
        
        matrix_divide = 0
        for i in range(matrix_size):
            for j in range(matrix_size):
                matrix_divide += matrix[j][i]
        
        width, height = self.PILImage.size
        temp_width = width + more_pixels
        temp_height = height + more_pixels
        temp_og_image = Image.new("RGB", (temp_width, temp_height))
        res_img = Image.new("RGB", (width, height))
        return_img = Image.new("RGB", (width, height))        
        
        
        for x in range(temp_width):
            for y in range(temp_height):
                if x < more_pixels or x >= temp_width - more_pixels or y < more_pixels or y >= temp_height - more_pixels:
                    temp_og_image.putpixel((x, y), (0, 0, 0))
                else:
                    r,g,b = self.PILImage.getpixel((x - more_pixels, y - more_pixels))
                    temp_og_image.putpixel((x, y), (r, g, b))
                
        
        for x in range(temp_width):
            for y in range(temp_height):
                if x < more_pixels or x >= temp_width - more_pixels or y < more_pixels or y >= temp_height - more_pixels:
                    pass
                else:
                    r_sum = 0
                    g_sum = 0
                    b_sum = 0
                    for i in range(matrix_size):        # 0-2
                        for j in range(matrix_size):    # 0-2
                            r,g,b = temp_og_image.getpixel((x + i - more_pixels, y + j - more_pixels))
                            r_sum += matrix[j][i] * r
                            g_sum += matrix[j][i] * g
                            b_sum += matrix[j][i] * b
                    
                    if matrix_divide == 0:
                        matrix_divide = 1
                    rgb = [int(r_sum/matrix_divide), int(g_sum/matrix_divide), int(b_sum/matrix_divide)]
                    for a in range(0,3):
                        if rgb[a] < 0:
                            rgb[a] = 0
                        elif rgb[a] > 255:
                            rgb[a] = 255
                    r, g, b = rgb
                    res_img.putpixel((x, y), (r, g, b))
        
        # for x in range(width):
        #     for y in range(height):
        #         r, g, b = res_img.getpixel((x + more_pixels, y + more_pixels))
        #         return_img.putpixel((x, y), (r, g, b))    
        return_img = res_img
        self.PILImage = return_img
        self.image_tk = ImageTk.PhotoImage(return_img)
        
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def smooth(self):
        if self.original_photoimage==None:
            return
        filter = [[1,1,1],[1,1,1],[1,1,1]]
        self.applyFilter(filter)
    
    def median(self):
        if self.original_photoimage==None:
            return
        matrix_size = 3
        more_pixels = matrix_size // 2
        
        width, height = self.PILImage.size
        temp_width = width - more_pixels
        temp_height = height - more_pixels
        res_img = Image.new("RGB", (temp_width, temp_height))
        return_img = Image.new("RGB", (width, height))        
        
        for x in range(temp_width):
            for y in range(temp_height):
                if x < more_pixels or x >= temp_width - more_pixels or y < more_pixels or y >= temp_height - more_pixels:
                    res_img.putpixel((x, y), (0, 0, 0))
                else:
                    r_sum = []
                    g_sum = []
                    b_sum = []
                    for i in range(matrix_size):        # 0-2
                        for j in range(matrix_size):    # 0-2
                            r,g,b = self.PILImage.getpixel((x + i - more_pixels, y + j - more_pixels))
                            r_sum.append(r)
                            g_sum.append(g)
                            b_sum.append(b)

                    # Calculating Median value from read values

                    r, g, b = [np.median(r_sum), np.median(g_sum), np.median(b_sum)] 
                    res_img.putpixel((x, y), (int(r), int(g), int(b)))
        
        for x in range(width):
            for y in range(height):
                r, g, b = res_img.getpixel((x - more_pixels, y - more_pixels))
                return_img.putpixel((x, y), (r, g, b))
        
        self.PILImage = return_img
        self.image_tk = ImageTk.PhotoImage(return_img)
        
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def sobelVertical(self):
        if self.original_photoimage==None:
            return    
        filter = [[-1,0,1],[-2,0,2],[-1,0,1]]
        self.applyFilter(filter)
        
    def sobelHorizontal(self):
        if self.original_photoimage==None:
            return  
        filter = [[1,2,1],[0,0,0],[-1,-2,-1]]
        self.applyFilter(filter)    
    
    def highpass(self):
        if self.original_photoimage==None:
            return
        filter = [[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]
        self.applyFilter(filter)
    
    def gaussian(self):
        if self.original_photoimage==None:
            return
        filter = [[1,2,1],[2,4,2],[1,2,1]]
        self.applyFilter(filter)
    
    def customFilter(self):
        if self.original_photoimage==None:
            return
        file_path = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*")]
        )
    
        if not file_path:
                print("no file selected")
                return
        
        with open(file_path, "r") as file:
            customFilter = file.readlines()
            customFilter = [line.strip().split(",") for line in customFilter]
            customFilter = [[int(x) for x in line] for line in customFilter]
            self.applyFilter(customFilter)
    
if __name__ == "__main__":#
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
