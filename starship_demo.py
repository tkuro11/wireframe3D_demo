import numpy as np
import tkinter as tk
from tkinter import Canvas
import math

from wireframe_3d_lib import Camera, Matrix3D, WireframeRenderer, WireframeObject

# 宇宙船の部品作成関数
def create_starship_hull():
    """宇宙船の船体を作成"""
    vertices = [
        # 前部（鋭利な先端）
        [0, 0, 4],      # 0: 先端
        [-0.5, -0.2, 3], # 1: 前部左下
        [0.5, -0.2, 3],  # 2: 前部右下
        [-0.5, 0.2, 3],  # 3: 前部左上
        [0.5, 0.2, 3],   # 4: 前部右上
        
        # 中央部
        [-1, -0.3, 1],   # 5: 中央左下
        [1, -0.3, 1],    # 6: 中央右下
        [-1, 0.3, 1],    # 7: 中央左上
        [1, 0.3, 1],     # 8: 中央右上
        
        # 後部
        [-0.8, -0.2, -1], # 9: 後部左下
        [0.8, -0.2, -1],  # 10: 後部右下
        [-0.8, 0.2, -1],  # 11: 後部左上
        [0.8, 0.2, -1],   # 12: 後部右上
    ]
    
    edges = [
        # 前部から中央部への接続
        [0, 1], [0, 2], [0, 3], [0, 4],
        [1, 2], [2, 4], [4, 3], [3, 1],
        [1, 5], [2, 6], [3, 7], [4, 8],
        
        # 中央部の輪郭
        [5, 6], [6, 8], [8, 7], [7, 5],
        [5, 9], [6, 10], [7, 11], [8, 12],
        
        # 後部の輪郭
        [9, 10], [10, 12], [12, 11], [11, 9],
    ]
    
    return WireframeObject(vertices, edges, "#00ffff")

def create_fuel_tank():
    """燃料タンクを作成"""
    vertices = [
        # タンク前部（円形断面）
        [-0.4, -0.4, 2],   # 0: 前部左下
        [0.4, -0.4, 2],    # 1: 前部右下
        [0.4, 0.4, 2],     # 2: 前部右上
        [-0.4, 0.4, 2],    # 3: 前部左上
        
        # タンク中央部（最大径）
        [-0.6, -0.6, 0],   # 4: 中央左下
        [0.6, -0.6, 0],    # 5: 中央右下
        [0.6, 0.6, 0],     # 6: 中央右上
        [-0.6, 0.6, 0],    # 7: 中央左上
        
        # タンク後部
        [-0.4, -0.4, -2],  # 8: 後部左下
        [0.4, -0.4, -2],   # 9: 後部右下
        [0.4, 0.4, -2],    # 10: 後部右上
        [-0.4, 0.4, -2],   # 11: 後部左上
        
        # 接続パイプ
        [-0.1, 0, 1],      # 12: パイプ前
        [-0.1, 0, -1],     # 13: パイプ後
    ]
    
    edges = [
        # 前部断面
        [0, 1], [1, 2], [2, 3], [3, 0],
        # 中央断面
        [4, 5], [5, 6], [6, 7], [7, 4],
        # 後部断面
        [8, 9], [9, 10], [10, 11], [11, 8],
        # 縦の接続線
        [0, 4], [1, 5], [2, 6], [3, 7],
        [4, 8], [5, 9], [6, 10], [7, 11],
        # 接続パイプ
        [12, 13], [12, 2], [13, 10],
    ]
    
    return WireframeObject(vertices, edges, "#ffff00")

def create_warp_nacelle():
    """ワープナセル（推進ユニット）を作成"""
    vertices = [
        # ナセル前部
        [-0.3, -0.2, 3],   # 0: 前部左下
        [0.3, -0.2, 3],    # 1: 前部右下
        [0.3, 0.2, 3],     # 2: 前部右上
        [-0.3, 0.2, 3],    # 3: 前部左上
        
        # ナセル中央部
        [-0.5, -0.3, 1],   # 4: 中央左下
        [0.5, -0.3, 1],    # 5: 中央右下
        [0.5, 0.3, 1],     # 6: 中央右上
        [-0.5, 0.3, 1],    # 7: 中央左上
        
        [-0.5, -0.3, -1],  # 8: 中央後左下
        [0.5, -0.3, -1],   # 9: 中央後右下
        [0.5, 0.3, -1],    # 10: 中央後右上
        [-0.5, 0.3, -1],   # 11: 中央後左上
        
        # ナセル後部
        [-0.3, -0.2, -3],  # 12: 後部左下
        [0.3, -0.2, -3],   # 13: 後部右下
        [0.3, 0.2, -3],    # 14: 後部右上
        [-0.3, 0.2, -3],   # 15: 後部左上
        
        # ワープコイル（内部構造）
        [-0.2, -0.1, 0.5], # 16: コイル1
        [0.2, -0.1, 0.5],  # 17
        [0.2, 0.1, 0.5],   # 18
        [-0.2, 0.1, 0.5],  # 19
        [-0.2, -0.1, -0.5], # 20: コイル2
        [0.2, -0.1, -0.5],  # 21
        [0.2, 0.1, -0.5],   # 22
        [-0.2, 0.1, -0.5],  # 23
    ]
    
    edges = [
        # 外殻の輪郭線
        [0, 1], [1, 2], [2, 3], [3, 0],  # 前部
        [4, 5], [5, 6], [6, 7], [7, 4],  # 中央前
        [8, 9], [9, 10], [10, 11], [11, 8],  # 中央後
        [12, 13], [13, 14], [14, 15], [15, 12],  # 後部
        
        # 縦の接続線
        [0, 4], [1, 5], [2, 6], [3, 7],
        [4, 8], [5, 9], [6, 10], [7, 11],
        [8, 12], [9, 13], [10, 14], [11, 15],
        
        # ワープコイル
        [16, 17], [17, 18], [18, 19], [19, 16],  # コイル1
        [20, 21], [21, 22], [22, 23], [23, 20],  # コイル2
        [16, 20], [17, 21], [18, 22], [19, 23],  # コイル間接続
    ]
    
    return WireframeObject(vertices, edges, "#00ffff")

def create_starship_engine():
    """宇宙船のエンジンを作成"""
    vertices = [
        # エンジン本体（円筒形）
        [-0.3, -0.3, -1.5], # 0: 前面左下
        [0.3, -0.3, -1.5],  # 1: 前面右下
        [0.3, 0.3, -1.5],   # 2: 前面右上
        [-0.3, 0.3, -1.5],  # 3: 前面左上
        
        [-0.4, -0.4, -3],   # 4: 後面左下
        [0.4, -0.4, -3],    # 5: 後面右下
        [0.4, 0.4, -3],     # 6: 後面右上
        [-0.4, 0.4, -3],    # 7: 後面左上
        
        # エンジンノズル
        [-0.2, -0.2, -3.5], # 8: ノズル左下
        [0.2, -0.2, -3.5],  # 9: ノズル右下
        [0.2, 0.2, -3.5],   # 10: ノズル右上
        [-0.2, 0.2, -3.5],  # 11: ノズル左上
    ]
    
    edges = [
        # 前面
        [0, 1], [1, 2], [2, 3], [3, 0],
        # 後面
        [4, 5], [5, 6], [6, 7], [7, 4],
        # 前面と後面の接続
        [0, 4], [1, 5], [2, 6], [3, 7],
        # ノズル
        [8, 9], [9, 10], [10, 11], [11, 8],
        [4, 8], [5, 9], [6, 10], [7, 11],
    ]
    
    return WireframeObject(vertices, edges, "#ff0000")

def create_engine_flame():
    """エンジンの炎エフェクト（グラデーション透明バー）を作成"""
    vertices = []
    edges = []
    
    # バーを複数のセグメントに分割して透明度グラデーションを作成
    segments = 8
    start_z = -3.5
    end_z = -5.5
    width_start = 0.1
    width_end = 0.05
    
    for i in range(segments + 1):
        progress = i / segments
        z = start_z + (end_z - start_z) * progress
        width = width_start + (width_end - width_start) * progress
        
        # 各セグメントの四角形頂点
        base_idx = i * 4
        vertices.extend([
            [-width, -width, z],  # 左下
            [width, -width, z],   # 右下
            [width, width, z],    # 右上
            [-width, width, z],   # 左上
        ])
        
        # セグメント内のエッジ
        if i < segments:  # 最後のセグメント以外
            # 現在のセグメントの四角形
            edges.extend([
                [base_idx, base_idx + 1],     # 下辺
                [base_idx + 1, base_idx + 2], # 右辺
                [base_idx + 2, base_idx + 3], # 上辺
                [base_idx + 3, base_idx],     # 左辺
            ])
            
            # 次のセグメントとの接続
            next_base = (i + 1) * 4
            edges.extend([
                [base_idx, next_base],         # 左下接続
                [base_idx + 1, next_base + 1], # 右下接続
                [base_idx + 2, next_base + 2], # 右上接続
                [base_idx + 3, next_base + 3], # 左上接続
            ])
    
    # 最後のセグメントの四角形
    last_base = segments * 4
    edges.extend([
        [last_base, last_base + 1],
        [last_base + 1, last_base + 2],
        [last_base + 2, last_base + 3],
        [last_base + 3, last_base],
    ])
    
    flame = WireframeObject(vertices, edges, "#ff0000")
    flame.is_flame = True  # フラグを追加
    return flame

def create_star_field():
    """星空を作成"""
    vertices = []
    edges = []
    
    # ランダムな星を配置
    np.random.seed(42)  # 再現性のため
    for i in range(100):
        x = np.random.uniform(-20, 20)
        y = np.random.uniform(-20, 20)
        z = np.random.uniform(-50, 50)
        vertices.append([x, y, z])
    
    # 星は単一の点として表示（自己ループエッジ）
    for i in range(len(vertices)):
        edges.append([i, i])
    
    return WireframeObject(vertices, edges, "#ffffff")

# 宇宙船アニメーションデモ
class StarshipDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Starship Animation - 3D Wireframe")
        self.root.geometry("1200x900")
        self.root.configure(bg='black')
        
        # Canvas
        self.canvas = Canvas(self.root, width=1200, height=900, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # レンダラー
        self.renderer = WireframeRenderer(self.canvas, 1200, 900)
        
        # カメラ設定
        self.camera = Camera([0, 5, 10], [0, 0, 0], [0, 1, 0], aspect=1200/900)
        self.renderer.set_camera(self.camera)
        
        # 宇宙船の部品
        self.starship_parts = []
        
        # オブジェクト追加
        self.setup_scene()
        
        # アニメーション変数
        self.time = 0
        self.ship_rotation = 0
        self.animate()
    
    def setup_scene(self):
        """シーンセットアップ"""
        # 星空
        stars = create_star_field()
        self.renderer.add_object(stars)
        
        # 宇宙船の船体
        hull = create_starship_hull()
        self.renderer.add_object(hull)
        self.starship_parts.append(hull)
        
        # 左燃料タンク
        left_tank = create_fuel_tank()
        left_tank.translate(-2.5, 0, 0)
        self.renderer.add_object(left_tank)
        self.starship_parts.append(left_tank)
        
        # 右燃料タンク
        right_tank = create_fuel_tank()
        right_tank.translate(2.5, 0, 0)
        self.renderer.add_object(right_tank)
        self.starship_parts.append(right_tank)
        
        # 左ワープナセル
        left_nacelle = create_warp_nacelle()
        left_nacelle.translate(-3.5, -1, 0)
        self.renderer.add_object(left_nacelle)
        self.starship_parts.append(left_nacelle)
        
        # 右ワープナセル
        right_nacelle = create_warp_nacelle()
        right_nacelle.translate(3.5, -1, 0)
        self.renderer.add_object(right_nacelle)
        self.starship_parts.append(right_nacelle)
        
        # メインエンジン
        main_engine = create_starship_engine()
        main_engine.translate(0, -0.5, 0)
        main_engine.scale(1.5, 1.5, 1.5)  # 少し大きく
        self.renderer.add_object(main_engine)
        self.starship_parts.append(main_engine)
        
        # メインエンジンの炎
        main_flame = create_engine_flame()
        main_flame.translate(0, -0.5, 0)
        main_flame.scale(1.5, 1.5, 1.8)
        self.renderer.add_object(main_flame)
        self.starship_parts.append(main_flame)
        
        # ワープナセルのエネルギー効果（左）
        left_warp_effect = create_engine_flame()
        left_warp_effect.translate(-3.5, -1, 0)
        left_warp_effect.scale(0.8, 0.8, 2)
        left_warp_effect.color = "#00ffff"  # シアン色
        self.renderer.add_object(left_warp_effect)
        self.starship_parts.append(left_warp_effect)
        
        # ワープナセルのエネルギー効果（右）
        right_warp_effect = create_engine_flame()
        right_warp_effect.translate(3.5, -1, 0)
        right_warp_effect.scale(0.8, 0.8, 2)
        right_warp_effect.color = "#00ffff"  # シアン色
        self.renderer.add_object(right_warp_effect)
        self.starship_parts.append(right_warp_effect)
    
    def animate(self):
        """アニメーション"""
        self.time += 0.03
        
        # カメラの動き（宇宙船の周りを回る）
        camera_distance = 15
        camera_angle = self.time * 0.3
        self.camera.position[0] = camera_distance * math.cos(camera_angle)
        self.camera.position[1] = 3 + 2 * math.sin(self.time * 0.5)
        self.camera.position[2] = camera_distance * math.sin(camera_angle)
        self.camera.target = [0, 0, 0]
        self.camera.update()
        
        # 宇宙船の回転とバンク
        ship_bank = math.sin(self.time * 0.7) * 0.3
        ship_pitch = math.sin(self.time * 0.5) * 0.2
        ship_yaw = self.time * 0.1
        
        # 宇宙船の各部品を更新
        for i, part in enumerate(self.starship_parts):
            part.transform_matrix = Matrix3D.identity()
            
            # 船体の場合
            if i == 0:  # hull
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            
            # 燃料タンクの場合
            elif i == 1:  # left fuel tank
                part.translate(-2.5, 0, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            elif i == 2:  # right fuel tank
                part.translate(2.5, 0, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            
            # ワープナセルの場合（わずかな振動効果）
            elif i == 3:  # left warp nacelle
                nacelle_vibration = 0.02 * math.sin(self.time * 15)
                part.translate(-3.5, -1 + nacelle_vibration, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            elif i == 4:  # right warp nacelle
                nacelle_vibration = 0.02 * math.sin(self.time * 15 + math.pi/3)
                part.translate(3.5, -1 + nacelle_vibration, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            
            # メインエンジンの場合
            elif i == 5:  # main engine
                part.scale(1.5, 1.5, 1.5)
                part.translate(0, -0.5, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            
            # メインエンジンの炎の場合（静的、アニメーションなし）
            elif i == 6:  # main flame
                part.scale(1.5, 1.5, 1.8)
                part.translate(0, -0.5, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            
            # ワープエフェクトの場合（静的、アニメーションなし）
            elif i == 7:  # left warp effect
                part.scale(0.8, 0.8, 2)
                part.translate(-3.5, -1, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
            elif i == 8:  # right warp effect
                part.scale(0.8, 0.8, 2)
                part.translate(3.5, -1, 0)
                part.rotate(ship_pitch, ship_yaw, ship_bank)
        
        # 星空の回転
        if len(self.renderer.objects) > 0:
            stars = self.renderer.objects[0]
            stars.transform_matrix = Matrix3D.identity()
            stars.rotate(0, self.time * 0.05, 0)
        
        # レンダリング
        self.renderer.render()
        
        # 次のフレーム
        self.root.after(16, self.animate)  # 約60FPS
    
    def run(self):
        self.root.mainloop()

# 実行
if __name__ == "__main__":
    demo = StarshipDemo()
    demo.run()
