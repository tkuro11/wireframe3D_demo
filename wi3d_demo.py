import numpy as np
import tkinter as tk
from tkinter import Canvas
import math
from wireframe_3d_lib import WireframeObject, WireframeRenderer, Camera, Matrix3D

def create_cube(size=1.0):
    s = size / 2
    vertices = [
        [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
        [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
    ]
    
    edges = [
        # back
        [0, 1], [1, 2], [2, 3], [3, 0],
        # front
        [4, 5], [5, 6], [6, 7], [7, 4],
        # inbetween
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    
    return WireframeObject(vertices, edges)

def create_grid(size=10, divisions=10):
    vertices = []
    edges = []
    
    step = size / divisions
    start = -size / 2
    
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            x = start + i * step
            z = start + j * step
            vertices.append([x, 0, z])
    
    for i in range(divisions + 1):
        for j in range(divisions):
            # horizontal
            idx1 = i * (divisions + 1) + j
            idx2 = i * (divisions + 1) + j + 1
            edges.append([idx1, idx2])
            
            # vertical
            idx1 = i * (divisions + 1) + j
            idx2 = (i + 1) * (divisions + 1) + j
            if i < divisions:
                edges.append([idx1, idx2])
    
    return WireframeObject(vertices, edges)

class WireframeDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Wireframe Library Demo")
        self.root.geometry("1000x800")
        self.root.configure(bg='black')
        
        self.canvas = Canvas(self.root, width=1000, height=800, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.renderer = WireframeRenderer(self.canvas, 1000, 800)
        
        self.camera = Camera([5.0, 3.0, 8.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], aspect=1000/800)
        self.renderer.set_camera(self.camera)
        
        self.setup_scene()
        
        self.angle = 0
        self.animate()
    
    def setup_scene(self):
        grid = create_grid(10, 20)
        self.renderer.add_object(grid)
        
        cube1 = create_cube(1.0)
        cube1.translate(-2, 1, 0)
        self.renderer.add_object(cube1)
        
        cube2 = create_cube(1.5)
        cube2.translate(2, 0.75, -1)
        self.renderer.add_object(cube2)
        
        cube3 = create_cube(0.8)
        cube3.translate(0, 2, 1)
        self.renderer.add_object(cube3)

        angles = np.linspace(0, np.pi*2, 30)
        self.points = list(zip(3*np.cos(angles), 3*np.sin(angles)))
        for x,y in self.points:
            c = create_cube(0.4)
            c.translate(0, x, y)
            self.renderer.add_object(c)

    
    def animate(self):
        self.angle += 0.02
        
        radius = 8
        self.camera.position[0] =  radius * math.cos(self.angle/2)*2
        self.camera.position[2] = radius * math.sin(self.angle/2)
        self.camera.update()
        
        if len(self.renderer.objects) > 1:
            cube1 = self.renderer.objects[1]
            cube1.transform_matrix = Matrix3D.identity()
            cube1.translate(-2, 1, 0)
            cube1.rotate(self.angle, self.angle * 0.7, 0)
            
            cube2 = self.renderer.objects[2]
            cube2.transform_matrix = Matrix3D.identity()
            cube2.translate(2, 0.75, -1)
            cube2.rotate(0, self.angle * 0.5, self.angle * 0.3)
            
            cube3 = self.renderer.objects[3]
            cube3.transform_matrix = Matrix3D.identity()
            cube3.translate(0, 2, 1)
            cube3.rotate(self.angle * 0.3, 0, self.angle * 0.8)

        for i in range(4, len(self.renderer.objects)):
            c = self.renderer.objects[i]
            c.transform_matrix = Matrix3D.identity()
            c.rotate(self.angle * 0.2, 0, self.angle* 0.3*i)
            c.translate(0, self.points[i-4][0], self.points[i-4][1])
            c.rotate(self.angle * 0.2, 0, self.angle* 0.3)
        
        self.renderer.render()
        
        self.root.after(10, self.animate)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = WireframeDemo()
    demo.run()
