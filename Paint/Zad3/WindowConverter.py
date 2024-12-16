import tkinter as tk
from tkinter import ttk, messagebox


class ConverterWindow:
    def __init__(self, root):
        
        
        self.root = root
        self.root.title("RGB AND CMYK Converter")
        self.root.geometry("800x800")
        
        
        self.rgb_prev = [100,100,100]
        self.rgb = [100,100,100]
        self.cmyk_prev = [0,0,0,61]
        self.cmyk = [0,0,0,61]
        
        self.user_input = True
        
        
        # divide window
        
        self.upper_frame = tk.Frame(self.root, width=800, height=400, bg="lightblue")
        self.upper_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.upper_frame.pack_propagate(False)
        
        self.lower_frame = tk.Frame(self.root, width=800, height=400, bg="white")
        self.lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.lower_frame.pack_propagate(False)
        
        #
        # upper frame 
        #

        self.upper_left_frame = tk.Frame(self.upper_frame, width=250, height=200, bg="lightblue")
        self.upper_left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.upper_left_frame.pack_propagate(False)
        
        self.upper_right_frame = tk.Frame(self.upper_frame, width=250, height=200, bg="lightblue")
        self.upper_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.upper_right_frame.pack_propagate(False)
        
        #
        # upper frame LEFT rgb-> cmyk
        #

        
        
        # frame for entrys
        self.rgb_to_entry_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.rgb_to_entry_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.r_to_value_entry = tk.Entry(self.rgb_to_entry_frame, width=10)
        self.r_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
                
        self.g_to_value_entry = tk.Entry(self.rgb_to_entry_frame, width=10)
        self.g_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
        
        self.b_to_value_entry = tk.Entry(self.rgb_to_entry_frame, width=10)
        self.b_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
        
        self.r_to_value_entry.insert(0,"100")
        self.g_to_value_entry.insert(0,"100")
        self.b_to_value_entry.insert(0,"100")
        
        # frane for r slider
        self.rgb_to_r_slider_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.rgb_to_r_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.r_to_value_label = ttk.Label(self.rgb_to_r_slider_frame, text="R")
        self.r_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.r_to_value_slider = ttk.Scale(
            self.rgb_to_r_slider_frame,
            from_=0,
            to=255,
            orient='horizontal',
            value=100  
        )
        self.r_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        
        # frane for g slider
        self.rgb_to_g_slider_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.rgb_to_g_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.g_to_value_label = ttk.Label(self.rgb_to_g_slider_frame, text="G")
        self.g_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.g_to_value_slider = ttk.Scale(
            self.rgb_to_g_slider_frame,
            from_=0,
            to=255,
            orient='horizontal',
            value=100  
        )
        self.g_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        # frane for b slider
        self.rgb_to_b_slider_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.rgb_to_b_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.b_to_value_label = ttk.Label(self.rgb_to_b_slider_frame, text="B")
        self.b_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.b_to_value_slider = ttk.Scale(
            self.rgb_to_b_slider_frame,
            from_=0,
            to=255,
            orient='horizontal',
            value=100  
        )
        self.b_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)

        # bindings
        
        self.r_to_value_entry.bind("<KeyRelease>", self.entry_fun_1)
        self.g_to_value_entry.bind("<KeyRelease>", self.entry_fun_1)
        self.b_to_value_entry.bind("<KeyRelease>", self.entry_fun_1)
        
        self.r_to_value_slider.config(command=self.slider_fun_1)
        self.g_to_value_slider.config(command=self.slider_fun_1)
        self.b_to_value_slider.config(command=self.slider_fun_1)

        
        
        
        # cmyk from
        self.c_from_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.c_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.c_from_label = ttk.Label(self.c_from_frame, text="C")
        self.c_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.c_from_value = ttk.Label(self.c_from_frame, text="100")
        self.c_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        self.m_from_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.m_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.m_from_label = ttk.Label(self.m_from_frame, text="M")
        self.m_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.m_from_value = ttk.Label(self.m_from_frame, text="100")
        self.m_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        self.y_from_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.y_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.y_from_label = ttk.Label(self.y_from_frame, text="Y")
        self.y_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.y_from_value = ttk.Label(self.y_from_frame, text="100")
        self.y_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        self.k_from_frame = tk.Frame(self.upper_left_frame, width=250, height=30, bg="lightblue")
        self.k_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.k_from_label = ttk.Label(self.k_from_frame, text="K")
        self.k_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.k_from_value = ttk.Label(self.k_from_frame, text="100")
        self.k_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        
        

        
        #
        #   UPPER FRAME RIGHT CMYK to RGB
        #
        
        self.cmyk_to_entry_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.cmyk_to_entry_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.c_to_value_entry = tk.Entry(self.cmyk_to_entry_frame, width=10)
        self.c_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
                
        self.m_to_value_entry = tk.Entry(self.cmyk_to_entry_frame, width=10)
        self.m_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
        
        self.y_to_value_entry = tk.Entry(self.cmyk_to_entry_frame, width=10)
        self.y_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
        
        self.k_to_value_entry = tk.Entry(self.cmyk_to_entry_frame, width=10)
        self.k_to_value_entry.pack(side=tk.LEFT,pady=5,padx=5)
        
        self.c_to_value_entry.insert(0,"0")
        self.m_to_value_entry.insert(0,"0")
        self.y_to_value_entry.insert(0,"0")
        self.k_to_value_entry.insert(0,"61")
        
        # frane for c slider
        self.cmyk_to_c_slider_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.cmyk_to_c_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.c_to_value_label = ttk.Label(self.cmyk_to_c_slider_frame, text="C")
        self.c_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.c_to_value_slider = ttk.Scale(
            self.cmyk_to_c_slider_frame,
            from_=0,
            to=100,
            orient='horizontal',
            value=0  
        )
        self.c_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        # frane for m slider
        self.cmyk_to_m_slider_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.cmyk_to_m_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.m_to_value_label = ttk.Label(self.cmyk_to_m_slider_frame, text="M")
        self.m_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.m_to_value_slider = ttk.Scale(
            self.cmyk_to_m_slider_frame,
            from_=0,
            to=100,
            orient='horizontal',
            value=0  
        )
        self.m_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        # frane for y slider
        self.cmyk_to_y_slider_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.cmyk_to_y_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.y_to_value_label = ttk.Label(self.cmyk_to_y_slider_frame, text="Y")
        self.y_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.y_to_value_slider = ttk.Scale(
            self.cmyk_to_y_slider_frame,
            from_=0,
            to=100,
            orient='horizontal',
            value=0  
        )
        self.y_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        # frane for k slider
        self.cmyk_to_k_slider_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.cmyk_to_k_slider_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.k_to_value_label = ttk.Label(self.cmyk_to_k_slider_frame, text="K")
        self.k_to_value_label.pack(side=tk.LEFT,pady=5, padx=5)
        self.k_to_value_slider = ttk.Scale(
            self.cmyk_to_k_slider_frame,
            from_=0,
            to=100,
            orient='horizontal',
            value=61  
        )
        self.k_to_value_slider.pack(padx=5, pady=5, fill='x', side=tk.LEFT)
        
        # bindings
        
        self.c_to_value_entry.bind("<KeyRelease>", self.entry_fun_2)
        self.m_to_value_entry.bind("<KeyRelease>", self.entry_fun_2)
        self.y_to_value_entry.bind("<KeyRelease>", self.entry_fun_2)
        self.k_to_value_entry.bind("<KeyRelease>", self.entry_fun_2)
        
        self.c_to_value_slider.config(command=self.slider_fun_2)
        self.m_to_value_slider.config(command=self.slider_fun_2)
        self.y_to_value_slider.config(command=self.slider_fun_2)
        self.k_to_value_slider.config(command=self.slider_fun_2)
        
        # rgb from
        self.r_from_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.r_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.r_from_label = ttk.Label(self.r_from_frame, text="R")
        self.r_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.r_from_value = ttk.Label(self.r_from_frame, text="100")
        self.r_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        self.g_from_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.g_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.g_from_label = ttk.Label(self.g_from_frame, text="G")
        self.g_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.g_from_value = ttk.Label(self.g_from_frame, text="100")
        self.g_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        self.b_from_frame = tk.Frame(self.upper_right_frame, width=250, height=30, bg="lightblue")
        self.b_from_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.b_from_label = ttk.Label(self.b_from_frame, text="B")
        self.b_from_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.b_from_value = ttk.Label(self.b_from_frame, text="100")
        self.b_from_value.pack(side=tk.LEFT, pady=5, padx=5)
        
        
        #
        # lower frame
        #
        
        self.lower_left_frame = tk.Frame(self.lower_frame, width=400, height=400, bg="lightblue")
        self.lower_left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.lower_left_frame.pack_propagate(False)
        
        self.lower_right_frame = tk.Frame(self.lower_frame, width=400, height=400, bg="lightblue")
        self.lower_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.lower_right_frame.pack_propagate(False)
        
        
        # preview CMYK to RGB

        self.canvas_2 = tk.Canvas(self.lower_right_frame, width=400, height=400)
        self.canvas_2.create_rectangle(0, 0, 400, 400, fill="#FF5733", outline="")
        self.canvas_2.pack(side=tk.LEFT)
        
        
        # preview RGB to CMYK
        
    
        self.canvas_1 = tk.Canvas(self.lower_left_frame, width=400, height=400)
        self.canvas_1.create_rectangle(0, 0, 400, 400, fill="#FF5733", outline="")
        self.canvas_1.pack(side=tk.LEFT)

        
    def cmyk_to_rgb(self, c, m, y, k):
        c,m,y,k = int(c), int(m), int(y), int(k)
        RGB_SCALE = 255
        CMYK_SCALE = 100
        r = RGB_SCALE * (1.0 - c / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
        g = RGB_SCALE * (1.0 - m / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
        b = RGB_SCALE * (1.0 - y / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
        return r, g, b
        
    def rgb_to_cmyk(self, r, g, b):
        r = int(r)
        g = int(g)
        b = int(b)
        CMYK_SCALE = 100
        RGB_SCALE = 255
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, CMYK_SCALE # black

        # rgb [0,255] -> cmy [0,1]
        c = 1 - r / RGB_SCALE
        m = 1 - g / RGB_SCALE
        y = 1 - b / RGB_SCALE

        # extract out k [0, 1]
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        # rescale to the range [0,CMYK_SCALE]
        c = int(c * CMYK_SCALE)
        m = int(m * CMYK_SCALE)
        y = int(y * CMYK_SCALE)
        k = int(k * CMYK_SCALE)
        
        return c, m, y, k
    
    
    
    def entry_fun_1(self,value):
        r = self.r_to_value_entry.get()
        g = self.g_to_value_entry.get()
        b = self.b_to_value_entry.get()
        rgb = [r,g,b]
        
        self.rgb = rgb
        none_value = False
        # if value is not between 0 and 255
        for a in range(0,3):
            try:
                if not 0 <= int(rgb[a]) <= 255:
                    messagebox.showerror("Error", "RGB values must be between 0 and 255")
                    self.rgb = self.rgb_prev
                elif rgb[a] == "":
                    pass
            except ValueError:
                if not rgb[a] == "":
                    messagebox.showerror("Error", "RGB values must be between 0 and 255")
                    self.rgb = self.rgb_prev
                else:
                    none_value = True
        if not none_value:
            self.update_1()
    
    def slider_fun_1(self, value):   
        if not self.user_input:
            return
        r = int(self.r_to_value_slider.get())
        g = int(self.g_to_value_slider.get())
        b = int(self.b_to_value_slider.get())
        rgb = [r,g,b]
        
        self.rgb = rgb
        
        self.update_1()
        
    
    
    
    def update_1(self):
        self.rgb_prev = self.rgb
        r = self.rgb[0]
        g = self.rgb[1]
        b = self.rgb[2]
        # update entrys
        self.r_to_value_entry.delete(0, tk.END)
        self.r_to_value_entry.insert(0, r)
        self.g_to_value_entry.delete(0, tk.END)
        self.g_to_value_entry.insert(0, g)
        self.b_to_value_entry.delete(0, tk.END)
        self.b_to_value_entry.insert(0, b)
        
        self.user_input = False
        self.r_to_value_slider.set(int(r))
        self.g_to_value_slider.set(int(g))
        self.b_to_value_slider.set(int(b))
        self.user_input = True
        # convert values to cmyk
        
        cmyk = self.rgb_to_cmyk(self.rgb[0], self.rgb[1], self.rgb[2])
        
        self.c_from_value.config(text=int(cmyk[0]))
        self.m_from_value.config(text=int(cmyk[1]))
        self.y_from_value.config(text=int(cmyk[2]))
        self.k_from_value.config(text=int(cmyk[3]))

        
        # show in canvas
        
        self.canvas_1.delete("all")
        rgb_hex = '#%02x%02x%02x' % (int(r), int(g), int(b))
        # rgb_hex = '#{:02x}{:02x}{:02x}'.format(self.rgb[0], self.rgb[1], self.rgb[2])
        self.canvas_1.create_rectangle(0, 0, 400, 400, fill=rgb_hex, outline="")
        
    def entry_fun_2(self,value):
        c = self.c_to_value_entry.get()
        m = self.m_to_value_entry.get()
        y = self.y_to_value_entry.get()
        k = self.k_to_value_entry.get()
        cmyk = [c,m,y,k]
        
        self.cmyk = cmyk
        none_value = False
        # if value is not between 0 and 255
        for a in range(0,4):
            try:
                if not 0 <= int(cmyk[a]) <= 100:
                    messagebox.showerror("Error", "CMYK values must be between 0 and 100")
                    self.cmyk = self.cmyk_prev
                elif cmyk[a] == "":
                    pass
            except ValueError:
                if not cmyk[a] == "":
                    messagebox.showerror("Error", "CMYK values must be between 0 and 100")
                    self.cmyk = self.cmyk_prev
                else:
                    none_value = True
        if not none_value:
            self.update_2()
        
    
    def slider_fun_2(self, value):   
        if not self.user_input:
            return
        c = int(self.c_to_value_slider.get())
        m = int(self.m_to_value_slider.get())
        y = int(self.y_to_value_slider.get())
        k = int(self.k_to_value_slider.get())
        cmyk = [c,m,y,k]
        
        self.cmyk = cmyk
        
        self.update_2()
    

    
    def update_2(self):
        self.cmyk_prev = self.cmyk
        c = self.cmyk[0]
        m = self.cmyk[1]
        y = self.cmyk[2]
        k = self.cmyk[3]
        # update entrys
        self.c_to_value_entry.delete(0, tk.END)
        self.c_to_value_entry.insert(0, c)
        self.m_to_value_entry.delete(0, tk.END) 
        self.m_to_value_entry.insert(0, m)
        self.y_to_value_entry.delete(0, tk.END)
        self.y_to_value_entry.insert(0, y)
        self.k_to_value_entry.delete(0, tk.END)
        self.k_to_value_entry.insert(0, k)
        
        self.user_input = False
        self.c_to_value_slider.set(int(c))
        self.m_to_value_slider.set(int(m))
        self.y_to_value_slider.set(int(y))
        self.k_to_value_slider.set(int(k))
        self.user_input = True
        # convert values to rgb
        rgb = self.cmyk_to_rgb(c, m, y, k)
        
        self.r_from_value.config(text=int(rgb[0]))
        self.g_from_value.config(text=int(rgb[1]))
        self.b_from_value.config(text=int(rgb[2]))
        
        # show in canvas
        
        self.canvas_2.delete("all")
        rgb_hex = '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        self.canvas_2.create_rectangle(0, 0, 400, 400, fill=rgb_hex, outline="")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterWindow(root)
    root.mainloop()
