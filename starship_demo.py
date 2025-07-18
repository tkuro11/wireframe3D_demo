import numpy as np
import tkinter as tk
from tkinter import Canvas
import math

from wireframe_3d_lib import Camera, Matrix3D, WireframeRenderer, WireframeObject

### functions for making indivisual parts of a starship

# HULL (cyan part)
def create_starship_hull():
    vertices = [
        # Front section (sharp tip)
        [0, 0, 4],      # 0: tip
        [-0.5, -0.2, 3], # 1: front left bottom
        [0.5, -0.2, 3],  # 2: front right bottom
        [-0.5, 0.2, 3],  # 3: front left top
        [0.5, 0.2, 3],   # 4: front right top
        
        # Middle section
        [-1, -0.3, 1],   # 5: middle left bottom
        [1, -0.3, 1],    # 6: middle right bottom
        [-1, 0.3, 1],    # 7: middle left top
        [1, 0.3, 1],     # 8: middle right top
        
        # Rear section
        [-0.8, -0.2, -1], # 9: rear left bottom
        [0.8, -0.2, -1],  # 10: rear right bottom
        [-0.8, 0.2, -1],  # 11: rear left top
        [0.8, 0.2, -1],   # 12: rear right top
    ]
    
    edges = [
        # Connection from front to middle section
        [0, 1], [0, 2], [0, 3], [0, 4],
        [1, 2], [2, 4], [4, 3], [3, 1],
        [1, 5], [2, 6], [3, 7], [4, 8],
        
        # Middle section outline
        [5, 6], [6, 8], [8, 7], [7, 5],
        [5, 9], [6, 10], [7, 11], [8, 12],
        
        # Rear section outline
        [9, 10], [10, 12], [12, 11], [11, 9],
    ]
    
    return WireframeObject(vertices, edges, "#00ffff")

# TANK (yellow parts)
def create_fuel_tank():
    vertices = [
        # Tank front section (circular cross-section)
        [-0.4, -0.4, 2],   # 0: front left bottom
        [0.4, -0.4, 2],    # 1: front right bottom
        [0.4, 0.4, 2],     # 2: front right top
        [-0.4, 0.4, 2],    # 3: front left top
        
        # Tank middle section (maximum diameter)
        [-0.6, -0.6, 0],   # 4: middle left bottom
        [0.6, -0.6, 0],    # 5: middle right bottom
        [0.6, 0.6, 0],     # 6: middle right top
        [-0.6, 0.6, 0],    # 7: middle left top
        
        # Tank rear section
        [-0.4, -0.4, -2],  # 8: rear left bottom
        [0.4, -0.4, -2],   # 9: rear right bottom
        [0.4, 0.4, -2],    # 10: rear right top
        [-0.4, 0.4, -2],   # 11: rear left top
        
        # Connection pipe
        [-0.1, 0, 1],      # 12: pipe front
        [-0.1, 0, -1],     # 13: pipe rear
    ]

    edges = [
        # Front cross-section
        [0, 1], [1, 2], [2, 3], [3, 0],
        # Middle cross-section
        [4, 5], [5, 6], [6, 7], [7, 4],
        # Rear cross-section
        [8, 9], [9, 10], [10, 11], [11, 8],
        # Vertical connection lines
        [0, 4], [1, 5], [2, 6], [3, 7],
        [4, 8], [5, 9], [6, 10], [7, 11],
        # Connection pipe
        [12, 13], [12, 2], [13, 10],
    ]
    
    return WireframeObject(vertices, edges, "#ffff00")

def create_warp_nacelle():
    """warp unit (warp motor)"""
    vertices = [
        # Nacelle front section
        [-0.3, -0.2, 3],   # 0: front left bottom
        [0.3, -0.2, 3],    # 1: front right bottom
        [0.3, 0.2, 3],     # 2: front right top
        [-0.3, 0.2, 3],    # 3: front left top
        
        # Nacelle middle section
        [-0.5, -0.3, 1],   # 4: middle left bottom
        [0.5, -0.3, 1],    # 5: middle right bottom
        [0.5, 0.3, 1],     # 6: middle right top
        [-0.5, 0.3, 1],    # 7: middle left top
        
        [-0.5, -0.3, -1],  # 8: middle rear left bottom
        [0.5, -0.3, -1],   # 9: middle rear right bottom
        [0.5, 0.3, -1],    # 10: middle rear right top
        [-0.5, 0.3, -1],   # 11: middle rear left top
        
        # Nacelle rear section
        [-0.3, -0.2, -3],  # 12: rear left bottom
        [0.3, -0.2, -3],   # 13: rear right bottom
        [0.3, 0.2, -3],    # 14: rear right top
        [-0.3, 0.2, -3],   # 15: rear left top
        
        # Warp coils (internal structure)
        [-0.2, -0.1, 0.5], # 16: coil1
        [0.2, -0.1, 0.5],  # 17
        [0.2, 0.1, 0.5],   # 18
        [-0.2, 0.1, 0.5],  # 19
        [-0.2, -0.1, -0.5], # 20: coil2
        [0.2, -0.1, -0.5],  # 21
        [0.2, 0.1, -0.5],   # 22
        [-0.2, 0.1, -0.5],  # 23
    ]
    
    edges = [
        # Hull outline lines
        [0, 1], [1, 2], [2, 3], [3, 0],  # front section
        [4, 5], [5, 6], [6, 7], [7, 4],  # middle front
        [8, 9], [9, 10], [10, 11], [11, 8],  # middle rear
        [12, 13], [13, 14], [14, 15], [15, 12],  # rear section
        
        # Vertical connection lines
        [0, 4], [1, 5], [2, 6], [3, 7],
        [4, 8], [5, 9], [6, 10], [7, 11],
        [8, 12], [9, 13], [10, 14], [11, 15],
        
        # Warp coils
        [16, 17], [17, 18], [18, 19], [19, 16],  # coil1
        [20, 21], [21, 22], [22, 23], [23, 20],  # coil2
        [16, 20], [17, 21], [18, 22], [19, 23],  # inter-coil connections
    ]
    
    return WireframeObject(vertices, edges, "#00ffff")

def create_starship_engine():
    vertices = [
        # Engine body (cylindrical)
        [-0.3, -0.3, -1.5], # 0: front face left bottom
        [0.3, -0.3, -1.5],  # 1: front face right bottom
        [0.3, 0.3, -1.5],   # 2: front face right top
        [-0.3, 0.3, -1.5],  # 3: front face left top
        
        [-0.4, -0.4, -3],   # 4: rear face left bottom
        [0.4, -0.4, -3],    # 5: rear face right bottom
        [0.4, 0.4, -3],     # 6: rear face right top
        [-0.4, 0.4, -3],    # 7: rear face left top
        
        # Engine nozzle
        [-0.2, -0.2, -3.5], # 8: nozzle left bottom
        [0.2, -0.2, -3.5],  # 9: nozzle right bottom
        [0.2, 0.2, -3.5],   # 10: nozzle right top
        [-0.2, 0.2, -3.5],  # 11: nozzle left top
    ]
    
    edges = [
        # Front face
        [0, 1], [1, 2], [2, 3], [3, 0],
        # Rear face
        [4, 5], [5, 6], [6, 7], [7, 4],
        # Connection between front and rear faces
        [0, 4], [1, 5], [2, 6], [3, 7],
        # Nozzle
        [8, 9], [9, 10], [10, 11], [11, 8],
        [4, 8], [5, 9], [6, 10], [7, 11],
    ]
    
    return WireframeObject(vertices, edges, "#ff0000")

def create_engine_flame(warp = False):
    vertices = []
    edges = []

    # Divide bar into multiple segments to create transparency gradient
    segments = 15
    start_z = -1.5
    end_z = -4.5
    width_start = 0.2
    width_end = 0.05
    
    for i in range(segments + 1):
        progress = i / segments
        z = start_z + (end_z - start_z) * progress
        width = width_start + (width_end - width_start) * progress
        
        # Rectangle vertices for each segment
        base_idx = i * 4
        vertices.extend([
            [-width, -width, z],
            [width, -width, z],
            [width, width, z],
            [-width, width, z],
        ])

        # Edges within segment
        if i < segments:  # except for the last segment
            # Rectangle of current segment
            edges.extend([
                [base_idx, base_idx + 1],
                [base_idx + 1, base_idx + 2],
                [base_idx + 2, base_idx + 3],
                [base_idx + 3, base_idx],
            ])
    # Rectangle of the last segment
    last_base = segments * 4
    edges.extend([
        [last_base, last_base + 1],
        [last_base + 1, last_base + 2],
        [last_base + 2, last_base + 3],
        [last_base + 3, last_base],
    ])
    
    flame = WireframeObject(vertices, edges, "#3f9000")
    if warp:
        flame.is_warp = True
    else:
        flame.is_flame = True

    return flame

def create_star_field():
    vertices = []
    edges = []

    # Place random stars
    np.random.seed(42)  # For reproducibility
    for i in range(2800): # rather large value because final movement decided yet
        x = np.random.uniform(-80, 80)
        y = np.random.uniform(-80, 80)
        z = np.random.uniform(-80, 100)
        vertices.append([x, y, z])
        x += 0
        y += 0
        z += 1     # stars're treated as lines aligned to z axis
        vertices.append([x, y, z])
    
    for i in range(0, len(vertices), 2):
        edges.append([i, i+1])
    
    return WireframeObject(vertices, edges, "#ffffff")

def create_grid_surface(size=10, grid_spacing=5, y_level=-5):
    """making gridded ground"""
    vertices = []
    edges = []
    half_size = size // 2
    
    # vertical (x)
    for x in range(-half_size, half_size + 1, grid_spacing):
        start_idx = len(vertices)
        vertices.append([x, y_level, -half_size])
        vertices.append([x, y_level, half_size])
        edges.append([start_idx, start_idx + 1])
    
    # horizontal (z)
    for z in range(-half_size, half_size + 1, grid_spacing):
        start_idx = len(vertices)
        vertices.append([-half_size, y_level, z])
        vertices.append([half_size, y_level, z])
        edges.append([start_idx, start_idx + 1])
    
    return WireframeObject(vertices, edges, "#ff00ff")

# Animation class
class StarshipDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Starship Animation - 3D Wireframe")
        self.root.geometry("1200x900")
        self.root.configure(bg='black')
        # Canvas
        self.canvas = Canvas(self.root, width=1200, height=900, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.renderer = WireframeRenderer(self.canvas, 1200, 900)
        # Camera settings
        self.camera = Camera([0, 5, 1], [0, 0, 0], [0, 1, 0], aspect=1200/900)
        self.renderer.set_camera(self.camera)
        
        self.starship_parts = []
        # Add objects
        self.setup_scene()
        
        self.time = 0
        self.ship_rotation = 0
        self.animate()
    
    def setup_scene(self):
        stars = create_star_field()
        self.renderer.add_object(stars)
        
        # grid surface (not use)
        #grid_surface = create_grid_surface(size=200, grid_spacing=3, y_level=-10)
        #self.renderer.add_object(grid_surface)
        
        hull = create_starship_hull()
        self.renderer.add_object(hull)
        self.starship_parts.append(hull)
        
        # left TANK
        left_tank = create_fuel_tank()
        left_tank.translate(-2.5, 0, 0)
        self.renderer.add_object(left_tank)
        self.starship_parts.append(left_tank)
        
        # right TANK
        right_tank = create_fuel_tank()
        right_tank.translate(2.5, 0, 0)
        self.renderer.add_object(right_tank)
        self.starship_parts.append(right_tank)
        
        # left warp nacelle
        left_nacelle = create_warp_nacelle()
        left_nacelle.translate(-3.5, -1, 0)
        self.renderer.add_object(left_nacelle)
        self.starship_parts.append(left_nacelle)
        
        # right warp nacelle
        right_nacelle = create_warp_nacelle()
        right_nacelle.translate(3.5, -1, 0)
        self.renderer.add_object(right_nacelle)
        self.starship_parts.append(right_nacelle)
        
        main_engine = create_starship_engine()
        main_engine.translate(0, -0.5, 0)
        main_engine.scale(1.5, 1.5, 1.5)
        self.renderer.add_object(main_engine)
        self.starship_parts.append(main_engine)
        
        # engine's FLAME
        main_flame = create_engine_flame()
        main_flame.translate(0, -0.5, 0)
        main_flame.scale(1.5, 1.5, 15.8)   # make it long
        self.renderer.add_object(main_flame)
        self.starship_parts.append(main_flame)
        
        # warp unit's ENERGY FLOW (left)
        left_warp_effect = create_engine_flame(True)
        left_warp_effect.translate(-3.5, -1, 0)
        left_warp_effect.scale(0.8, 0.8, 2)
        self.renderer.add_object(left_warp_effect)
        self.starship_parts.append(left_warp_effect)

        # warp unit's ENERGY FLOW (right)       
        right_warp_effect = create_engine_flame(True)
        right_warp_effect.translate(3.5, -1, 0)
        right_warp_effect.scale(0.8, 0.8, 2)
        self.renderer.add_object(right_warp_effect)
        self.starship_parts.append(right_warp_effect)
    
    def animate(self):
        """animation"""
        self.time += 0.03
        if self.time > 40: self.time = 0
        
        # path of flight (go straight)
        flight_height = -5
        ship_x = self.time * 2
        ship_y = flight_height + 1 * math.sin(self.time * 0.3)
        ship_z = 0
        
        # camera lookat position 
        self.camera.position[0] = 10 +ship_x  # back of starship
        self.camera.position[1] = ship_y + 5 * math.cos(self.time*0.3)  # up and down
        self.camera.position[2] = ship_z - 15   # Z
        self.camera.target = [ship_x, ship_y, ship_z]
        self.camera.update()
        
        # bank angle
        ship_bank = math.sin(self.time * 0.7) * 0.3
        ship_pitch = math.sin(self.time * 0.5) * 0.2
        ship_yaw = self.time * 0.2
        
        # Update each part of the starship
        for i, part in enumerate(self.starship_parts):
            part.transform_matrix = Matrix3D.identity()
            
            # For hull
            if i == 0:  # hull
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            
            # For fuel tanks
            elif i == 1:  # left fuel tank
                part.translate(-2.5, 0, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            elif i == 2:  # right fuel tank
                part.translate(2.5, 0, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            
            # For warp nacelles (slight vibration effect)
            elif i == 3:  # left warp nacelle
                nacelle_vibration = 0.02 * math.sin(self.time * 15)
                part.translate(-3.5, -1 + nacelle_vibration, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            elif i == 4:  # right warp nacelle
                nacelle_vibration = 0.02 * math.sin(self.time * 15 + math.pi/3)
                part.translate(3.5, -1 + nacelle_vibration, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            
            # For main engine
            elif i == 5:  # main engine
                part.scale(1.5, 1.5, 1.5)
                part.translate(0, -0.5, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            
            # For main engine flame
            elif i == 6:  # main flame
                part.scale(1.5, 1.5, 1.8)
                part.translate(0, -0.5, -2)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            
            # For warp effects (static, no animation)
            elif i == 7:  # left warp effect
                part.scale(0.8, 0.8, 2)
                part.translate(-3.5, -1, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
            elif i == 8:  # right warp effect
                part.scale(0.8, 0.8, 2)
                part.translate(3.5, -1, 0)
                part.rotate(0, 0, ship_bank)
                part.translate(ship_x, ship_y, ship_z)
        
        # rotation of background stars (stars are now at index 0, grid surface at index 1)
        if len(self.renderer.objects) > 0:
            stars = self.renderer.objects[0]
            stars.transform_matrix = Matrix3D.identity()
            stars.rotate(0, self.time * 0.05, 0)
        
        self.renderer.render()
        
        # next frame
        self.root.after(16, self.animate)  # Approximately 60FPS
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = StarshipDemo()
    demo.run()
