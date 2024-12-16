'''
Projekt 5 
Histogram - wyrównanieAdres URL
http://www.algorytm.org/przetwarzanie-obrazow/histogram-wyrownywanie.html
Histogram - rozciąganie
http://www.algorytm.org/przetwarzanie-obrazow/histogram-rozciaganie.html
Metody automatycznego dobierania progu binaryzacji
https://www.olympus-lifescience.com/en/microscope-resource/primer/java/digitalimaging/processing/automaticthresholding/

Wymagania na najwyższą ocenę:

a. Histogram

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i zaprezentowanie działania normalizacji obrazu poprzez:
Rozszerzenie histogramu,
Wyrównanie (equalization) histogramu.
b. Binaryzacja

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i zaprezentowanie działania binaryzacji z ustaleniem progów binaryzacji w następujący sposób:
# Ręcznie przez użytkownika - użytkownik podaje próg bezpośrednio,
Procentowa selekcja czarnego (ang. Percent Black Selection),
Selekcja iteratywna średniej (ang. Mean Iterative Selection),
Selekcja entropii (ang. Entropy Selection),
Błąd Minimalny (ang. Minimum Error),
Metoda rozmytego błędu minimalnego (ang. Fuzzy Minimum Error).
Uwagi:
Spośród powyższych sposobów binaryzacji konieczna jest implementacja sposobu 1 oraz dwóch wybranych spośród 2 - 6. Za implementację więcej niż dwóch sposobów binaryzacji wybranych spośród 2 - 6 przyznane zostaną dodatkowe punkty.
Zabronione jest stosowanie bibliotek w implementacji normalizacji i binaryzacji.
'''


import tkinter as tk
from tkinter import filedialog, messagebox
import io
from PIL import Image,ImageTk,ImageEnhance
import numpy as np

from smoothingWindow import smoothingWindow
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
        
        self.left_frame = tk.Frame(self.root, width=300, height=800, bg="lightblue")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)
        self.right_frame = tk.Frame(self.root, width=800, height=800, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)
        
        
        # tkinker
    
        # Rozszerzenie Histogramu
        self.histogram_button = tk.Button(self.left_frame, text="Histogram", command=self.streaching)
        self.histogram_button.pack()
        
        # Wyrównanie
        
        self.histogram2_button = tk.Button(self.left_frame, text="Equalization", command=self.equalization)
        self.histogram2_button.pack()
        
        # Binaryzacja manualna
        
        self.threshold_frame = tk.Frame(self.left_frame)
        self.threshold_frame.pack()
    
        self.threshold_label = tk.Label(self.threshold_frame, text="Lower Threshold:")
        self.threshold_label.pack(side=tk.LEFT)
    
        self.threshold_entry = tk.Entry(self.threshold_frame)
        self.threshold_entry.pack(side=tk.LEFT)
            
        self.manual_binaryzation_button = tk.Button(self.left_frame, text="Manual Binaryzation", command=self.manualBinaryzation)
        self.manual_binaryzation_button.pack()
        
        # Binaryzacja 1 - Procentowa selekcja czarnego 
        
        self.percentage_black_frame = tk.Frame(self.left_frame)
        self.percentage_black_frame.pack()
    
        self.percentage_black_label = tk.Label(self.percentage_black_frame, text="% Black:")
        self.percentage_black_label.pack(side=tk.LEFT)
    
        self.percentage_black_entry = tk.Entry(self.percentage_black_frame)
        self.percentage_black_entry.pack(side=tk.LEFT)
        
        self.percent_black_selection_button = tk.Button(self.left_frame, text="Percent Black Selection", command=self.percentBlackSelection)
        self.percent_black_selection_button.pack()
        
        # Binaryzacja 2 - Selekcja iteracyjna średniej
        
        self.mean_iterative_selection_button = tk.Button(self.left_frame, text="Mean Iterative Selection", command=self.meanIterativeSelection)
        self.mean_iterative_selection_button.pack()
        
        # Binaryzacja 3 - Selekcja entropii
        
        # self.entropy_selection_button = tk.Button(self.left_frame, text="Entropy Selection", command=self.entropySelection)
        # self.entropy_selection_button.pack()
        
        # # Binaryzacja 4 - Bląd Minimalny
        
        # self.minimum_error_button = tk.Button(self.left_frame, text="Minimum Error", command=self.minimumError)
        # self.minimum_error_button.pack()
        

        # Cancel changes
        
        self.cancel_button = tk.Button(self.left_frame, text="Cancel", command=self.cancelChanges)
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
        
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))    
        
        #
        #   self images
        #
        self.original_PILImage = None
        self.PILImage = None
        self.original_photoimage = None          
        self.image_tk = None                
        self.image_id = None
        # scale factor for zooming
        self.scale_factor = 1.0
        # Mouse binds    
        self.canvas.bind("<MouseWheel>", self.zoom)
    
    def setImage(self, photo_image):
        self.scale_factor = 1.0
        self.original_photoimage = photo_image
        self.image_tk = photo_image
        self.image_id = self.canvas.create_image(0,0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))            
        
    def setPILImage(self, PILImage):
        self.PILImage = PILImage
        self.image_tk = ImageTk.PhotoImage(PILImage)
        
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
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
    
    def cancelChanges(self):
        if self.original_photoimage==None: 
            return
        self.PILImage = self.original_PILImage
        self.canvas.delete("all")  
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photoimage)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    # Projekt 5

    def streaching(self):
        if self.original_photoimage==None: 
            return
        
    
        width, height = self.PILImage.size
        pixels = list(self.PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
            

        i_max = 255
        max_vals = [0,0,0]
        min_vals = [255,255,255]
        same_vals = [False, False, False]
        
        threads = []                        
        
        #
        #   get max and min
        #
        # thread Worker
        def minMaxWorker(line, max_vals, min_vals): 
            width = len(line)
            for x in range(width):
                r,g,b = line[x]
                rgb = [r,g,b]
                for a in range(0,3):
                    max_vals[a] = max(max_vals[a], rgb[a])
                    min_vals[a] = min(min_vals[a], rgb[a])
            return min_vals, max_vals
            
        # create workers
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = minMaxWorker, args=(line, max_vals, min_vals,)))
            threads[-1].start()
        
        # join workers
        for thread in threads:
            min_vals_temp, max_val_temp = thread.join()
            for a in range(0,3):
                max_vals[a] = max(max_vals[a], min_vals_temp[a])
                min_vals[a] = min(min_vals[a], max_val_temp[a])

        # check if values are the same
        for a in range(0,3):
            if max_vals[a] == min_vals[a]:
                same_vals[a] = True
        
        threads = []

        #
        #   streaching
        #
        
        # streaching worker
        def streachingWorker(line, y, i_max, max_vals, min_vals, same_vals): 
            width = len(line)
            line_pixels = []
            for x in range(width):
                r,g,b = line[x]
                rgb = [r,g,b]
                # calculate LUT 
                LUT = [0,0,0]
                LUT[0] = int((i_max/(max_vals[0] - min_vals[0])) * (r - min_vals[0]))
                LUT[1] = int((i_max/(max_vals[1] - min_vals[1])) * (g - min_vals[1]))
                LUT[2] = int((i_max/(max_vals[2] - min_vals[2])) * (b - min_vals[2]))
                # if not same_vals[0]:
                #     LUT[0] = int((i_max/(max_vals[0] - min_vals[0])) * (r - min_vals[0]))
                # else:
                #     LUT[0] = int((i_max/1)) * (r - min_vals[0])
                # if not same_vals[1]:
                #     LUT[1] = int((i_max/(max_vals[1] - min_vals[1])) * (g - min_vals[1]))
                # else:
                #     LUT[1] = int((i_max/1)) * (g - min_vals[1])
                # if not same_vals[2]:
                #     LUT[2] = int((i_max/(max_vals[2] - min_vals[2])) * (b - min_vals[2]))
                # else:
                #     LUT[2] = int((i_max/1)) * (b - min_vals[2])        
            
                for a in range(0,3):
                    if LUT[a] < 0:
                        LUT[a] = 0
                    elif LUT[a] > 255:
                        LUT[a] = 255
                line_pixels.append((LUT[0], LUT[1], LUT[2]))
            return line_pixels
        
        # create streaching workers
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = streachingWorker, args=(line, x, i_max, max_vals, min_vals, same_vals)))
            threads[-1].start()
        
            
        # join workers
        res_pixels = []
        for x in range(len(threads)):
            line_pixels = threads[x].join()
            res_pixels.extend(line_pixels)
        res_img.putdata(res_pixels)
        
        threads = []   
        
        image_array = np.array(self.PILImage, dtype=np.uint8)
        smooth_array = np.array(res_img, dtype=np.uint8)
        smoothingWindow(self.root, image_array, smooth_array)
    
        self.setPILImage(res_img)
    
    def equalization(self):
        if self.original_photoimage==None: 
            return        
        width, height = self.PILImage.size
        pixels = list(self.PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
            
        img_array = np.array(self.PILImage)   
        D = 0
        
        hist_r = np.histogram(img_array[:,:,0], bins=256, range=(0,255))[0]
        hist_g = np.histogram(img_array[:,:,1], bins=256, range=(0,255))[0]
        hist_b = np.histogram(img_array[:,:,2], bins=256, range=(0,255))[0]
        
        # get amount of pixels
        r_pixel = 0
        g_pixel = 0
        b_pixel = 0
        for i in range(len(hist_r)):
            r_pixel = r_pixel + hist_r[i]
            g_pixel = g_pixel + hist_g[i]
            b_pixel = b_pixel + hist_b[i]
    
        
        D_r = []
        D_g = []
        D_b = []
        r_sum = 0
        g_sum = 0
        b_sum = 0
        # calculate D
        for i in range(len(hist_r)):
            r_sum = r_sum + hist_r[i]
            g_sum = g_sum + hist_g[i]
            b_sum = b_sum + hist_b[i]
            D_r.append(r_sum/r_pixel)
            D_g.append(g_sum/g_pixel)
            D_b.append(b_sum/b_pixel)
        
        # find first D non-zero value
        non_zero_D_r = 0
        non_zero_D_g = 0
        non_zero_D_b = 0
        for i in range(len(D_r)):
            if D_r[i] != 0:
                non_zero_D_r = D_r[i]
                break
        for i in range(len(D_g)):
            if D_g[i] != 0:
                non_zero_D_g = D_g[i]
                break
        for i in range(len(D_b)):
            if D_b[i] != 0:
                non_zero_D_b = D_b[i]
                break
        
        LUT_r = [0] * 256
        LUT_g = [0] * 256
        LUT_b = [0] * 256
        # calculate LUT
        for a in range(len(D_r)):
            LUT_r[a] = int(((D_r[a] - non_zero_D_r)/(1-non_zero_D_r)) * 255)
            LUT_g[a] = int(((D_g[a] - non_zero_D_g)/(1-non_zero_D_g)) * 255)
            LUT_b[a] = int(((D_b[a] - non_zero_D_b)/(1-non_zero_D_b)) * 255)
            
        
        img = np.zeros_like(img_array)
        
        img[:,:,0] = np.take(LUT_r, img_array[:,:,0].astype(np.uint8))
        img[:,:,1] = np.take(LUT_g, img_array[:,:,1].astype(np.uint8))
        img[:,:,2] = np.take(LUT_b, img_array[:,:,2].astype(np.uint8))
        
        res_img = Image.fromarray(img.astype(np.uint8))
        self.setPILImage(res_img)
        
        equal_array = np.array(res_img, dtype=np.uint8)
        smoothingWindow(self.root, img_array, equal_array)

    def BinaryzationWorker(self, line, threshold): 
        width = len(line)
        line_pixels = []
        for x in range(width):
            r,g,b = line[x]
            rgb = [r,g,b]
            if int((r+g+b)/3) < threshold:
                line_pixels.append((0,0,0))
            else:
                line_pixels.append((255,255,255))
        return line_pixels

    def manualBinaryzation(self):
        if self.original_photoimage==None: 
            return

        width, height = self.PILImage.size
        pixels = list(self.PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
        threads = []     
            
        threshold = self.threshold_entry.get()
        
        if threshold == "":
            messagebox.showerror("Error", "Please enter threshold value")
            return
        
        threshold = int(threshold)
        
        # create workers
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = self.BinaryzationWorker, args=(line, threshold)))
            threads[-1].start()
        
        # join workers
        res_pixels = []
        for x in range(len(threads)):
            line_pixels = threads[x].join()
            res_pixels.extend(line_pixels)
        res_img.putdata(res_pixels)
        
        threads = []   
        
        # image_array = np.array(self.PILImage, dtype=np.uint8)
        # binary_array = np.array(res_img, dtype=np.uint8)
        # smoothingWindow(self.root, image_array, binary_array)
    
        self.setPILImage(res_img)
            
    def percentBlackSelection(self):
        if self.original_photoimage==None: 
            return
        
        percent = self.percentage_black_entry.get()
        
        if percent == "":
            messagebox.showerror("Error", "Please enter % value (0-100)")
            return
        
        percent = int(percent)
        
        
        width, height = self.PILImage.size
        pixels = list(self.PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
 
        threads = [] 
        
        # change values to avg pixel value
        def averageSetWorker(line): 
            line_pixels = []
            for x in range(len(line)):
                r,g,b = line[x]
                line_pixels.append((r+g+b)//3)
            return line_pixels
        
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = averageSetWorker, args=(line,)))
            threads[-1].start()
        
        # join workers
        avg_pixels = []
        for x in range(len(threads)):
            line_pixels = threads[x].join()
            avg_pixels.extend(line_pixels)
        threads = []   
        
        # calculate percent black
        avg_pixels.sort()
        
        percent_black = int(len(avg_pixels)*percent//100)
        
        threshold = avg_pixels[percent_black]
        
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = self.BinaryzationWorker, args=(line, threshold,)))
            threads[-1].start()
        
        # join workers
        res_pixels = []
        for x in range(len(threads)):
            line_pixels = threads[x].join()
            res_pixels.extend(line_pixels)
        res_img.putdata(res_pixels)
        
        threads = []   

        self.setPILImage(res_img)
        
    def meanIterativeSelection(self):
        if self.original_photoimage==None: 
            return
        width, height = self.PILImage.size
        pixels = list(self.PILImage.getdata())
        res_img = Image.new("RGB", (width, height))
        
        threads = []
        mean_values = []
        res_pixels = []
        def meanWorker(line):
            line_pixels = []
            for x in range(len(line)):
                r,g,b = line[x]
                line_pixels.append((r+g+b)//3)
            mean_val = sum(line_pixels)//len(line_pixels)
            return mean_val
        
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = meanWorker, args=(line,)))
            threads[-1].start()
        for x in range(len(threads)):
            mean_values.append(threads[x].join())
        threads = []
        
        # calculate threash hold value as mean value of all pixels
        threshold = sum(mean_values)//len(mean_values)
        
        for x in range(0, len(pixels), width):
            end_of_line = x+width
            line = pixels[x:end_of_line]
            if end_of_line > len(pixels):
                line = pixels[x:]
            threads.append(CustomThread(target = self.BinaryzationWorker, args=(line, threshold,)))
            threads[-1].start()
        for x in range(len(threads)):
            line_pixels = threads[x].join()
            res_pixels.extend(line_pixels)
        res_img.putdata(res_pixels)
        
        threads = []
        
        
        self.setPILImage(res_img)
        
        
if __name__ == "__main__":#
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
