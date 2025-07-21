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

# 3. 放置文件
# 将llm.py、llm_module.py和main.py三个文件复制到point-e-main文件夹下

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

## 效果展示
### 输入：我想生成一个大的现代化的彩色的木质的有趣的椅子  
输出词：chair colorful wooden modern  
生成图片：   
<img width="206" height="256" alt="image" src="https://github.com/user-attachments/assets/8cf58555-98fa-4fc8-ad56-0a4eb5b3f506" />  
不使用LLM生成的图片：  
<img width="211" height="222" alt="bb3ff504eb41e8c34bf0402acb33f2bc" src="https://github.com/user-attachments/assets/6e382bb7-832f-4f48-95ce-af598bf6fb74" />  
翻译成英文再生成：I want to generate a large, modern, colorful, wooden, and interesting chair.  
<img width="211" height="218" alt="a657dac5cf0ad157cf801e88b346a303" src="https://github.com/user-attachments/assets/b5a7323e-5c41-4056-9b12-10f423e2848a" />

### 输入：我想生成一个红黄蓝相间大皮凳子  
输出词：stool red, yellow, blue leather object
生成图片：  
<img width="222" height="308" alt="image" src="https://github.com/user-attachments/assets/765ea102-e2b0-4a46-a4c1-2aca30c8f60e" />  
不使用LLM生成的图片：  
<img width="222" height="154" alt="dcd22f7bbeecdedcb357fb31f8b4b583" src="https://github.com/user-attachments/assets/08bcf809-c73c-45d1-ac7a-72ca3f62f62e" /> 
翻译成英文再生成：I want to generate a large leather stool with red, yellow and blue colors.  
<img width="224" height="226" alt="918d790e394defbcca0641680bce5901" src="https://github.com/user-attachments/assets/e5d15000-fda9-49ec-b848-ea193fc21172" />

### 输入：给咱来一个黑白复古老旧掉链子自行车   
输出词：bicycle black and white object vintage  
生成图片：  
<img width="222" height="212" alt="image" src="https://github.com/user-attachments/assets/831bf37c-9759-4237-90a6-a4edc950e290" />  
不使用LLM生成的图片：  
<img width="234" height="137" alt="290ba3833a3e3f4bf9c4c9b074df3c6a" src="https://github.com/user-attachments/assets/f61ac9b4-a354-4a72-9a94-f19799157961" />  
翻译成英文再生成：Give me a black-and-white, vintage, old-fashioned bicycle with a broken chain.  
<img width="228" height="139" alt="80517ae2c6f977400a3c718d42c66b76" src="https://github.com/user-attachments/assets/d69ba3cc-c837-41b1-b1b0-b5e16fb66148" />

### 输入：OMG，天呢宝贝，本可尊素想要获得五个超级无敌美丽好看五彩斑斓的小星星，哈尼可以实现我这个小小的愿望吗，人家是真的真的很想要  
输出词：star multicolored object beautiful and super gorgeous  
生成图片：  
<img width="231" height="354" alt="image" src="https://github.com/user-attachments/assets/42a581af-4ff0-49b2-80bd-79bdf36b59d6" />  
不使用LLM生成的图片:  
<img width="233" height="189" alt="c36b422ebe5b9967048cc23299259efb" src="https://github.com/user-attachments/assets/5bd7463f-f03b-41e9-bae8-021f7ffefa6f" />  
翻译成英文再生成：OMG, oh my god baby, I，the queen，really want to get five super ultra beautiful, good-looking and colorful little stars. Honey, can you fulfill my little wish? I really, really want them.  
<img width="228" height="221" alt="53eb488e5b6bfe7fe79c501702eb0b75" src="https://github.com/user-attachments/assets/87c58e29-df91-4859-bb07-bdc2723d9f79" />

### 输入：什么你听说了吗，今天天气特别好，天上星星月亮都没有，有的只有太阳，但是我呢？我不是一颗小草，据说先有鸡还是后有蛋，这不重要，我不想生成这些东西，是的没错！我是男的！！红的桌子，这是我要生成的，因为云朵很淡，我回了母校，黄河自行车，摩托车开过去了。  
输出词：table red object object  
生成图片：  
<img width="247" height="267" alt="image" src="https://github.com/user-attachments/assets/a1f19313-79bb-4b6b-a5e8-d0173c2a090f" />  
不使用LLM生成的图片：  
<img width="247.5" height="66.75" alt="f55b72934c1618402bfb66b06ae46de7" src="https://github.com/user-attachments/assets/69a75ec2-2eaf-40fd-bc5e-8190bb437d18" />  
翻译成英文再生成：Did you hear? The weather is especially nice today. There are no stars or moon in the sky—only the sun. But me? I’m not a blade of grass. They say the age-old question is whether the chicken came first or the egg, but that doesn’t matter. I don’t want to generate any of those things. That’s right! I’m male!! A red table—that’s what I want to generate. Because the clouds are faint, I went back to my alma mater. Huanghe and bicycle, a motorcycle passed by.  
<img width="247.5" height="191.25" alt="7d80e0c4d91960d5f91fd5005366fdf6" src="https://github.com/user-attachments/assets/4fd45346-b2eb-445a-89ea-15f07b876017" />

### 输入：好吃的苹果香蕉！来个绿摩托！化学生物都比不过大盘鸡面条获取一个出生成功的紫色早上好仿佛蓝牛肉面  
输出词：green motorcycle green object object  
生成图片：  
<img width="225" height="249" alt="image" src="https://github.com/user-attachments/assets/48c65905-4861-4478-a9c6-f4efb6d79f72" />  
不使用LLM生成的图片：  
<img width="223" height="250" alt="d37af44e3d6812dc87dba368ee658dc9" src="https://github.com/user-attachments/assets/70848f3c-c50e-408b-af21-1354f1c6bc2f" />  
翻译成英文再生成：Delicious apples and bananas! Bring me a green motorcycle! Chemistry and biology can not compare to big plate chicken noodles. Get a successfully born purple "good morning" as if it were blue beef noodles. 
<img width="236" height="226" alt="bdb94baa98ae3c787c707a8b4b0126dc" src="https://github.com/user-attachments/assets/6a63b0b4-1e51-4244-b97a-7f14b7839d4c" />
