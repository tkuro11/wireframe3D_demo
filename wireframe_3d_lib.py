import numpy as np
import tkinter as tk
from tkinter import Canvas
import math

class Matrix3D:
    """3D変換マトリックス操作クラス"""
    
    @staticmethod
    def identity():
        """単位行列を返す"""
        return np.eye(4)
    
    @staticmethod
    def translate(tx, ty, tz):
        """平行移動行列"""
        mat = np.eye(4)
        mat[0, 3] = tx
        mat[1, 3] = ty
        mat[2, 3] = tz
        return mat
    
    @staticmethod
    def scale(sx, sy, sz):
        """スケール行列"""
        mat = np.eye(4)
        mat[0, 0] = sx
        mat[1, 1] = sy
        mat[2, 2] = sz
        return mat
    
    @staticmethod
    def rotate_x(angle):
        """X軸回転行列"""
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
        """Y軸回転行列"""
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
        """Z軸回転行列"""
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
        """パースペクティブ投影行列"""
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
        """ビュー行列（カメラ座標系）"""
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
    """ワイヤーフレームオブジェクト"""
    
    def __init__(self, vertices, edges):
        """
        vertices: 頂点リスト [[x, y, z], ...]
        edges: エッジリスト [[頂点1, 頂点2], ...]
        """
        self.vertices = np.array(vertices)
        self.edges = edges
        self.transform_matrix = Matrix3D.identity()
    
    def set_transform(self, matrix):
        """変換行列を設定"""
        self.transform_matrix = matrix
    
    def translate(self, tx, ty, tz):
        """平行移動"""
        self.transform_matrix = Matrix3D.translate(tx, ty, tz) @ self.transform_matrix
    
    def rotate(self, rx, ry, rz):
        """回転"""
        rot_x = Matrix3D.rotate_x(rx)
        rot_y = Matrix3D.rotate_y(ry)
        rot_z = Matrix3D.rotate_z(rz)
        self.transform_matrix = rot_z @ rot_y @ rot_x @ self.transform_matrix
    
    def scale(self, sx, sy, sz):
        """スケール"""
        self.transform_matrix = Matrix3D.scale(sx, sy, sz) @ self.transform_matrix
    
    def get_transformed_vertices(self):
        """変換された頂点を取得"""
        # 同次座標に変換
        homogeneous = np.ones((len(self.vertices), 4))
        homogeneous[:, 0:3] = self.vertices
        
        # 変換適用
        transformed = (self.transform_matrix @ homogeneous.T).T
        
        return transformed

class Camera:
    """カメラクラス"""
    
    def __init__(self, position, target, up, fov=60, aspect=1.0, near=0.1, far=100):
        self.position = np.array(position)
        self.target = np.array(target)
        self.up = np.array(up)
        self.fov = math.radians(fov)
        self.aspect = aspect
        self.near = near
        self.far = far
        
        self.view_matrix = Matrix3D.look_at(self.position, self.target, self.up)
        self.projection_matrix = Matrix3D.perspective(self.fov, self.aspect, self.near, self.far)
    
    def update(self):
        """カメラ行列を更新"""
        self.view_matrix = Matrix3D.look_at(self.position, self.target, self.up)
        self.projection_matrix = Matrix3D.perspective(self.fov, self.aspect, self.near, self.far)

class WireframeRenderer:
    """ワイヤーフレームレンダラー"""
    
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.camera = Camera([0, 0, 5], [0, 0, 0], [0, 1, 0], aspect=width/height)
        self.objects = []
    
    def add_object(self, obj):
        """オブジェクトを追加"""
        self.objects.append(obj)
    
    def set_camera(self, camera):
        """カメラを設定"""
        self.camera = camera
    
    def world_to_screen(self, world_pos):
        """ワールド座標からスクリーン座標へ変換"""
        # ビュー変換
        view_pos = self.camera.view_matrix @ world_pos
        
        # 投影変換
        proj_pos = self.camera.projection_matrix @ view_pos
        
        # クリッピング座標 → NDC
        if proj_pos[3] != 0:
            ndc = proj_pos / proj_pos[3]
        else:
            ndc = proj_pos
        
        # ビューポート変換
        screen_x = (ndc[0] + 1) * self.width / 2
        screen_y = (1 - ndc[1]) * self.height / 2
        
        return screen_x, screen_y, ndc[2]
    
    def render(self):
        """レンダリング"""
        self.canvas.delete("all")
        
        for obj in self.objects:
            # 変換された頂点を取得
            transformed_vertices = obj.get_transformed_vertices()
            
            # スクリーン座標に変換
            screen_vertices = []
            for vertex in transformed_vertices:
                screen_x, screen_y, depth = self.world_to_screen(vertex)
                screen_vertices.append((screen_x, screen_y, depth))
            
            # エッジを描画
            for edge in obj.edges:
                v1_idx, v2_idx = edge
                
                # 範囲チェック
                if v1_idx >= len(screen_vertices) or v2_idx >= len(screen_vertices):
                    continue
                
                x1, y1, z1 = screen_vertices[v1_idx]
                x2, y2, z2 = screen_vertices[v2_idx]
                
                # 深度によるクリッピング
                if z1 < -1 or z1 > 1 or z2 < -1 or z2 > 1:
                    continue
                
                # 画面内チェック
                if (0 <= x1 <= self.width and 0 <= y1 <= self.height and
                    0 <= x2 <= self.width and 0 <= y2 <= self.height):
                    
                    # 深度による色の変化
                    depth_factor = (z1 + z2) / 2
                    intensity = max(0.3, 1 - depth_factor * 0.5)
                    color = f"#{0:02x}{int(intensity*255):02x}{int(intensity*255):02x}"
                    
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

# プリミティブ生成関数
def create_cube(size=1.0):
    """立方体を生成"""
    s = size / 2
    vertices = [
        [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # 後面
        [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # 前面
    ]
    
    edges = [
        # 後面
        [0, 1], [1, 2], [2, 3], [3, 0],
        # 前面
        [4, 5], [5, 6], [6, 7], [7, 4],
        # 接続
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    
    return WireframeObject(vertices, edges)

def create_grid(size=10, divisions=10):
    """グリッドを生成"""
    vertices = []
    edges = []
    
    step = size / divisions
    start = -size / 2
    
    # 頂点生成
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            x = start + i * step
            z = start + j * step
            vertices.append([x, 0, z])
    
    # エッジ生成
    for i in range(divisions + 1):
        for j in range(divisions):
            # 水平線
            idx1 = i * (divisions + 1) + j
            idx2 = i * (divisions + 1) + j + 1
            edges.append([idx1, idx2])
            
            # 垂直線
            idx1 = i * (divisions + 1) + j
            idx2 = (i + 1) * (divisions + 1) + j
            if i < divisions:
                edges.append([idx1, idx2])
    
    return WireframeObject(vertices, edges)

# デモアプリケーション
class WireframeDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Wireframe Library Demo")
        self.root.geometry("1000x800")
        self.root.configure(bg='black')
        
        # Canvas
        self.canvas = Canvas(self.root, width=1000, height=800, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # レンダラー
        self.renderer = WireframeRenderer(self.canvas, 1000, 800)
        
        # カメラ設定
        self.camera = Camera([5, 3, 8], [0, 0, 0], [0, 1, 0], aspect=1000/800)
        self.renderer.set_camera(self.camera)
        
        # オブジェクト追加
        self.setup_scene()
        
        # アニメーション
        self.angle = 0
        self.animate()
    
    def setup_scene(self):
        """シーンセットアップ"""
        # グリッド
        grid = create_grid(10, 20)
        self.renderer.add_object(grid)
        
        # 立方体1
        cube1 = create_cube(1.0)
        cube1.translate(-2, 1, 0)
        self.renderer.add_object(cube1)
        
        # 立方体2
        cube2 = create_cube(1.5)
        cube2.translate(2, 0.75, -1)
        self.renderer.add_object(cube2)
        
        # 立方体3
        cube3 = create_cube(0.8)
        cube3.translate(0, 2, 1)
        self.renderer.add_object(cube3)
    
    def animate(self):
        """アニメーション"""
        self.angle += 0.02
        
        # カメラを回転
        radius = 8
        self.camera.position[0] = radius * math.cos(self.angle)
        self.camera.position[2] = radius * math.sin(self.angle)
        self.camera.update()
        
        # 立方体を回転
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
        
        # レンダリング
        self.renderer.render()
        
        # 次のフレーム
        self.root.after(30, self.animate)
    
    def run(self):
        self.root.mainloop()

# 実行
if __name__ == "__main__":
    demo = WireframeDemo()
    demo.run()