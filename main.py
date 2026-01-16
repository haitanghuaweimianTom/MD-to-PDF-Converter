import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
from pathlib import Path

# 将当前目录添加到Python路径（打包后需要）
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from converter import convert_md_to_pdf

class MDToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown 转 PDF 转换器")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 创建UI
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Markdown文件选择
        ttk.Label(main_frame, text="Markdown 文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.md_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.md_var, width=50).grid(row=0, column=1, padx=5, sticky=tk.EW)
        ttk.Button(main_frame, text="浏览", command=self.browse_md).grid(row=0, column=2, padx=5)
        
        # PDF输出路径
        ttk.Label(main_frame, text="PDF 输出:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pdf_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.pdf_var, width=50).grid(row=1, column=1, padx=5, sticky=tk.EW)
        ttk.Button(main_frame, text="浏览", command=self.browse_pdf).grid(row=1, column=2, padx=5)
        
        # 转换按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        self.convert_btn = ttk.Button(button_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="使用说明", command=self.show_help).pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=tk.EW, pady=(0, 10))
        
        # 日志区域
        ttk.Label(main_frame, text="转换日志:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, font=('Consolas', 9))
        self.log_text.grid(row=5, column=0, columnspan=3, sticky=tk.EW)
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        
        # 设置默认值
        self.set_defaults()
    
    def set_defaults(self):
        desktop = str(Path.home() / "Desktop")
        self.pdf_var.set(os.path.join(desktop, "output.pdf"))
    
    def browse_md(self):
        file_path = filedialog.askopenfilename(
            title="选择Markdown文件",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        if file_path:
            self.md_var.set(file_path)
            # 自动设置PDF输出路径
            pdf_path = os.path.splitext(file_path)[0] + ".pdf"
            self.pdf_var.set(pdf_path)
    
    def browse_pdf(self):
        file_path = filedialog.asksaveasfilename(
            title="选择PDF保存位置",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.pdf_var.set(file_path)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        md_file = self.md_var.get().strip()
        pdf_file = self.pdf_var.get().strip()
        
        if not md_file or not pdf_file:
            messagebox.showerror("错误", "请选择输入和输出文件")
            return
        
        if not os.path.exists(md_file):
            messagebox.showerror("错误", f"文件不存在: {md_file}")
            return
        
        # 禁用按钮，启用进度条
        self.convert_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中执行转换
        threading.Thread(
            target=self.run_conversion,
            args=(md_file, pdf_file),
            daemon=True
        ).start()
    
    def run_conversion(self, md_file, pdf_file):
        try:
            self.log("开始转换...")
            self.log(f"输入: {md_file}")
            self.log(f"输出: {pdf_file}")
            
            # 执行转换
            success = convert_md_to_pdf(md_file, pdf_file, application_path)
            
            if success:
                self.log("✅ 转换成功！")
                # 询问是否打开PDF
                self.root.after(0, lambda: self.ask_open_pdf(pdf_file))
            else:
                self.log("❌ 转换失败")
                self.root.after(0, lambda: messagebox.showerror("错误", "转换失败，请查看日志"))
                
        except Exception as e:
            self.log(f"❌ 错误: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
        finally:
            self.root.after(0, self.restore_ui)
    
    def ask_open_pdf(self, pdf_file):
        if os.path.exists(pdf_file):
            if messagebox.askyesno("完成", "转换成功！是否打开PDF文件？"):
                try:
                    if sys.platform == "win32":
                        os.startfile(pdf_file)
                    elif sys.platform == "darwin":
                        os.system(f"open '{pdf_file}'")
                    else:
                        os.system(f"xdg-open '{pdf_file}'")
                except Exception as e:
                    self.log(f"无法打开PDF: {e}")
    
    def restore_ui(self):
        self.convert_btn.config(state=tk.NORMAL)
        self.progress.stop()
    
    def show_help(self):
        help_text = """
使用说明：

1. 选择Markdown文件（.md）
   - 支持标准Markdown语法
   - LaTeX公式：$...$（行内）或$$...$$（块级）

2. 选择PDF输出位置
   - 程序会自动生成PDF文件

3. 点击"开始转换"
   - 转换完成后会询问是否打开PDF
   - PDF包含可点击目录和正确渲染的数学公式

注意事项：
- 首次运行可能需要几秒钟初始化
- 确保有足够的磁盘空间
- 中文显示需要系统支持
        """
        messagebox.showinfo("使用说明", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MDToPDFConverter(root)
    root.mainloop()