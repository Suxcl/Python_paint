import tkinter as tk

class ResizeableShapeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Resize Shape with Scroll Button")

        # Create a Canvas widget
        self.canvas = tk.Canvas(master, width=400, height=300, bg="white")
        self.canvas.pack()

        # Initial coordinates for the bounding box of the circle
        self.x0, self.y0 = 150, 100
        self.x1, self.y1 = 250, 200

        # Draw the initial circle on the canvas
        self.shape_id = self.canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill="blue")

        # Bind the middle mouse button for resizing on drag
        self.canvas.bind("<ButtonPress-2>", self.start_resizing)
        self.canvas.bind("<B2-Motion>", self.resize_shape)

    def start_resizing(self, event):
        # Store the initial click position
        self.start_y = event.y

    def resize_shape(self, event):
        # Calculate the change in y position
        delta_y = event.y - self.start_y

        # Adjust the y1 and x1 positions based on the drag distance
        # This allows resizing by changing the bottom-right corner coordinates (x1, y1)
        new_x1 = self.x1 + delta_y // 2  # Use delta_y to adjust both x1 and y1
        new_y1 = self.y1 + delta_y // 2

        # Update the coordinates for the shape
        self.canvas.coords(self.shape_id, self.x0, self.y0, new_x1, new_y1)

        # Update the stored x1 and y1 coordinates
        self.x1, self.y1 = new_x1, new_y1

# Create the main window
root = tk.Tk()
app = ResizeableShapeApp(root)
root.mainloop()
