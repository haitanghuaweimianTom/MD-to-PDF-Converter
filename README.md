# MD to PDF Converter with LaTeX Math Support

## 工具介绍

这是一个Markdown转PDF转换器，支持复杂的LaTeX数学公式（使用$...$表示行内公式，$$...$$表示块级公式）。

主要功能：
- 支持Markdown到PDF的直接转换
- 支持复杂LaTeX数学公式渲染
- 自动检查依赖（Pandoc和XeLaTeX）
- 当PDF转换失败时，自动回退到HTML转换
- 生成详细的转换日志
- 支持中文文本和数学公式

## 安装说明
### 使用前准备：
在目标电脑上，确保：

1. 已安装MikTeX和Pandoc
2. 这两个程序的安装路径已添加到系统环境变量（PATH）
关于miktex和pandoc的安装，请双击basic-miktex.exe和pandoc.msi完成，记得勾选for all users
3. 首次运行时，MikTeX会自动安装缺少的LaTeX包（需保持网络连接，并且耐心等待一段时间，仅第一次需要较长时间安装LaTeX包）
4. 如果等待半小时后依旧无法正常使用，请重启电脑，让环境变量更改生效

### 方式一：直接使用EXE文件（推荐）

1. 下载`md2pdf.exe`文件
2. 将文件放在任意目录即可使用
3.直接将md文件拖动到exe上面，用exe打开，即在md文件的同一文件夹路径生成html网页，用浏览器打开，右键选择“打印”即可

### 方式二：从源码运行

1. 确保安装了Python 3.6+和pip
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行脚本：
   ```bash
   python md2pdf.py input.md -o output.pdf
   ```

## 依赖要求

转换器需要以下外部依赖：

1. **Pandoc**：用于Markdown转换
   - 下载地址：https://pandoc.org/installing.html

2. **MiKTeX**：用于LaTeX公式渲染
   - 下载地址：https://miktex.org/download

## 使用方法

### 基本用法

```bash
md2pdf.exe input.md
```

这将生成一个名为`input.pdf`的输出文件。

### 指定输出文件名

```bash
md2pdf.exe input.md -o output.pdf
```

### 开启调试模式

```bash
md2pdf.exe input.md --debug
```

### 仅检查依赖

```bash
md2pdf.exe --check-deps
```

## 示例

### 示例1：基本转换

```bash
md2pdf.exe test_math.md
```

### 示例2：指定输出文件名

```bash
md2pdf.exe chinese_test.md -o 中文测试.pdf
```

### 示例3：调试模式

```bash
md2pdf.exe complex_formulas.md -o complex.pdf --debug
```

## 常见问题

### 问题1：转换失败，提示缺少LaTeX包

**解决方案**：
- 确保MiKTeX已正确安装
- 首次运行时，MiKTeX会自动安装缺少的包，请保持网络连接
- 如果自动安装失败，可以手动安装缺少的包

### 问题2：中文显示乱码

**解决方案**：
- 确保Markdown文件使用UTF-8编码
- 转换器已默认添加UTF-8编码声明，无需额外设置

### 问题3：数学公式显示不正确

**解决方案**：
- 确保使用正确的LaTeX语法
- 行内公式使用`$...$`，块级公式使用`$$...$$`
- 如果PDF转换失败，转换器会自动生成HTML文件，使用浏览器打开即可正确显示数学公式

### 问题4：转换速度慢

**解决方案**：
- 首次转换时，MiKTeX需要下载和安装缺少的LaTeX包，可能会比较慢
- 后续转换会使用已安装的包，速度会加快

## 日志文件

转换过程中会生成`md2pdf.log`日志文件，包含详细的转换信息和错误日志，便于调试和排查问题。

## 技术支持

如果遇到问题，请查看日志文件`md2pdf.log`，或联系开发者。

