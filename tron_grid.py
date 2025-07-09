import tkinter as tk
from tkinter import Canvas
import math

class TronGrid:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("トロン風グリッド")
        self.root.geometry("1200x800")
        self.root.configure(bg='black')
        
        # Canvas設定
        self.canvas = Canvas(self.root, width=1200, height=800, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # グリッドの設定
        self.width = 1200
        self.height = 800
        self.horizon_y = 300  # 地平線の高さ
        self.vanishing_point_x = 600  # 消失点X座標
        self.vanishing_point_y = 300  # 消失点Y座標
        
        # アニメーション用
        self.grid_offset = 0
        self.animation_speed = 2
        
        self.draw_grid()
        self.animate()
        
    def draw_grid(self):
        self.canvas.delete("all")
        
        # 水平線（パースペクティブ効果付き）
        self.draw_horizontal_lines()
        
        # 縦線（消失点に向かう）
        self.draw_vertical_lines()
        
        # 地平線
        self.canvas.create_line(0, self.horizon_y, self.width, self.horizon_y, 
                               fill='#00ffff', width=1)
    
    def draw_horizontal_lines(self):
        # 手前から奥へ向かう水平線
        grid_spacing = 15
        for i in range(50):
            # 地平線から下に向かって線を描画
            y = self.horizon_y + i * grid_spacing + (self.grid_offset % grid_spacing)
            
            if y > self.height:  # 画面外は描画しない
                continue
            
            # パースペクティブ効果：奥ほど線が短くなる
            perspective_factor = (y - self.horizon_y) / (self.height - self.horizon_y)
            perspective_factor = max(0, min(1, perspective_factor))
            
            # 線の幅を計算（画面全体に広がる）
            line_width = self.width * (1 - perspective_factor * 0.8)
            
            # 線の位置
            x1 = self.vanishing_point_x - line_width // 2
            x2 = self.vanishing_point_x + line_width // 2
            
            # 色の強度（奥ほど薄く）
            intensity = 1 - perspective_factor * 0.8
            color = f"#{0:02x}{int(intensity*255):02x}{int(intensity*255):02x}"
            
            self.canvas.create_line(x1, y, x2, y, fill=color, width=1)
    
    def draw_vertical_lines(self):
        # 消失点に向かう縦線
        num_lines = 25
        for i in range(-num_lines, num_lines + 1):
            
            # 画面下部でのX座標
            bottom_x = self.vanishing_point_x + i * 25
            
            # 画面外に出る線はスキップ
            if bottom_x < 0 or bottom_x > self.width:
                continue
            
            # 線の色（中央から離れるほど薄く）
            distance_factor = abs(i) / num_lines
            intensity = 1 - distance_factor * 0.7
            color = f"#{0:02x}{int(intensity*255):02x}{int(intensity*255):02x}"
            
            self.canvas.create_line(bottom_x, self.height, 
                                   self.vanishing_point_x, self.vanishing_point_y,
                                   fill=color, width=1)
    
    def animate(self):
        # グリッドをアニメーション
        self.grid_offset += self.animation_speed
        self.draw_grid()
        
        # 次のフレームをスケジュール
        self.root.after(50, self.animate)  # 20FPS
    
    def run(self):
        self.root.mainloop()

# 実行
if __name__ == "__main__":
    game = TronGrid()
    game.run()