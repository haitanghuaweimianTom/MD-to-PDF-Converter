# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 19:33:29 2026

@author: hhh
"""

import markdown
import re
import os
from weasyprint import HTML, CSS

def preprocess_math(text):
    """预处理LaTeX数学公式，转换为MathJax兼容格式"""
    # 处理块级公式 $$...$$
    text = re.sub(r'\$\$(.*?)\$\$', r'<div class="math">\1</div>', text, flags=re.DOTALL)
    # 处理行内公式 $...$
    text = re.sub(r'\$(.*?)\$', r'<span class="math inline">\1</span>', text)
    return text

def md_to_html(md_text, mathjax_path):
    """将Markdown转换为HTML，支持数学公式"""
    # 预处理数学公式
    md_text = preprocess_math(md_text)
    
    # 转换Markdown
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # 构建完整的HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
            h1, h2, h3, h4, h5, h6 {{ 
                margin-top: 24px; 
                margin-bottom: 16px;
                page-break-after: avoid;
            }}
            .math {{ 
                text-align: center; 
                margin: 1em 0;
                font-size: 1.2em;
            }}
            .math.inline {{ 
                display: inline; 
                text-align: left;
            }}
            code {{ 
                background-color: #f4f4f4; 
                padding: 2px 4px; 
                border-radius: 3px;
            }}
            pre {{ 
                background-color: #f4f4f4; 
                padding: 10px; 
                border-radius: 5px;
                overflow-x: auto;
            }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin: 1em 0;
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 8px; 
                text-align: left;
            }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    return full_html

def convert_md_to_pdf(md_file, pdf_file, app_path):
    """主转换函数"""
    try:
        # 读取Markdown文件
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为HTML
        html_content = md_to_html(md_content, app_path)
        
        # 转换为PDF
        HTML(string=html_content).write_pdf(pdf_file)
        
        return True
    except Exception as e:
        print(f"转换错误: {e}")
        return False