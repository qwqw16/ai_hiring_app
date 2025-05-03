# 🤖 AI 智能招聘助手

这是一个基于 **Streamlit + OpenAI GPT** 的互动式招聘系统，能自动完成简历筛选、面试问题生成、候选人回答评分、薪资推荐及 offer 确认等招聘流程。

---

## 🌟 项目功能亮点

- 📄 **上传 PDF 简历**
- 🌐 **自动识别简历语言（支持中文和英文）**
- 🧠 **AI 打分简历匹配度**
- ❓ **根据简历自动生成英文面试问题**
- 🗣️ **对候选人回答进行 AI 评分**
- 💵 **根据评分动态计算可提供的薪资范围**
- 🎁 **展示个性化福利包及 offer 接受环节**

---

## 🧰 技术栈

- `Streamlit` —— 用于构建网页界面
- `OpenAI GPT-3.5` —— 提供自然语言处理能力
- `pdfplumber` —— 读取 PDF 简历文本
- `langdetect` —— 检测简历语言
- `Python` —— 构建核心逻辑与交互流程

---

## 📦 安装使用方法

### 1. 克隆项目
git clone https://github.com/qwqw16/ai_hiring_app.git
cd ai_hiring_app

### 2. 安装依赖
pip install -r requirements.txt

### 3. 配置 API 密钥
在项目根目录下新建 .env 文件，写入以下内容（替换为你自己的 OpenAI Key）：
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

## 🚀 本地运行
streamlit run app.py




