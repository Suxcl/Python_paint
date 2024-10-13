import tkinter as tk

class CanvasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Select Canvas Element")

        # Create a Canvas widget
        self.canvas = tk.Canvas(master, width=500, height=400, bg="white")
        self.canvas.pack()

        # Draw some rectangles on the canvas
        self.rectangles = []
        for i in range(5):
            x1 = 50 + i * 80
            y1 = 100
            x2 = x1 + 50
            y2 = y1 + 50
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
            self.rectangles.append(rect_id)

        # Bind the mouse click event
        self.canvas.bind("<Button-1>", self.select_item)

    def select_item(self, event):
        # Get the mouse click coordinates
        x, y = event.x, event.y

        # Find the closest item at the clicked coordinates
        clicked_items = self.canvas.find_closest(x, y)

        # Check if any item was clicked and change its color
        for item_id in clicked_items:
            # Check if the clicked item is one of our rectangles
            if item_id in self.rectangles:
                self.canvas.itemconfig(item_id, fill="red")  # Change the color to red
                break  # Stop after changing the color of the first selected rectangle

# Create the main window
root = tk.Tk()
app = CanvasApp(root)
root.mainloop()
