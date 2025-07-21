# LLM & Point-E

## 项目概述
这是我的人工智能基础大作业，实现了LLM（大语言模型）与Point-E模型的结合应用。

## 项目文件说明
- `llm.py`：用于对比不同temperature值下的生成效果
- `llm_module.py`：LLM代理模块
- `main.py`：交互系统和图形用户界面模块

## 环境配置

### Python版本要求
- Python: 3.9.81

### 模块依赖安装
```bash
# 1. 克隆point-e仓库
git clone https://github.com/openai/point-e.git

# 2. 进入项目目录
cd point-e-main

# 3. 放置核心文件
将llm.py、llm_module.py和main.py三个文件复制到point-e-main文件夹下

# 4. 安装point-e框架
pip install -e .

# 5. 安装项目所需依赖
pip install -r requirements.txt
```

### API 密钥配置
本程序测试时使用硅基流动 API Key 进行 DeepSeek API 调用，需要将其设置为名为 `API_KEY` 的环境变量。根据不同操作系统的终端，配置方式如下：
```CMD
# Windows 命令提示符（CMD）
set API_KEY = 您的api key
```
```powershell
# PowerShell
$env:API_KEY=您的实际API密钥
```
```bash
# Linux 或 macOS 终端
export API_KEY=您的实际API密钥
```

## 程序运行
完成上述所有配置后，在point-e-main文件夹目录下，通过终端执行以下命令启动程序：
```bash
python main.py
```
