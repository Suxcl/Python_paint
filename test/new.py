import tkinter as tk
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from tkinter import Frame
import sys

class OpenGLCanvas(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.initialize_opengl()
        self.after(10, self.draw)

    def initialize_opengl(self):
        if not callable(glutCreateWindow):
            raise RuntimeError("GLUT is not properly installed or glutCreateWindow is unavailable.")

        self.glut_id = glutCreateWindow(b"3D Cube")
        glutDisplayFunc(self.render_scene)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1)

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        # Draw a cube
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)  # Red
        glVertex3f(1, 1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)

        glColor3f(0, 1, 0)  # Green
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)

        glColor3f(0, 0, 1)  # Blue
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)

        glColor3f(1, 1, 0)  # Yellow
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)

        glColor3f(1, 0, 1)  # Magenta
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)

        glColor3f(0, 1, 1)  # Cyan
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)
        glEnd()

        glutSwapBuffers()

    def draw(self):
        glutPostRedisplay()
        self.after(16, self.draw)  # Approx. 60 FPS

def main():
    root = tk.Tk()
    root.title("3D Cube in Tkinter with OpenGL")
    root.geometry("800x600")

    try:
        OpenGLCanvas(root)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    root.mainloop()

if __name__ == "__main__":
    main()
