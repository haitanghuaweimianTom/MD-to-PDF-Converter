@echo off
cd /d "C:\Users\hhh\Desktop\md-to-pdf-converter"

echo ========================================
echo 正在安装必需的Python依赖...
echo ========================================
pip install markdown weasyprint pyinstaller

echo.
echo ========================================
echo 正在打包应用程序...
echo ========================================
pyinstaller --onefile --windowed ^
  --add-data "mathjax;mathjax" ^
  --hidden-import=markdown.extensions.tables ^
  --hidden-import=markdown.extensions.fenced_code ^
  main.py

echo.
echo ========================================
echo 清理临时文件...
echo ========================================
rd /s /q build __pycache__ dist\main.spec 2>nul

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位置: C:\Users\hhh\Desktop\md-to-pdf-converter\dist\main.exe
echo ========================================
pause