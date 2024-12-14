import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),  # 0
    (1, 1, -1),   # 1
    (-1, 1, -1),  # 2
    (-1, -1, -1), # 3
    (1, -1, 1),   # 4
    (1, 1, 1),    # 5
    (-1, -1, 1),  # 6
    (-1, 1, 1)    # 7
)

edges = (
    (0,1), (0,3), (0,4),
    (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7),
    (5,1), (5,4), (5,7)
)

def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
    
    # Set up the perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    # Set up the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)
    
    # Initial rotation to make cube visible
    glRotatef(45, 1, 1, 0)
    
    # Variables for mouse rotation
    mouse_pressed = False
    last_mouse_pos = None
    total_rotation_x = 45
    total_rotation_y = 45
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pressed = True
                    last_mouse_pos = pygame.mouse.get_pos()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    mouse_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION and mouse_pressed:
                current_mouse_pos = pygame.mouse.get_pos()
                if last_mouse_pos:
                    delta_x = current_mouse_pos[0] - last_mouse_pos[0]
                    delta_y = current_mouse_pos[1] - last_mouse_pos[1]
                    
                    total_rotation_y += delta_x * 0.5
                    total_rotation_x += delta_y * 0.5
                    
                last_mouse_pos = current_mouse_pos
        
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset modelview matrix and apply transformations
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(total_rotation_x, 1, 0, 0)
        glRotatef(total_rotation_y, 0, 1, 0)
        
        # Draw cube
        draw_cube()
        
        # Update display
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()