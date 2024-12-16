import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

class smoothingWindow(tk.Toplevel):
    def __init__(self, parent, pixels, smoothed_pixels):
        super().__init__(parent)
    
        self.title("Compress Image")
        self.geometry("1000x800")
    
        self.pixels = pixels
        self.smoothed_pixels = smoothed_pixels
            
        self.plot_frame_upper = tk.Frame(self, width=800, height=400, bg="lightblue")
        self.plot_frame_upper.pack(side=tk.TOP, fill=tk.BOTH)
        self.plot_frame_upper.pack_propagate(False)
        
        self.plot_frame_lower = tk.Frame(self, width=800, height=400, bg="white")
        self.plot_frame_lower.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.plot_frame_lower.pack_propagate(False)
    
        
        # First Histogram
        
        plt.figure(figsize=(6, 4))
        plt.hist(self.pixels.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.7)
        plt.title("Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        
        self.fig = plt.gcf()  # Get the current figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame_upper)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        
        plt.close(self.fig)
        
        # Second Histogram
        
        plt.figure(figsize=(6, 4))
        plt.hist(self.smoothed_pixels.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.7)
        plt.title("Smoothed Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        
        self.fig = plt.gcf()  # Get the current figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame_lower)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        
        plt.close(self.fig)

        
        