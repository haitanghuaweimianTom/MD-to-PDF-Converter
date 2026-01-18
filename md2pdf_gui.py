#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter with LaTeX Math Support (GUI Version)
Supports: $...$ (inline math) and $$...$$ (block math)
Requires: pandoc, miktex (xelatex)
"""

import argparse
import subprocess
import logging
import os
import tempfile
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('md2pdf.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class MD2PDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MD to PDF Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.input_files = []
        self.output_folder = ""
        self.debug = False
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input files section
        input_frame = ttk.LabelFrame(main_frame, text="输入文件", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Select files button
        ttk.Button(input_frame, text="选择MD文件", command=self.select_files).pack(side=tk.LEFT, padx=5)
        
        # Clear files button
        ttk.Button(input_frame, text="清空列表", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # Debug checkbox
        self.debug_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="调试模式", variable=self.debug_var).pack(side=tk.RIGHT, padx=5)
        
        # Files listbox
        files_frame = ttk.Frame(main_frame, padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.files_listbox = tk.Listbox(files_frame, selectmode=tk.MULTIPLE, height=10)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        # Output folder section
        output_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="输出文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.output_folder_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_folder_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(output_frame, text="浏览", command=self.select_output_folder).grid(row=0, column=2, padx=5, pady=5)
        
        # Convert button
        convert_frame = ttk.Frame(main_frame, padding="10")
        convert_frame.pack(fill=tk.X, pady=5)
        
        self.convert_button = ttk.Button(convert_frame, text="开始转换", command=self.start_conversion, style="Accent.TButton")
        self.convert_button.pack(fill=tk.X)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        ttk.Label(main_frame, textvariable=self.status_var, anchor=tk.CENTER).pack(fill=tk.X, pady=5)
        
        # Configure styles
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078d7")
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="选择Markdown文件",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.files_listbox.insert(tk.END, file)
        
        self.update_status(f"已选择 {len(self.input_files)} 个文件")
    
    def clear_files(self):
        self.input_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_status("就绪")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_folder = folder
            self.output_folder_var.set(folder)
            self.update_status(f"输出文件夹：{folder}")
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("警告", "请先选择要转换的MD文件")
            return
        
        if not self.output_folder:
            self.output_folder = os.getcwd()
            self.output_folder_var.set(self.output_folder)
        
        self.debug = self.debug_var.get()
        
        # Disable convert button during conversion
        self.convert_button.config(state=tk.DISABLED)
        
        # Create a thread for conversion to avoid freezing the UI
        conversion_thread = Thread(target=self.convert_files)
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def convert_files(self):
        total_files = len(self.input_files)
        success_count = 0
        
        self.update_status("开始转换...")
        self.update_progress(0)
        
        for i, input_file in enumerate(self.input_files):
            try:
                self.update_status(f"转换中：{os.path.basename(input_file)} ({i+1}/{total_files})")
                
                # Determine output file paths
                input_path = Path(input_file)
                output_file = os.path.join(self.output_folder, input_path.stem + ".pdf")
                html_output = os.path.join(self.output_folder, input_path.stem + ".html")
                
                # Convert to PDF
                success = self.convert_md_to_pdf(input_file, output_file, self.debug)
                
                if success:
                    success_count += 1
                else:
                    self.update_status(f"PDF转换失败，生成HTML：{os.path.basename(input_file)}")
                
                # Update progress
                progress = (i + 1) / total_files * 100
                self.update_progress(progress)
                
            except Exception as e:
                logger.error(f"转换文件 {input_file} 时出错：{str(e)}")
                self.update_status(f"转换 {os.path.basename(input_file)} 时出错：{str(e)}")
        
        self.update_progress(100)
        self.update_status(f"转换完成！成功：{success_count}/{total_files}")
        self.convert_button.config(state=tk.NORMAL)
        
        messagebox.showinfo("转换完成", f"转换完成！成功：{success_count}/{total_files}")
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        # Check pandoc
        try:
            result = subprocess.run(
                ['pandoc', '--version'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            logger.info(f"✓ Pandoc found: {result.stdout.splitlines()[0]}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("✗ Pandoc not found. Please install pandoc first.")
            messagebox.showerror("错误", "未找到Pandoc。请先安装Pandoc。")
            return False
        except UnicodeDecodeError:
            logger.warning("⚠ Pandoc version check: Unicode decode error, but pandoc is available")
        
        # Check xelatex (miktex)
        try:
            result = subprocess.run(
                ['xelatex', '--version'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            try:
                version_line = result.stdout.splitlines()[0].strip()
                logger.info(f"✓ XeLaTeX found: {version_line}")
            except (IndexError, AttributeError):
                logger.info("✓ XeLaTeX found: Version information not available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("✗ XeLaTeX not found. Please install MikTeX first.")
            messagebox.showerror("错误", "未找到XeLaTeX。请先安装MiKTeX。")
            return False
        except UnicodeDecodeError:
            logger.warning("⚠ XeLaTeX version check: Unicode decode error, but xelatex is available")
        
        return True
    
    def convert_md_to_pdf(self, input_file, output_file, debug=False):
        """Convert Markdown file to PDF with reliable fallback"""
        logger.info(f"Converting {input_file} to {output_file}...")
        
        # Use absolute paths for input and output to avoid issues
        input_abs = os.path.abspath(input_file)
        output_abs = os.path.abspath(output_file)
        
        # Basic pandoc command with math and HTML support
        basic_cmd = [
            'pandoc',
            input_abs,
            '-o', output_abs,
            '--from=markdown+raw_html+tex_math_dollars',  # Support math and raw html
            '--syntax-highlighting=default',  # Use default highlighting which requires fewer packages
            '-V', 'geometry:margin=1in',
            '-V', 'documentclass=article',
            '-V', 'fontsize=12pt'
        ]
        
        logger.debug(f"Using basic command: {' '.join(basic_cmd)}")
        
        # Try PDF conversion first
        pdf_success = False
        try:
            # Execute basic pandoc command
            result = subprocess.run(
                basic_cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            
            if result.stdout:
                logger.debug(f"Pandoc stdout: {result.stdout}")
            if result.stderr:
                logger.warning(f"Pandoc stderr: {result.stderr}")
            
            logger.info(f"✓ PDF conversion successful! Output: {output_file}")
            pdf_success = True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ PDF conversion failed with exit code {e.returncode}")
            logger.error(f"Command: {' '.join(basic_cmd)}")
            if e.stdout:
                logger.error(f"Stdout: {e.stdout}")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr}")
        except Exception as e:
            logger.error(f"✗ Unexpected error during PDF conversion: {str(e)}")
        
        # Always convert to HTML as reliable fallback
        logger.info("Generating HTML fallback...")
        
        # Convert to HTML first
        html_output = output_abs.replace('.pdf', '.html')
        html_cmd = [
            'pandoc',
            input_abs,
            '-o', html_output,
            '--mathjax',
            '-s',  # Standalone HTML with header and footer
            '--syntax-highlighting=default'
        ]
        
        try:
            # Convert to HTML
            subprocess.run(
                html_cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            logger.info(f"✓ HTML conversion successful: {html_output}")
            
            return pdf_success
            
        except subprocess.CalledProcessError as e2:
            logger.error(f"✗ HTML conversion also failed: {e2.returncode}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error during HTML conversion: {str(e)}")
            return False

def main():
    root = tk.Tk()
    app = MD2PDFConverter(root)
    
    # Check dependencies on startup
    if not app.check_dependencies():
        sys.exit(1)
    
    root.mainloop()

if __name__ == '__main__':
    main()
