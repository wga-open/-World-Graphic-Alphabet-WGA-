# DeepSeek 文本分析工具

一个强大的文本分析和可视化工具，结合了自然语言处理和基于图像的学习支持。该工具旨在帮助用户通过视觉辅助理解多种语言的文本。

## 功能特点

- **多语言支持**：支持中文、英文、日语、阿拉伯语、法语、德语、葡萄牙语、西班牙语和俄语
- **智能文本分析**：使用 DeepSeek AI 进行高级文本注释和分析
- **视觉学习**：将图像与文本集成，增强理解
- **交互式界面**：现代化响应式用户界面，支持实时处理
- **翻译集成**：内置百度翻译 API 支持多语言翻译
- **词库管理**：全面的词汇数据库，支持图像关联
- **可自定义显示**：可调整文本与图像比例和分页

## 技术架构

### 核心组件

1. **界面管理器 (`ui_manager.py`)**
   - 处理所有界面相关功能
   - 管理语言切换
   - 创建和维护应用程序窗口
   - 实现响应式布局

2. **文本处理器 (`deepseek_module.py`)**
   - 集成 DeepSeek AI 进行文本分析
   - 处理文本分块和处理
   - 管理 API 通信和响应解析

3. **数据处理器 (`data_processor.py`)**
   - 处理和分析文本标记
   - 管理分词
   - 处理词库匹配和优化

4. **图像加载器 (`image_loader.py`)**
   - 管理图像加载和缓存
   - 处理图像调整大小和优化
   - 提供图像到文本的关联

5. **翻译服务 (`Baidu_Text_transAPI.py`)**
   - 集成百度翻译 API
   - 处理多语言翻译
   - 管理 API 认证和请求

6. **词库管理器 (`lexicon_manager.py`)**
   - 管理词汇数据库
   - 处理词汇图像关联
   - 优化词库加载和缓存

7. **分页管理器 (`pagination.py`)**
   - 处理内容分页
   - 管理页面渲染
   - 实现滚动功能

## 安装说明

1. **环境要求**
   ```bash
   Python 3.7+
   pip install requests
   pip install pillow
   pip install pandas
   pip install jieba
   ```

2. **配置**
   - 在 `Baidu_Text_transAPI.py` 中设置百度翻译 API 凭证
   - 在 `deepseek_module.py` 中配置 DeepSeek API 密钥
   - 确保所需图像资源位于 `TU` 目录中
   - 将词库数据放在 `KU.csv` 中

3. **运行应用**
   ```bash
   python main.py
   ```

## 使用说明

1. **文本输入**
   - 在输入框中输入文本（最多1000字符）
   - 从下拉菜单中选择所需语言
   - 点击"开始处理"

2. **查看结果**
   - 使用导航按钮在页面间移动
   - 使用百分比按钮调整显示比例
   - 悬停在文本上查看附加信息
   - 查看与文本关联的图像

3. **语言切换**
   - 从下拉菜单中选择语言
   - 文本和界面将自动更新
   - 翻译实时处理

## 项目结构

```
├── main.py                 # 主程序入口
├── ui_manager.py          # 界面管理和布局
├── deepseek_module.py     # DeepSeek AI 集成
├── data_processor.py      # 文本处理和分析
├── image_loader.py        # 图像处理和优化
├── Baidu_Text_transAPI.py # 翻译服务
├── lexicon_manager.py     # 词库管理
├── pagination.py          # 内容分页
├── tooltip.py            # 提示框功能
├── TU/                   # 图像资源目录
└── KU.csv               # 词库数据库
```

## 依赖项

- **外部 API**
  - DeepSeek AI API
  - 百度翻译 API

- **Python 包**
  - requests
  - pillow
  - pandas
  - jieba
  - tkinter

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 联系方式

如需支持或咨询，请联系：familyerpro@gmail.com 