"""
链接卡片生成器 - 使用 pywinstyles 实现 Windows 11 现代化风格
Author: 0liuuil0
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import re

# 尝试导入 pywinstyles，如果未安装则提示用户
try:
    import pywinstyles
    HAS_PYWINSTYLES = True
except ImportError:
    HAS_PYWINSTYLES = False
    print("提示: 未安装 pywinstyles，将使用普通样式。")
    print("安装命令: pip install pywinstyles")


class LinkCardGenerator:
    """链接卡片生成器的主类"""
    
    def __init__(self, root):
        """初始化方法：程序启动时执行，负责搭建界面"""
        
        self.root = root
        self.root.title("链接代码生成器 By 0liuuil0")
        self.root.geometry("650x850")
        
        # 设置窗口背景色（深色主题更配 pywinstyles）
        self.bg_color = "#202020"
        self.card_bg = "#2d2d2d"
        self.text_color = "#e0e0e0"
        self.hint_color = "#888888"
        self.accent_color = "#0078d4"
        
        self.root.configure(bg=self.bg_color)
        
        # --- 应用 pywinstyles 现代化样式 ---
        if HAS_PYWINSTYLES:
            try:
                # 应用暗色主题 + Mica 效果（Windows 11 风格）
                pywinstyles.apply_style(self.root, style="acrylic")
                # 可选的其他样式:
                # style="mica" - Windows 11 Mica 效果
                # style="acrylic" - 亚克力模糊效果
                # style="dark" - 深色主题
                # style="light" - 浅色主题
            except Exception as e:
                print(f"应用样式失败: {e}")
        
        # --- 主容器 ---
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # --- 标题区域 ---
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            title_frame, 
            text="🔗 链接卡片生成器", 
            font=("Microsoft YaHei", 18, "bold"),
            bg=self.bg_color, 
            fg=self.text_color
        )
        title_label.pack(anchor=tk.W)
        
        # 副标题
        subtitle_label = tk.Label(
            title_frame,
            text="快速生成精美的链接卡片 HTML 代码",
            font=("Microsoft YaHei", 9),
            bg=self.bg_color,
            fg=self.hint_color
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        # --- 输入区域 ---
        input_frame = tk.Frame(main_frame, bg=self.card_bg, padx=15, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
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
                input_frame, 
                text=label_text, 
                font=("Microsoft YaHei", 10),
                bg=self.card_bg, 
                fg=self.text_color, 
                anchor=tk.W
            )
            lbl.pack(fill=tk.X, pady=(10, 0))
            
            # 输入框 - 现代化样式
            entry = tk.Entry(
                input_frame, 
                font=("Microsoft YaHei", 10),
                bg="#3d3d3d",
                fg=self.text_color,
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground="#4a4a4a",
                highlightcolor=self.accent_color,
                insertbackground=self.text_color  # 光标颜色
            )
            entry.pack(fill=tk.X, pady=(3, 0), ipady=8)
            
            self.entries[key] = entry
            
            # 提示文字
            hint_lbl = tk.Label(
                input_frame, 
                text=hint, 
                font=("Microsoft YaHei", 8),
                bg=self.card_bg, 
                fg=self.hint_color, 
                anchor=tk.W
            )
            hint_lbl.pack(fill=tk.X)
        
        # --- 按钮区域 ---
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(5, 10))
        
        # 生成代码按钮
        gen_btn = tk.Button(
            btn_frame, 
            text="✨ 生成代码",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.accent_color, 
            fg="white",
            relief=tk.FLAT,
            activebackground="#005a9e",
            activeforeground="white",
            cursor="hand2",
            command=self.generate_code
        )
        gen_btn.pack(side=tk.LEFT, ipadx=25, ipady=8)
        
        # 清空按钮
        clear_btn = tk.Button(
            btn_frame, 
            text="🗑️ 清空",
            font=("Microsoft YaHei", 10),
            bg="#3d3d3d",
            fg=self.text_color,
            relief=tk.FLAT,
            activebackground="#4d4d4d",
            activeforeground=self.text_color,
            cursor="hand2",
            command=self.clear_inputs
        )
        clear_btn.pack(side=tk.LEFT, padx=10, ipadx=15, ipady=8)
        
        # --- 输出区域标题 ---
        output_header = tk.Frame(main_frame, bg=self.bg_color)
        output_header.pack(fill=tk.X, pady=(5, 8))
        
        # 复制按钮放在右侧
        copy_btn = tk.Button(
            output_header, 
            text="📋 一键复制",
            font=("Microsoft YaHei", 9),
            bg="#28a745",
            fg="white",
            relief=tk.FLAT,
            activebackground="#218838",
            activeforeground="white",
            cursor="hand2",
            command=self.copy_code
        )
        copy_btn.pack(side=tk.RIGHT, ipadx=20, ipady=6)
        
        # 输出标签
        out_title = tk.Label(
            output_header, 
            text="📝 生成的代码",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color, 
            fg=self.text_color
        )
        out_title.pack(side=tk.LEFT)
        
        # --- 代码显示框 ---
        self.output_text = scrolledtext.ScrolledText(
            main_frame, 
            height=12,
            font=("Consolas", 10),
            bg="#1a1a1a",
            fg="#d4d4d4",
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#3d3d3d",
            selectbackground=self.accent_color
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # --- 绑定快捷键 ---
        self.root.bind('<Return>', lambda e: self.generate_code())
        self.root.bind('<Control-c>', lambda e: self.copy_code())
        
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
        
        # 表单验证
        if not url or not name or not desc:
            messagebox.showwarning("提示", "请填写必填项！")
            return
            
        # 处理默认值
        if not keyword:
            keyword = name
        if not favicon_domain:
            favicon_domain = self.extract_domain(url)
            
        # 生成 HTML 代码
        code = (
            '                    <a href="' + url + '" target="_blank" class="link-card" data-name="' + keyword + '">\n'
            '                        <img src="https://favicon.im/' + favicon_domain + '" alt="' + favicon_domain + ' favicon" loading="lazy" style="width: 32px; height: 32px; object-fit: cover;"/>\n'
            '                        <div class="link-info">\n'
            '                            <span class="link-name">' + name + '</span>\n'
            '                            <span class="link-desc">' + desc + '</span>\n'
            '                        </div>\n'
            '                    </a>'
        )
        
        # 显示结果
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
