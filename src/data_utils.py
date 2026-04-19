#数据初始化，数据读取脚本

import json
from pathlib import Path


def load_exam_data(file_path: str):
    """
    读取考试题目 JSON 文件
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"加载完成，共 {len(data)} 道题目")
    return data


def format_options(option_dict: dict) -> str:
    """
    将选项字典格式化成 prompt 可直接使用的文本
    例如：
    {"A": "...", "B": "..."} -> "A:...\nB:..."
    """
    return "\n".join([f"{k}: {v}" for k, v in option_dict.items()])


def preprocess_sample(sample: dict) -> dict:
    """
    对单条样本做轻量预处理，补充 options_text 字段
    """
    new_sample = sample.copy()
    if "option" in new_sample:
        new_sample["options_text"] = format_options(new_sample["option"])
    else:
        raise KeyError("样本中缺少 'option' 字段")
    return new_sample


def preprocess_dataset(data: list) -> list:
    """
    对整个数据集预处理
    """
    return [preprocess_sample(sample) for sample in data]