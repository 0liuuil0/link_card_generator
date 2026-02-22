"""
链接卡片生成器 - 使用 pywinstyles 实现 Windows 11 现代化风格
Author: 0liuuil0
"""

import tkinter as tk
from tkinter import messagebox
import re
import os

# 尝试导入 pywinstyles，如果未安装则提示用户
try:
    import pywinstyles
    HAS_PYWINSTYLES = True
except ImportError:
    HAS_PYWINSTYLES = False
    print("提示: 未安装 pywinstyles，将使用普通样式。")
    print("安装命令: pip install pywinstyles")


class RoundedButton(tk.Canvas):
    """圆角按钮组件"""
    
    def __init__(self, parent, text, command=None, bg="#0078d4", fg="white",
                 font=("Microsoft YaHei", 10), width=120, height=36, radius=8, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent.cget('bg'), **kwargs)
        
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.text = text
        self.font = font
        self.radius = radius
        self.width = width
        self.height = height
        self.hover_color = self._darken_color(bg, 0.15)
        self.current_bg = bg
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
        self._draw_button()
    
    def _darken_color(self, hex_color, factor):
        """将颜色变暗"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _draw_button(self):
        """绘制圆角矩形按钮"""
        self.delete("all")
        
        # 绘制圆角矩形
        x1, y1 = 2, 2
        x2, y2 = self.width - 2, self.height - 2
        r = self.radius
        
        # 使用多边形绘制圆角矩形
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        
        self.create_polygon(points, fill=self.current_bg, smooth=True, tags="button")
        
        # 绘制文字
        self.create_text(self.width // 2, self.height // 2, 
                        text=self.text, fill=self.fg_color, 
                        font=self.font, tags="text")
    
    def _on_enter(self, event):
        """鼠标进入"""
        self.current_bg = self.hover_color
        self.config(cursor="hand2")
        self._draw_button()
    
    def _on_leave(self, event):
        """鼠标离开"""
        self.current_bg = self.bg_color
        self._draw_button()
    
    def _on_click(self, event):
        """点击事件"""
        if self.command:
            self.command()


class RoundedFrame(tk.Canvas):
    """圆角框架组件"""
    
    def __init__(self, parent, bg="white", radius=10, border_color=None, border_width=1, **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent.cget('bg'), **kwargs)
        
        self.frame_bg = bg
        self.radius = radius
        self.border_color = border_color
        self.border_width = border_width
        
        # 内部 Frame 用于放置其他控件
        self.inner_frame = tk.Frame(self, bg=bg)
        
        self._draw_frame()
    
    def _draw_frame(self):
        """绘制圆角框架"""
        self.delete("all")
        
        w = self.winfo_width() or 300
        h = self.winfo_height() or 200
        
        x1, y1 = 0, 0
        x2, y2 = w, h
        r = self.radius
        
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        
        # 绘制边框（如果有）
        if self.border_color:
            self.create_polygon(points, fill=self.border_color, smooth=True, tags="border")
            # 内部缩小绘制背景
            bw = self.border_width
            inner_points = [
                x1 + r + bw, y1 + bw,
                x2 - r - bw, y1 + bw,
                x2 - bw, y1 + bw,
                x2 - bw, y1 + r + bw,
                x2 - bw, y2 - r - bw,
                x2 - bw, y2 - bw,
                x2 - r - bw, y2 - bw,
                x1 + r + bw, y2 - bw,
                x1 + bw, y2 - bw,
                x1 + bw, y2 - r - bw,
                x1 + bw, y1 + r + bw,
                x1 + bw, y1 + bw,
            ]
            self.create_polygon(inner_points, fill=self.frame_bg, smooth=True, tags="bg")
        else:
            self.create_polygon(points, fill=self.frame_bg, smooth=True, tags="bg")


class LinkCardGenerator:
    """链接卡片生成器的主类"""
    
    def __init__(self, root):
        """初始化方法：程序启动时执行，负责搭建界面"""
        
        self.root = root
        self.root.title("链接代码生成器 By 0liuuil0")
        self.root.geometry("900x550")
        
        # 浅色主题配色
        self.bg_color = "#f0f2f5"
        self.card_bg = "#ffffff"
        self.text_color = "#333333"
        self.hint_color = "#888888"
        self.accent_color = "#0078d4"
        self.border_color = "#e0e0e0"
        self.code_bg = "#f6f8fa"
        self.code_text = "#24292e"
        
        self.root.configure(bg=self.bg_color)
        
        # --- 设置窗口图标 ---
        self._set_window_icon()
        
        # --- 应用 pywinstyles 现代化样式 ---
        if HAS_PYWINSTYLES:
            try:
                pywinstyles.apply_style(self.root, style="light")
            except Exception as e:
                print(f"应用样式失败: {e}")
        
        # --- 主容器 ---
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 配置网格
        main_frame.columnconfigure(0, weight=1, minsize=400)
        main_frame.columnconfigure(1, weight=1, minsize=400)
        main_frame.rowconfigure(0, weight=1)
        
        # ========== 左侧：输入区域 ==========
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # 标题
        title_label = tk.Label(
            left_frame,
            text="🔗 链接卡片生成器",
            font=("Microsoft YaHei", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(anchor=tk.W, pady=(0, 12))
        
        # 输入卡片容器
        self.input_container = tk.Frame(left_frame, bg=self.bg_color)
        self.input_container.pack(fill=tk.BOTH, expand=True)
        
        # 使用Canvas绘制圆角背景
        self.input_canvas = tk.Canvas(self.input_container, bg=self.bg_color, 
                                      highlightthickness=0, height=350)
        self.input_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 内部Frame
        self.input_frame = tk.Frame(self.input_canvas, bg=self.card_bg)
        
        # 字段配置
        fields = [
            ("网址 *", "url", "例如: https://www.baidu.com"),
            ("网站名称 *", "name", "例如: 百度"),
            ("网站描述 *", "desc", "例如: 全球最大的中文搜索引擎"),
            ("搜索关键词", "keyword", "留空则自动使用网站名称"),
            ("Favicon域名", "favicon_domain", "留空则自动从网址提取")
        ]
        
        self.entries = {}
        
        for label_text, key, hint in fields:
            # 标签
            lbl = tk.Label(
                self.input_frame,
                text=label_text,
                font=("Microsoft YaHei", 10),
                bg=self.card_bg,
                fg=self.text_color,
                anchor=tk.W
            )
            lbl.pack(fill=tk.X, pady=(10, 0))
            
            # 输入框
            entry = tk.Entry(
                self.input_frame,
                font=("Microsoft YaHei", 10),
                bg="#f8f9fa",
                fg=self.text_color,
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground=self.border_color,
                highlightcolor=self.accent_color,
                insertbackground=self.text_color
            )
            entry.pack(fill=tk.X, pady=(3, 0), ipady=6)
            
            self.entries[key] = entry
            
            # 提示文字
            hint_lbl = tk.Label(
                self.input_frame,
                text=hint,
                font=("Microsoft YaHei", 8),
                bg=self.card_bg,
                fg=self.hint_color,
                anchor=tk.W
            )
            hint_lbl.pack(fill=tk.X)
        
        # 延迟绘制圆角和放置内部Frame
        self.root.after(50, self._setup_input_frame)
        
        # ========== 右侧：代码预览区域 ==========
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # 预览标题
        preview_title = tk.Label(
            right_frame,
            text="📝 代码预览",
            font=("Microsoft YaHei", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        preview_title.pack(anchor=tk.W, pady=(0, 12))
        
        # 代码显示框容器（使用Canvas实现圆角）
        self.code_container = tk.Frame(right_frame, bg=self.bg_color)
        self.code_container.pack(fill=tk.BOTH, expand=True)
        
        self.code_canvas = tk.Canvas(self.code_container, bg=self.bg_color, 
                                     highlightthickness=0)
        self.code_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 代码显示框
        self.output_text = tk.Text(
            self.code_canvas,
            font=("Consolas", 10),
            bg=self.code_bg,
            fg=self.code_text,
            insertbackground=self.code_text,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.accent_color,
            selectforeground="white",
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        
        # 延迟设置代码框
        self.root.after(50, self._setup_code_frame)
        
        # ========== 底部按钮区域 ==========
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        btn_container = tk.Frame(btn_frame, bg=self.bg_color)
        btn_container.pack(anchor=tk.CENTER)
        
        # 生成代码按钮
        self.gen_btn = RoundedButton(
            btn_container,
            text="✨ 生成代码",
            command=self.generate_code,
            bg=self.accent_color,
            fg="white",
            font=("Microsoft YaHei", 10, "bold"),
            width=130,
            height=38,
            radius=8
        )
        self.gen_btn.pack(side=tk.LEFT, padx=8)
        
        # 一键复制按钮
        self.copy_btn = RoundedButton(
            btn_container,
            text="📋 一键复制",
            command=self.copy_code,
            bg="#28a745",
            fg="white",
            font=("Microsoft YaHei", 10),
            width=130,
            height=38,
            radius=8
        )
        self.copy_btn.pack(side=tk.LEFT, padx=8)
        
        # 清空按钮
        self.clear_btn = RoundedButton(
            btn_container,
            text="🗑️ 清空",
            command=self.clear_inputs,
            bg="#6c757d",
            fg="white",
            font=("Microsoft YaHei", 10),
            width=130,
            height=38,
            radius=8
        )
        self.clear_btn.pack(side=tk.LEFT, padx=8)
        
        # --- 绑定快捷键 ---
        self.root.bind('<Return>', lambda e: self.generate_code())
        self.root.bind('<Control-c>', lambda e: self.copy_code())
    
    def _setup_input_frame(self):
        """设置输入框区域的圆角背景"""
        self.input_canvas.delete("all")
        
        w = self.input_canvas.winfo_width()
        h = self.input_canvas.winfo_height()
        
        if w < 10 or h < 10:
            self.root.after(50, self._setup_input_frame)
            return
        
        # 绘制圆角矩形背景
        r = 10
        points = [
            r, 0, w - r, 0, w, 0, w, r,
            w, h - r, w, h, w - r, h,
            r, h, 0, h, 0, h - r,
            0, r, 0, 0, r, 0
        ]
        self.input_canvas.create_polygon(points, fill=self.card_bg, smooth=True, tags="bg")
        
        # 绘制边框
        self.input_canvas.create_polygon(points, outline=self.border_color, 
                                        width=1, fill='', smooth=True, tags="border")
        
        # 放置内部Frame
        self.input_window = self.input_canvas.create_window(15, 15, 
                                                            window=self.input_frame, 
                                                            anchor=tk.NW)
        self.input_frame.update_idletasks()
        
    def _setup_code_frame(self):
        """设置代码框区域的圆角背景"""
        self.code_canvas.delete("all")
        
        w = self.code_canvas.winfo_width()
        h = self.code_canvas.winfo_height()
        
        if w < 10 or h < 10:
            self.root.after(50, self._setup_code_frame)
            return
        
        # 绘制圆角矩形背景
        r = 10
        points = [
            r, 0, w - r, 0, w, 0, w, r,
            w, h - r, w, h, w - r, h,
            r, h, 0, h, 0, h - r,
            0, r, 0, 0, r, 0
        ]
        self.code_canvas.create_polygon(points, fill=self.code_bg, smooth=True, tags="bg")
        
        # 绘制边框
        self.code_canvas.create_polygon(points, outline=self.border_color, 
                                        width=1, fill='', smooth=True, tags="border")
        
        # 放置Text组件
        self.code_window = self.code_canvas.create_window(8, 8, 
                                                          window=self.output_text, 
                                                          anchor=tk.NW)
        self.output_text.update_idletasks()
        
    def _set_window_icon(self):
        """设置窗口图标"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "ah9v5-zy2rl.png")
        
        if os.path.exists(icon_path):
            try:
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
                self.root._icon_image = icon_image
            except Exception as e:
                print(f"加载图标失败: {e}")
        else:
            print(f"图标文件不存在: {icon_path}")
        
    def extract_domain(self, url):
        """从URL中提取域名"""
        try:
            domain = re.sub(r'^https?://', '', url)
            domain = domain.split('/')[0]
            return domain
        except:
            return url

    def generate_code(self):
        """生成代码的核心逻辑"""
        url = self.entries['url'].get().strip()
        name = self.entries['name'].get().strip()
        desc = self.entries['desc'].get().strip()
        keyword = self.entries['keyword'].get().strip()
        favicon_domain = self.entries['favicon_domain'].get().strip()
        
        if not url or not name or not desc:
            messagebox.showwarning("提示", "请填写必填项！")
            return
            
        if not keyword:
            keyword = name
        if not favicon_domain:
            favicon_domain = self.extract_domain(url)
            
        code = (
            '                    <a href="' + url + '" target="_blank" class="link-card" data-name="' + keyword + '">\n'
            '                        <img src="https://favicon.im/' + favicon_domain + '" alt="' + favicon_domain + ' favicon" loading="lazy" style="width: 32px; height: 32px; object-fit: cover;"/>\n'
            '                        <div class="link-info">\n'
            '                            <span class="link-name">' + name + '</span>\n'
            '                            <span class="link-desc">' + desc + '</span>\n'
            '                        </div>\n'
            '                    </a>'
        )
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, code)
        print("✅ 代码已生成")

    def copy_code(self):
        """复制代码到剪贴板"""
        code = self.output_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showinfo("提示", "没有可复制的内容！")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.root.update()
        
        print("✅ 已复制到剪贴板！")
        messagebox.showinfo("成功", "代码已复制到剪贴板！")

    def clear_inputs(self):
        """清空所有输入框"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        print("已清空所有输入")


# --- 程序入口 ---
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LinkCardGenerator(root)
        root.mainloop()
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按回车键退出...")
