import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import webbrowser

class FileCryptoApp:
    def __init__(self, master):
        self.master = master
        master.title("文件加密解密工具 v3.0")
        
        # 主界面布局
        main_frame = tk.Frame(master)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 日志文本框
        self.log_text = tk.Text(main_frame, state='disabled', width=60, height=25)
        self.log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 右侧按钮区域
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        ttk.Button(right_frame, text="选择文件", command=self.select_file).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="输出目录", command=self.select_output).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="开始加密", command=self.start_encrypt).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="开始解密", command=self.start_decrypt).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="关于", command=self.show_about).pack(fill='x', pady=5)
        
        # 底部版权信息
        copyright_frame = tk.Frame(master)
        copyright_frame.pack(fill='x', side='bottom', pady=5)
        
        # 底部左侧添加两个链接按钮
        link_frame = tk.Frame(copyright_frame)
        link_frame.pack(side='left', padx=10)
        
        bilibili_btn = ttk.Button(link_frame, text="作者B站主页", 
                                command=lambda: webbrowser.open("https://space.bilibili.com/3461564273265329"))
        bilibili_btn.pack(side='left', padx=5)
        
        website_btn = ttk.Button(link_frame, text="作者官网", 
                               command=lambda: webbrowser.open("https://wenyuxiangxiang1221.wordpress.com"))
        website_btn.pack(side='left', padx=5)
        
        # 底部右侧版权信息
        tk.Label(copyright_frame, text="© 2025 文宇香香工作室", fg="gray").pack(side='right', padx=10)
        
        # 文件扩展名配置
        self.ENCRYPT_EXT = ".lock"
        self.EXT_LENGTH = len(self.ENCRYPT_EXT)
        
        # 加密配置
        self.SECRET_KEY = 0x6D  # 109 in decimal
        self.file_path = ""
        self.output_dir = ""

    def show_about(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("关于")
        about_window.geometry("300x200")
        
        about_text = """文件加密解密工具 v3.0

作者B站主页:
space.bilibili.com/3461564273265329

作者官网:
wenyuxiangxiang1221.wordpress.com

作者：文宇香香
由文宇香香工作室代为出品

         © 2025 文宇香香工作室
"""
        tk.Label(about_window, text=about_text, justify=tk.LEFT).pack(pady=20, padx=20)
        
        button_frame = tk.Frame(about_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="关闭", command=about_window.destroy).pack()

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.log(f"已选择文件: {os.path.basename(self.file_path)}")

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.log(f"输出目录: {self.output_dir}")

    def start_encrypt(self):
        if not self._validate_input():
            return
        try:
            output_path = self._get_output_path(encrypt=True)
            self._process_file(self.file_path, output_path, encrypt=True)
            self.log("加密成功！")
            messagebox.showinfo("完成", "文件加密完成！")
        except Exception as e:
            self.log(f"加密错误: {str(e)}")
            messagebox.showerror("错误", str(e))

    def start_decrypt(self):
        if not self._validate_input():
            return
        try:
            # 检查文件扩展名
            if not self.file_path.endswith(self.ENCRYPT_EXT):
                if not messagebox.askyesno("警告", "文件没有加密后缀，确定要解密吗？"):
                    return
                
            output_path = self._get_output_path(encrypt=False)
            self._process_file(self.file_path, output_path, encrypt=False)
            self.log("解密成功！")
            messagebox.showinfo("完成", "文件解密完成！")
        except Exception as e:
            self.log(f"解密错误: {str(e)}")
            messagebox.showerror("错误", str(e))

    def _validate_input(self):
        if not self.file_path:
            messagebox.showerror("错误", "请先选择文件")
            return False
        if not self.output_dir:
            messagebox.showerror("错误", "请先选择输出目录")
            return False
        return True

    def _get_output_path(self, encrypt=True):
        base_name = os.path.basename(self.file_path)
        if encrypt:
            return os.path.join(self.output_dir, f"{base_name}{self.ENCRYPT_EXT}")
        else:
            if base_name.endswith(self.ENCRYPT_EXT):
                return os.path.join(self.output_dir, base_name[:-self.EXT_LENGTH])
            return os.path.join(self.output_dir, f"decrypted_{base_name}")

    def _process_file(self, input_path, output_path, encrypt=True):
        block_size = 4096  # 4KB 块处理
        key = self.SECRET_KEY
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            position = 0
            while True:
                chunk = fin.read(block_size)
                if not chunk:
                    break
                
                processed = bytearray()
                for byte in chunk:
                    if encrypt:
                        # 加密算法：(XOR + 位移) 取模保证范围
                        encrypted = ((byte ^ key) + (position % 256)) % 256
                        processed.append(encrypted)
                    else:
                        # 解密算法：(先减位移再XOR) 双重取模保证范围
                        decrypted = (byte - (position % 256)) % 256
                        processed.append(decrypted ^ key)
                    position += 1
                
                fout.write(bytes(processed))
            self.log(f"已处理 {position} 字节")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCryptoApp(root)
    root.mainloop()
