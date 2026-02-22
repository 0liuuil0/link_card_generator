"""
链接卡片生成器 - 使用 pywinstyles 实现 Windows 11 现代化风格
Author: 0liuuil0
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
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
        self.border_color = "#dddddd"
        
        self.root.configure(bg=self.bg_color)
        
        # --- 设置窗口图标 ---
        self._set_window_icon()
        
        # --- 应用 pywinstyles 现代化样式 ---
        if HAS_PYWINSTYLES:
            try:
                pywinstyles.apply_style(self.root, style="light")
            except Exception as e:
                print(f"应用样式失败: {e}")
        
        # --- 主容器（左右两栏布局）---
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 配置网格列权重
        main_frame.columnconfigure(0, weight=1, minsize=380)
        main_frame.columnconfigure(1, weight=1, minsize=380)
        main_frame.rowconfigure(0, weight=1)
        
        # ========== 左侧：输入区域 ==========
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        # 标题
        title_label = tk.Label(
            left_frame,
            text="🔗 链接卡片生成器",
            font=("Microsoft YaHei", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(anchor=tk.W, pady=(0, 12))
        
        # 输入卡片
        input_frame = tk.Frame(left_frame, bg=self.card_bg, padx=12, pady=12)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
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
            lbl.pack(fill=tk.X, pady=(8, 0))
            
            # 输入框
            entry = tk.Entry(
                input_frame,
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
                input_frame,
                text=hint,
                font=("Microsoft YaHei", 8),
                bg=self.card_bg,
                fg=self.hint_color,
                anchor=tk.W
            )
            hint_lbl.pack(fill=tk.X)
        
        # ========== 右侧：代码预览区域 ==========
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        
        # 预览标题
        preview_title = tk.Label(
            right_frame,
            text="📝 代码预览",
            font=("Microsoft YaHei", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        preview_title.pack(anchor=tk.W, pady=(0, 12))
        
        # 代码显示框容器
        code_frame = tk.Frame(right_frame, bg="#1e1e1e", padx=2, pady=2)
        code_frame.pack(fill=tk.BOTH, expand=True)
        
        # 代码显示框
        self.output_text = scrolledtext.ScrolledText(
            code_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.accent_color,
            wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        


        # ========== 底部按钮区域 ==========
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        # 三个按钮放一排，居中
        btn_container = tk.Frame(btn_frame, bg=self.bg_color)
        btn_container.pack(anchor=tk.CENTER)
        
        # 生成代码按钮
        gen_btn = tk.Button(
            btn_container,
            text="✨ 生成代码",
            font=("Microsoft YaHei", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            relief=tk.FLAT,
            activebackground="#005a9e",
            activeforeground="white",
            cursor="hand2",
            command=self.generate_code
        )
        gen_btn.pack(side=tk.LEFT, ipadx=20, ipady=8)
        
        # 一键复制按钮
        copy_btn = tk.Button(
            btn_container,
            text="📋 一键复制",
            font=("Microsoft YaHei", 10),
            bg="#28a745",
            fg="white",
            relief=tk.FLAT,
            activebackground="#218838",
            activeforeground="white",
            cursor="hand2",
            command=self.copy_code
        )
        copy_btn.pack(side=tk.LEFT, padx=15, ipadx=20, ipady=8)
        
        # 清空按钮
        clear_btn = tk.Button(
            btn_container,
            text="🗑️ 清空",
            font=("Microsoft YaHei", 10),
            bg="#6c757d",
            fg="white",
            relief=tk.FLAT,
            activebackground="#5a6268",
            activeforeground="white",
            cursor="hand2",
            command=self.clear_inputs
        )
        clear_btn.pack(side=tk.LEFT, ipadx=20, ipady=8)
        
        # --- 绑定快捷键 ---
        self.root.bind('<Return>', lambda e: self.generate_code())
        self.root.bind('<Control-c>', lambda e: self.copy_code())
        
    def _set_window_icon(self):
        """设置窗口图标"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "ah9v5-zy2rl.png")
        
        if os.path.exists(icon_path):
            try:
                # 加载 PNG 图片作为图标
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
                # 保存引用防止被垃圾回收
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
