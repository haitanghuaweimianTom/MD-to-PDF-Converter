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
3. 首次运行时，MikTeX会自动安装缺少的LaTeX包（需保持网络连接，并且耐心等待一段时间，仅第一次需要较长时间安装LaTeX包）
4. 如果等待半小时后依旧无法正常使用，请重启电脑，让环境变量更改生效

### MiKTeX安装详细设置：

1. 双击`basic-miktex.exe`开始安装
2. **选择安装范围**：
   - 勾选"For all users (recommended)"
   - 安装路径使用默认路径（通常为`C:\Program Files\MiKTeX`）
3. **关键设置：自动安装宏包**：
   - 在安装过程中，会出现"Settings"页面
   - 找到"Install missing packages"选项
   - 从下拉菜单中选择**Yes**（如图所示）
   - 这个设置确保MiKTeX会自动下载并安装转换过程中需要的LaTeX宏包
   - 纸张大小选择"A4"
   - 点击"下一步(N) >"继续安装

   ![MiKTeX Settings](images/miktex_settings.png)

4. **完成安装**：
   - 等待安装完成
   - 安装完成后，建议重启计算机以确保环境变量更新

### Pandoc安装：

1. 双击`pandoc.msi`开始安装
2. 勾选"For all users"选项
3. 确保勾选"Add pandoc to PATH"选项
4. 按照默认选项完成安装

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

在releases里面有对应的安装包。

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
- 确保MiKTeX已正确安装，安装时install missing packages 选择YES
- 首次运行时，MiKTeX会**自动安装**缺少的包，请保持网络连接
- 转换器已配置为`batchmode`，允许MiKTeX在后台自动安装缺少的包
- 如果自动安装失败，可以手动打开MiKTeX包管理器，搜索并安装缺少的包
- 示例：如果提示缺少`infwarerr.sty`，可以在MiKTeX包管理器**MiKTeX Console**中搜索`infwarerr`并安装

### 问题2：中文显示乱码

**解决方案**：
- 确保Markdown文件使用UTF-8编码
- 转换器已默认添加UTF-8编码声明，无需额外设置
- 如果PDF转换中的中文显示有问题，可以使用HTML转换结果

### 问题3：数学公式显示不正确

**解决方案**：
- 确保使用正确的LaTeX语法
- 行内公式使用`$...$`，块级公式使用`$$...$$`
- 如果PDF转换失败，转换器会**自动生成HTML文件**，使用浏览器打开即可正确显示数学公式，可以在浏览器打开html文件后右键点击页面，选择 **打印** 即可输出PDF
- HTML文件使用MathJax渲染公式，支持所有LaTeX语法

### 问题4：转换速度慢

**解决方案**：
- 首次转换时，MiKTeX需要下载和安装缺少的LaTeX包，可能会比较慢
- 后续转换会使用已安装的包，速度会加快
- 建议首次运行时使用简单的测试文件，让MiKTeX安装基础包

### 问题5：PDF转换失败，生成了HTML文件

**解决方案**：
- 这是正常的回退机制，当PDF转换失败时，会自动生成HTML文件
- 可以使用浏览器打开HTML文件，然后使用浏览器的"打印"功能将其转换为PDF
- HTML文件包含了所有内容和样式，转换为PDF后效果与直接生成的PDF类似

### 问题6：提示"Windows API error 267: 目录名称无效"

**解决方案**：
- 这是由于MiKTeX无法找到指定的字体目录
- 转换器已处理此问题，会自动回退到HTML转换
- 可以直接使用生成的HTML文件，或手动调整MiKTeX的字体设置

## 日志文件

转换过程中会生成`md2pdf.log`日志文件，包含详细的转换信息和错误日志，便于调试和排查问题。

## 技术支持

如果遇到问题，请查看日志文件`md2pdf.log`，或联系开发者。
