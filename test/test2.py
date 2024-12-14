import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Define vertices and their RGB colors
vertices = (
    (1, -1, -1, 1, 0, 0),    # 0 Red corner
    (1, 1, -1, 1, 1, 0),     # 1 Yellow corner
    (-1, 1, -1, 0, 1, 0),    # 2 Green corner
    (-1, -1, -1, 0, 0, 0),   # 3 Black corner
    (1, -1, 1, 1, 0, 1),     # 4 Magenta corner
    (1, 1, 1, 1, 1, 1),      # 5 White corner
    (-1, -1, 1, 0, 0, 1),    # 6 Blue corner
    (-1, 1, 1, 0, 1, 1)      # 7 Cyan corner
)

faces = (
    (0, 1, 2, 3),  # Back face
    (4, 5, 1, 0),  # Right face
    (6, 7, 5, 4),  # Front face
    (3, 2, 7, 6),  # Left face
    (1, 5, 7, 2),  # Top face
    (4, 0, 3, 6)   # Bottom face
)

def get_ray_from_click(mx, my, width, height):
    # Get the normalized device coordinates
    x = (2.0 * mx) / width - 1.0
    y = 1.0 - (2.0 * my) / height
    
    # Get the current modelview and projection matrices
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    
    # Combine projection and modelview matrices
    MVP = np.dot(np.array(projection), np.array(modelview))
    MVP_inv = np.linalg.inv(MVP)
    
    # Create near and far points in clip space
    near_point = np.array([x, y, -1.0, 1.0])
    far_point = np.array([x, y, 1.0, 1.0])
    
    # Transform to world space
    near_point = np.dot(MVP_inv, near_point)
    far_point = np.dot(MVP_inv, far_point)
    
    # Normalize by w component
    near_point = near_point / near_point[3]
    far_point = far_point / far_point[3]
    
    # Return only the xyz components
    return near_point[:3], far_point[:3]

def calculate_intersection_plane(start, end):
    # Calculate ray direction
    direction = end - start
    direction = direction / np.linalg.norm(direction)
    
    # Define plane point (center of cube) and normal (facing camera)
    plane_point = np.array([0.0, 0.0, 0.0])
    plane_normal = direction
    
    # Calculate intersection
    d = np.dot(plane_normal, plane_point - start) / np.dot(plane_normal, direction)
    intersection = start + d * direction
    
    return intersection, plane_normal

def draw_cross_section(intersection_point, normal):
    # Calculate basis vectors for the cross-section plane
    up = np.array([0, 1, 0])
    right = np.cross(normal, up)
    if np.all(right == 0):
        right = np.array([1, 0, 0])
    up = np.cross(right, normal)
    
    # Normalize vectors
    right = right / np.linalg.norm(right)
    up = up / np.linalg.norm(up)
    
    # Size of the cross-section
    size = 2.0
    
    # Calculate corners of the cross-section
    corners = [
        intersection_point + (right + up) * size,
        intersection_point + (right - up) * size,
        intersection_point + (-right - up) * size,
        intersection_point + (-right + up) * size
    ]
    
    # Draw cross-section
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glBegin(GL_QUADS)
    glColor4f(1.0, 1.0, 1.0, 0.5)  # Semi-transparent white
    for corner in corners:
        glVertex3f(*corner)
    glEnd()
    
    glDisable(GL_BLEND)

def draw_cube():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3f(vertices[vertex][3], vertices[vertex][4], vertices[vertex][5])
            glVertex3f(vertices[vertex][0], vertices[vertex][1], vertices[vertex][2])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # Enable depth testing and smooth shading
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    
    # Set up the perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    # Set up the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)
    
    # Initial rotation
    glRotatef(45, 1, 1, 0)
    
    # Variables for mouse rotation and intersection
    mouse_pressed = False
    last_mouse_pos = None
    total_rotation_x = 45
    total_rotation_y = 45
    intersection_point = None
    plane_normal = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pressed = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 3:  # Right mouse button
                    try:
                        # Calculate ray from click position
                        mx, my = pygame.mouse.get_pos()
                        start, end = get_ray_from_click(mx, my, display[0], display[1])
                        intersection_point, plane_normal = calculate_intersection_plane(start, end)
                    except Exception as e:
                        print(f"Error calculating intersection: {e}")
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
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
        
        # Draw cross-section if intersection exists
        if intersection_point is not None and plane_normal is not None:
            draw_cross_section(intersection_point, plane_normal)
        
        # Update display
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()