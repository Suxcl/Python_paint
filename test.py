import tkinter as tk
from tkinter import PhotoImage

def load_ppm(file_path):
    """
    Reads a PPM (P3 or P6) file and converts it to a Tkinter-compatible PhotoImage object.
    
    :param file_path: Path to the PPM file.
    :return: Tkinter PhotoImage object.
    """
    with open(file_path, 'rb') as f:
        # Read the header
        header = f.readline().decode().strip()
        if header not in {'P3', 'P6'}:
            raise ValueError("Unsupported PPM format. Only P3 and P6 are supported.")
        
        # Skip comments
        while True:
            line = f.readline().decode().strip()
            if not line.startswith('#'):
                break
        
        # Get image dimensions
        width, height = map(int, line.split())
        max_val = int(f.readline().decode().strip())
        
        # Validate max color value
        if max_val != 255:
            raise ValueError("Only 8-bit per channel PPM files are supported.")
        
        # Read pixel data
        if header == 'P3':
            # ASCII format
            data = []
            for line in f:
                data.extend(map(int, line.decode().split()))
        elif header == 'P6':
            # Binary format
            data = list(f.read())
        
        # Convert data to a PhotoImage-compatible format
        pixels = []
        for i in range(0, len(data), 3):
            r, g, b = data[i:i+3]
            pixels.append(f"#{r:02x}{g:02x}{b:02x}")
        
        # Create PhotoImage
        image = PhotoImage(width=width, height=height)
        for y in range(height):
            line_data = "{" + " ".join(pixels[y*width:(y+1)*width]) + "}"
            image.put(line_data, (0, y))
        
        return image

# Example usage in a Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    image = load_ppm("pixilart-spritep6.ppm")
    label = tk.Label(root, image=image)
    label.pack()
    root.mainloop()
