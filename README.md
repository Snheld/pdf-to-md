# pdf-to-md

一个用于 **Claude Code** 的本地 Skill，用于将本地 PDF 文件转换为 Markdown，并自动提取 PDF 中的图片到 `images/` 目录。

该 Skill 适合处理接口文档、产品文档、方案文档、对接文档等本地 PDF 文件，尽可能保留文档标题、分页、表格和嵌入图片，方便后续检索、编辑和二次加工。

---

## 功能特性

- 将本地 PDF 转换为 `.md` 文件
- 自动提取 PDF 中的嵌入图片到 `images/` 目录
- 自动输出文档标题和页数信息
- 基于字体大小、加粗和编号规则进行标题识别
- 自动提取表格并转换为 Markdown Table
- 支持命令行指定输出路径
- 适合作为 Claude Code 的本地 Skill 使用

---

## 目录结构

```text
pdf-to-md/
├── README.md
├── SKILL.md
└── scripts/
    ├── pdf_to_md.py
    └── run_pdf_to_md.py
```

文件说明：

- `SKILL.md`：Skill 定义文件，用于让 Claude Code 识别和触发该技能
- `scripts/pdf_to_md.py`：核心 PDF 转 Markdown 脚本
- `scripts/run_pdf_to_md.py`：包装入口脚本，提供稳定的执行入口

---

## 安装方式

### 1. 放置到 Claude Code skills 目录

将本项目放到本地 Claude Code skills 目录下，例如：

```text
C:\Users\<your-name>\.claude\skills\pdf-to-md
```

确保目录中至少包含：

- `SKILL.md`
- `scripts/pdf_to_md.py`
- `scripts/run_pdf_to_md.py`

### 2. 安装 Python 依赖

本项目依赖 [PyMuPDF](https://pymupdf.readthedocs.io/)。

安装方式：

```bash
pip install pymupdf
```

---

## 使用方法

### 在 Claude Code 中使用

当你在 Claude Code 中提出类似请求时，可以触发该 Skill：

- `把这个 PDF 转成 md`
- `Convert this local PDF to markdown`
- `提取这个 PDF 的内容，保留表格和图片`

### 直接通过命令行使用

#### 默认输出到同目录同名 `.md`

```bash
python "C:/Users/<your-name>/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/path/to/input.pdf"
```

#### 指定输出路径

```bash
python "C:/Users/<your-name>/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/path/to/input.pdf" -o "C:/path/to/output.md"
```

---

## 示例命令

### 示例 1：将 PDF 转为同目录 Markdown

```bash
python "C:/Users/suzhucong/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/Users/suzhucong/Desktop/xxx/xxxx.0.2.pdf"
```

执行后将生成：

- xxxx.md`
- `images/`

### 示例 2：指定输出文件

```bash
python "C:/Users/suzhucong/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/docs/api.pdf" -o "C:/docs/output/api.md"
```

---

## 输出结果

运行成功后，通常会生成以下内容：

- 一个 Markdown 文件，例如：`input.md`
- 一个图片目录，例如：`images/`

Markdown 内容通常包含：

- 文档标题
- 原始 PDF 文件名
- 总页数
- 分页分隔标记
- 自动识别的标题
- Markdown 表格
- 指向 `images/` 目录的图片引用

---

## 依赖说明

### 必需依赖

- Python 3.9+
- PyMuPDF (`fitz`)

安装命令：

```bash
pip install pymupdf
```

---

## 限制说明

当前版本存在以下限制：

1. **不提供 OCR 能力**  
   该工具主要提取 PDF 中原生可读取的文本、表格和嵌入图片；对于扫描件 PDF，文本提取效果有限。

2. **标题识别基于启发式规则**  
   当前标题识别依赖编号格式、字体大小和加粗等规则，对于排版特殊的 PDF，可能出现误判或漏判。

3. **复杂布局支持有限**  
   对于双栏排版、复杂浮动布局、特殊图文混排文档，输出顺序可能不完全理想。

4. **表格识别依赖 PDF 本身结构**  
   若 PDF 表格结构不规范，Markdown 表格的提取效果可能受影响。

5. **图片输出目录固定为 `images/`**  
   当前版本默认在输出目录下生成 `images/` 文件夹，未提供自定义图片目录参数。

---

## 适用场景

本项目适合以下场景：

- 接口文档 PDF 转 Markdown
- 产品文档、方案文档归档为可编辑文本
- 对接文档、技术说明文档结构化提取
- 将 PDF 内容转为便于检索、二次加工的 Markdown 格式
- 在 Claude Code 工作流中快速处理本地 PDF 文件

---

## 注意事项

- 请优先使用**绝对路径**，避免路径解析问题
- 如果指定输出路径，请确保目标目录存在
- 如果输出文件已存在，建议先确认是否覆盖
- Windows 终端下可能出现中文日志显示乱码，这通常是控制台编码问题，不影响实际生成结果
- 对于非常大的 PDF，处理时间会随页数和图片数量增加

---

## 开发说明

当前 Skill 的核心逻辑封装在：

- `scripts/pdf_to_md.py`

推荐通过以下入口执行：

- `scripts/run_pdf_to_md.py`

这样可以保持 Skill 触发方式稳定，便于后续扩展参数或调整内部实现。

---

## License

如需开源发布，请根据你的实际选择补充 License（例如 MIT、Apache-2.0 等）。

如果你准备公开发布，建议同时补充：

- `LICENSE`
- `.gitignore`
- 示例输入/输出说明

---

## 未来可扩展方向

- 增加批量转换目录下多个 PDF 的能力
- 增加图片输出目录配置项
- 增加页码范围选择
- 增加 OCR 支持
- 改进复杂布局和标题识别策略

---

如果你正在使用 Claude Code，并希望把本地 PDF 转换能力封装成一个可复用的 Skill，这个项目可以作为一个轻量、实用的起点。
