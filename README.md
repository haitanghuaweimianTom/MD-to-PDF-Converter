# Markdown 转 PDF 转换器 (MD to PDF Converter)

这是一个基于 Python 开发的桌面级工具，旨在为用户提供简单、直观的界面，将 Markdown 文档快速转换为排版精美的 PDF 文件。

## 🌟 功能特点

*   **直观界面**：基于 Tkinter 开发的图形化界面，操作简单，无需记忆命令行。
*   **标准语法支持**：全面支持标准 Markdown 语法，包括：
    *   表格 (Tables)
    *   栅栏代码块 (Fenced Code Blocks)
    *   分级标题
*   **数学公式支持**：
    *   行内公式：使用 `$E=mc^2$` 格式。
    *   块级公式：使用 `$$...$$` 格式。
*   **实时转换日志**：提供转换进度反馈和错误调试信息。
*   **一键预览**：转换完成后可直接在默认 PDF 阅读器中打开结果。
*   **自动路径生成**：选定输入文件后自动建议输出路径，减少重复点击。

## 🚀 如何使用 (EXE 版本)

1.  **启动程序**：双击运行 `main.exe`。
2.  **选择文件**：点击“Markdown 文件”旁的“浏览”按钮，选择你要转换的 `.md` 文件。
3.  **确认输出**：程序会自动将 PDF 输出路径设为原文件同目录。如需修改，可点击“PDF 输出”旁的“浏览”按钮。
4.  **开始转换**：点击“开始转换”按钮。进度条会开始运行，日志窗口会显示实时状态。
5.  **查看结果**：转换完成后，弹窗会询问“是否打开 PDF 文件”，点击“是”即可立即预览。

## 🛠️ 技术栈

*   **GUI 框架**：Tkinter
*   **核心逻辑**：
    *   `Python-Markdown`：解析 Markdown 语法。
    *   `WeasyPrint`：高性能的 HTML 到 PDF 渲染引擎。
    *   `Regular Expressions`：预处理 LaTeX 数学公式。

## 📦 如何从源码重新打包 (开发者参考)

如果你修改了 `main.py` 或 `converter.py` 并想重新生成 `.exe`，建议使用 `PyInstaller`：

1.  安装依赖：
    ```bash
    pip install markdown weasyprint
    pip install pyinstaller
    ```

2.  使用以下命令打包（确保将相关 DLL 和依赖包含在内）：
    ```bash
    pyinstaller --noconfirm --onedir --windowed --name "MD_Converter" "main.py"
    ```

## ⚠️ 注意事项

*   **中文字体**：PDF 转换质量取决于系统安装的字体。如果发现中文无法显示，请确保系统安装了标准字体（如 Arial 或微软雅黑）。
*   **数学公式**：本工具采用 MathJax 兼容的 HTML 类名进行预处理。如果公式特别复杂，建议检查 LaTeX 语法的闭合性。
*   **系统环境**：在 Windows 上运行打包后的 EXE 不需要安装 Python 环境，但需确保系统没有防火墙阻止文件写入权限。

---

**由 [haitanghuaweimianTom] 开发**
*更新日期：2026-01-16*