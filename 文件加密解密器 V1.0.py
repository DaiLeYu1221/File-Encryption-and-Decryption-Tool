import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class FileCryptoApp:
    def __init__(self, master):
        self.master = master
        master.title("文件加密解密工具 v1.0")
        
        # 界面布局
        self.log_text = tk.Text(master, state='disabled', width=60, height=25)
        self.log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        right_frame = tk.Frame(master)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        ttk.Button(right_frame, text="选择文件", command=self.select_file).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="输出目录", command=self.select_output).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="开始加密", command=self.start_encrypt).pack(fill='x', pady=5)
        ttk.Button(right_frame, text="开始解密", command=self.start_decrypt).pack(fill='x', pady=5)
        
        # 文件扩展名配置
        self.ENCRYPT_EXT = ".lock"  # 加密文件扩展名
        self.EXT_LENGTH = len(self.ENCRYPT_EXT)
        
        # 固定加密密钥
        self.SECRET_KEY = 0x6D
        self.file_path = ""
        self.output_dir = ""

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
        block_size = 4096
        key = self.SECRET_KEY
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            position = 0
            while True:
                chunk = fin.read(block_size)
                if not chunk:
                    break
                
                processed = bytearray()
                for byte in chunk:
                    # 核心加密算法保持不变
                    if encrypt:
                        processed.append((byte ^ key) + position % 256)
                    else:
                        processed.append((byte - position % 256) ^ key)
                    position += 1
                
                fout.write(bytes(processed))
            self.log(f"已处理 {position} 字节")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCryptoApp(root)
    root.mainloop()
