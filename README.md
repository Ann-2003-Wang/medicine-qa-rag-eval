# medicine-qa-rag-eval 医学问答 RAG 评测项目


一个面向**医学选择题问答**的轻量级评测项目，用于系统比较 **大语言模型（LLM）不同提示策略** 以及 **RAG（Retrieval-Augmented Generation，检索增强生成）** 方法的效果。  
本项目主要从 **准确率（Accuracy）**、**延迟（Latency）** 和 **解析成功率（Parse Success Rate）** 三个角度，对不同策略进行统一评测与分析。

---

## 一、项目简介

本项目的目标是：在医学多项选择问答任务上，比较不同 Prompt 策略和 RAG 管线对模型性能的影响。

项目支持：

- 多种 Prompt 策略的评测
- 基于外部医学知识文档的 RAG 问答
- 自动答案解析
- 指标统计与汇总
- 实验结果可视化

这个项目适合用于：

- LLM Prompt Engineering 实验
- 医学问答场景下的策略比较
- RAG 系统原型验证
- 课程项目 / 作品集展示

---

## 二、项目目标

本项目主要关注以下几个研究问题：

- 基础 Prompt 是否已经能在医学选择题上取得不错效果？
- Chain-of-Thought（CoT）是否能提升医学问答准确率？
- 严格格式约束（Strict Prompt）是否能提升输出可解析性？
- Option Elimination 是否更适合多选题场景？
- Reflection 是否能提升最终效果，还是只会增加延迟？
- 引入 RAG 后，是否能比纯 Prompt 方法取得更好的结果？

---

## 三、项目特点

- 支持多种 Prompt 策略统一评测
- 支持 RAG 与非 RAG 方法对比
- 支持医学多项选择问答任务
- 自动统计准确率、耗时和解析成功率
- 自动汇总实验结果
- 自动绘制结果图表
- 项目结构清晰，适合作品集展示

---

## 四、支持的策略

当前项目支持以下策略：

- `baseline`：基础提示策略
- `strict`：严格格式约束策略
- `cot`：Chain-of-Thought 推理策略
- `option_elimination`：选项排除策略
- `reflection`：自我反思策略
- `few_shot`：少样本提示策略
- `rag`：检索增强生成策略
- `rag_cot`：RAG + Chain-of-Thought 组合策略

---

## 五、项目结构

```text
medicine-qa-rag-eval/
├── data/
│   ├── 1.exam.json                  # 医学问答数据
│   └── kb/
│       └── who_eml_2025.pdf         # 外部知识文档（RAG知识源）
├── outputs/
│   ├── all_metrics.csv              # 所有策略的汇总指标
│   ├── metrics_*.csv                # 各策略评测指标
│   ├── predictions_*.csv            # 各策略预测结果
│   └── figures/                     # 可视化图表
├── src/
│   ├── data_utils.py                # 数据读取与处理
│   ├── evaluate.py                  # 评测逻辑
│   ├── llm_client.py                # 大模型接口调用
│   ├── parser.py                    # 输出解析
│   ├── prompts.py                   # Prompt模板
│   └── retriever.py                 # 检索模块
├── merge_metrics.py                 # 汇总不同策略的指标
├── plot_results.py                  # 绘制评测结果图
├── run_eval.py                      # 运行评测主程序
├── requirements.txt                 # 项目依赖
└── README.md                        # 项目说明文档

## 六、运行环境

建议使用以下环境：

- Python 3.8 及以上
- Windows / macOS / Linux 均可（本指引仅保留 Windows 命令）
- 可访问对应的大模型 API
- 建议使用虚拟环境

## 七、安装方法

### 1. 克隆仓库

```bash
git clone https://github.com/Ann-2003-Wang/medicine-qa-rag-eval.git
cd medicine-qa-rag-eval
```
### 2. 创建虚拟环境
```bash
python -m venv .venv
```

### 3. 激活虚拟环境（Windows）

```Windows cmd
.venv\Scripts\activate
```
### 4. 安装依赖
```bash
pip install -r requirements.txt
```
## 八、环境变量配置
在运行项目之前，需要先配置 API Key 和接口地址。

```Windows CMD

set DEEPSEEK_API_KEY=你的_api_key
set DEEPSEEK_BASE_URL=https://api.deepseek.com
```
## 九、使用方法
### 1. 运行基础策略评测
```bash
python run_eval.py --strategy baseline --model_name deepseek-chat
```
### 2. 运行其他策略评测
```bash
python run_eval.py --strategy strict --model_name deepseek-chat
python run_eval.py --strategy cot --model_name deepseek-chat
python run_eval.py --strategy option_elimination --model_name deepseek-chat
python run_eval.py --strategy reflection --model_name deepseek-chat
python run_eval.py --strategy few_shot --model_name deepseek-chat
python run_eval.py --strategy rag --model_name deepseek-chat
python run_eval.py --strategy rag_cot --model_name deepseek-chat
```

## 十、评测指标
本项目主要评估以下三个指标：

- 准确率（Accuracy）
衡量模型预测答案与标准答案一致的比例。

- 延迟（Latency）
衡量模型在不同策略下完成一次问答所需时间。

- 解析成功率（Parse Success Rate）
衡量模型输出是否能被程序成功解析为合法选项答案。

这三个指标分别对应：

- 效果：答得对不对

- 效率：答得快不快

- 稳定性：输出是否规范、能否自动处理

## 十一、输出结果说明
运行评测后，项目会在 outputs/ 目录下生成结果文件。

### 1. 预测结果文件
outputs/predictions_*.csv
保存每一种策略在数据集上的预测结果。

### 2. 单策略指标文件
outputs/metrics_*.csv
保存每一种策略对应的评测指标。

### 3. 汇总指标文件
outputs/all_metrics.csv
汇总所有策略的评测结果，便于横向比较。

### 4. 图表文件
outputs/figures/
通常包括：

- 各策略准确率对比图

- 各策略延迟对比图

- 各策略解析成功率对比图

## 十二、结果汇总与可视化
### 1. 汇总各策略指标
```bash
python merge_metrics.py
```
### 2. 绘制结果图
```bash
python plot_results.py
执行后可以在 outputs/figures/ 目录中查看图表结果。
```
## 十三、RAG 设置说明
本项目中的 RAG 模式使用外部医学知识文档作为知识来源：
```bash
data/kb/who_eml_2025.pdf
```
RAG 流程大致如下：

- 读取外部知识文档

- 根据问题检索相关内容

- 将检索到的上下文拼接进 Prompt

- 调用大模型生成答案

- 对结果进行解析和评测
