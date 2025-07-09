import math
import numpy as np
import tkinter as tk

class Matrix3D:
    """matrix for 3D"""
    
    @staticmethod
    def identity():
        return np.eye(4)
    
    @staticmethod
    def translate(tx, ty, tz):
        mat = np.eye(4)
        mat[0, 3] = tx
        mat[1, 3] = ty
        mat[2, 3] = tz
        return mat
    
    @staticmethod
    def scale(sx, sy, sz):
        mat = np.eye(4)
        mat[0, 0] = sx
        mat[1, 1] = sy
        mat[2, 2] = sz
        return mat
    
    @staticmethod
    def rotate_x(angle):
        """X axis"""
        mat = np.eye(4)
        c = math.cos(angle)
        s = math.sin(angle)
        mat[1, 1] = c
        mat[1, 2] = -s
        mat[2, 1] = s
        mat[2, 2] = c
        return mat
    
    @staticmethod
    def rotate_y(angle):
        """Y axis"""
        mat = np.eye(4)
        c = math.cos(angle)
        s = math.sin(angle)
        mat[0, 0] = c
        mat[0, 2] = s
        mat[2, 0] = -s
        mat[2, 2] = c
        return mat
    
    @staticmethod
    def rotate_z(angle):
        """Z axis"""
        mat = np.eye(4)
        c = math.cos(angle)
        s = math.sin(angle)
        mat[0, 0] = c
        mat[0, 1] = -s
        mat[1, 0] = s
        mat[1, 1] = c
        return mat
    
    @staticmethod
    def perspective(fov, aspect, near, far):
        """perspective & projection"""
        mat = np.zeros((4, 4))
        f = 1.0 / math.tan(fov / 2)
        mat[0, 0] = f / aspect
        mat[1, 1] = f
        mat[2, 2] = (far + near) / (near - far)
        mat[2, 3] = (2 * far * near) / (near - far)
        mat[3, 2] = -1
        return mat
    
    @staticmethod
    def look_at(eye, target, up):
        """view (camera coordinate)"""
        forward = (target - eye) / np.linalg.norm(target - eye)
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        
        mat = np.eye(4)
        mat[0, 0:3] = right
        mat[1, 0:3] = up
        mat[2, 0:3] = -forward
        mat[0, 3] = -np.dot(right, eye)
        mat[1, 3] = -np.dot(up, eye)
        mat[2, 3] = np.dot(forward, eye)
        return mat

class WireframeObject:
    """base class of wireframe objects"""
    
    def __init__(self, vertices, edges, color="#00ff00"):
        """
        vertices: vertex list [[x, y, z], ...]
        edges: edge list [[vertex 1, vertex 2], ...]
        color: color
        """
        self.vertices = np.array(vertices)
        self.edges = edges
        self.color = color
        self.is_flame = False  # may be no use
        self.transform_matrix = Matrix3D.identity()
    
    def set_transform(self, matrix):
        self.transform_matrix = matrix
    
    def translate(self, tx, ty, tz):
        """shift in world coord."""
        self.transform_matrix = Matrix3D.translate(tx, ty, tz) @ self.transform_matrix
    
    def rotate(self, rx, ry, rz):
        """rotation in world coord. """
        rot_x = Matrix3D.rotate_x(rx)
        rot_y = Matrix3D.rotate_y(ry)
        rot_z = Matrix3D.rotate_z(rz)
        self.transform_matrix = rot_z @ rot_y @ rot_x @ self.transform_matrix
    
    def scale(self, sx, sy, sz):
        self.transform_matrix = Matrix3D.scale(sx, sy, sz) @ self.transform_matrix
    
    def get_transformed_vertices(self):
        # translate to homogeneous coord.
        homogeneous = np.ones((len(self.vertices), 4))
        homogeneous[:, 0:3] = self.vertices
        
        # do it!!
        transformed = (self.transform_matrix @ homogeneous.T).T
        
        return transformed

class Camera:
    def __init__(self, position, target, up, fov=60, aspect=1.0, near=0.1, far=100):
        self.position = np.array(position, dtype=float)
        self.target = np.array(target, dtype=float)
        self.up = np.array(up, dtype=float)
        self.fov = math.radians(fov)
        self.aspect = aspect
        self.near = near
        self.far = far
        
        self.view_matrix = Matrix3D.look_at(self.position, self.target, self.up)
        self.projection_matrix = Matrix3D.perspective(self.fov, self.aspect, self.near, self.far)
    
    def update(self):
        """update camera (view) matrix """
        self.view_matrix = Matrix3D.look_at(self.position, self.target, self.up)
        self.projection_matrix = Matrix3D.perspective(self.fov, self.aspect, self.near, self.far)

class WireframeRenderer:
    """rendering class"""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.camera = Camera([0, 0, 5], [0, 0, 0], [0, 1, 0], aspect=width/height)
        self.objects = []
        self.f_time = 0
        self.w_time = 0
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def set_camera(self, camera):
        self.camera = camera
    
    def world_to_screen(self, world_pos):
        # view transform
        view_pos = self.camera.view_matrix @ world_pos
        
        # projection transform
        proj_pos = self.camera.projection_matrix @ view_pos
        
        # clipping → NDC
        if proj_pos[3] != 0:
            ndc = proj_pos / proj_pos[3]
        else:
            ndc = proj_pos + 10
        
        # viewport
        screen_x = (ndc[0] + 1) * self.width / 2
        screen_y = (1 - ndc[1]) * self.height / 2
        
        return screen_x, screen_y, ndc[2]
    
    def render(self):
        self.canvas.delete("all")
        
        for obj in self.objects:
            # retreive each the transformed vertices
            transformed_vertices = obj.get_transformed_vertices()
            
            # transform to screen 
            screen_vertices = []
            for vertex in transformed_vertices:
                screen_x, screen_y, depth = self.world_to_screen(vertex)
                screen_vertices.append((screen_x, screen_y, depth))
            
            # traverse edges
            for edge in obj.edges:
                v1_idx, v2_idx = edge
                
                # edge's id is legal or not
                if v1_idx >= len(screen_vertices) or v2_idx >= len(screen_vertices):
                    continue
                
                x1, y1, z1 = screen_vertices[v1_idx]
                x2, y2, z2 = screen_vertices[v2_idx]
                
                # clipping
                if z1 < -1 or z1 > 1 or z2 < -1 or z2 > 1:
                    continue
                
                # in the screen?
                if (0 <= x1 <= self.width and 0 <= y1 <= self.height and
                    0 <= x2 <= self.width and 0 <= y2 <= self.height):
                    
                    # color factor( don't think good idea...)
                    depth_factor = (z1 + z2) / 2
                    intensity = max(0.1, 1 - depth_factor * 0.5)
                    
                    t = None
                    if hasattr(obj, 'is_flame') and obj.is_flame:
                        self.f_time += 0.05
                        xxx_intensity = 80
                        t = self.f_time
                    if hasattr(obj, 'is_warp') and obj.is_warp:
                        self.w_time += 0.03
                        t = self.w_time
                        xxx_intensity = 180
                    if t:
                        flame_start_z = -3.5
                        flame_end_z = -10.5
                        avg_z = (transformed_vertices[v1_idx][2] + transformed_vertices[v2_idx][2]) / 2
                        
                        if flame_end_z <= avg_z <= flame_start_z:
                            transparency = ((avg_z - flame_end_z) * (1 - math.cos(t) /3)
                                            )/ (flame_start_z - flame_end_z)
                            transparency = max(0.0, min(1.0, transparency))
                        else:
                            transparency = 1.0
                        
                        red_intensity = int(255 * intensity * transparency)
                        color = f"#{red_intensity:02x}{xxx_intensity:02x}{xxx_intensity:02x}"
                        line_width = max(1, int(4 * transparency))
                    else:
                        # color procedure for normal object 
                        if obj.color.startswith('#'):
                            base_color = obj.color
                        else:
                            base_color = "#00ff00"
                        
                        line_width = 2
                        
                        # depth intensity must be reflect to color
                        if base_color == "#00ff00": 
                            color = f"#{0:02x}{int(intensity*255):02x}{0:02x}"
                        elif base_color == "#ff0000":
                            color = f"#{int(intensity*255):02x}{0:02x}{0:02x}"
                        elif base_color == "#0000ff":
                            color = f"#{0:02x}{0:02x}{int(intensity*255):02x}"
                        elif base_color == "#ffff00":
                            color = f"#{int(intensity*255):02x}{int(intensity*255):02x}{0:02x}"
                        elif base_color == "#ff00ff":
                            color = f"#{int(intensity*255):02x}{0:02x}{int(intensity*255):02x}"
                        elif base_color == "#00ffff":
                            color = f"#{0:02x}{int(intensity*255):02x}{int(intensity*255):02x}"
                        else:
                            color = f"#{int(intensity*255):02x}{int(intensity*255):02x}{int(intensity*255):02x}"
                    
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=line_width)


