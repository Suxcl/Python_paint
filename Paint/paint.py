from tkinter import *

class paint:
    _instance = None
    canvas = None
    shapes = []
    selected_shape = None
    
    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(paint, self).__new__(self)
        return self._instance
    
    
    
    
    
        
        
        
        