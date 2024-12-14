import tkinter as tk
from tkinter import ttk

class CompressionWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        
        self.callback_function = callback
        self.title("Compress Image")
        self.geometry("300x150")
        
        # Slider
        self.slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient='horizontal',
            value=100  
        )
        self.slider.pack(pady=20, padx=20, fill='x')
        
        # label for percentage
        self.value_label = ttk.Label(self, text="100%")
        self.value_label.pack(pady=5)
        
        # Save Button
        self.save_button = ttk.Button(
            self,
            text="Save",
            command=self.save_value
        )
        self.save_button.pack(pady=10)
        
        # Bind slider movement to update label
        self.slider.config(command=self.update_label)
    
    def update_label(self, value):
        self.value_label.config(text=f"{int(float(value))}%")
    
    def save_value(self):
        value = self.slider.get()
        self.callback_function(value)  
        self.destroy() 
        
        