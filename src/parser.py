import re


def extract_answer(text: str):
    """
    从模型输出中提取答案，统一返回列表形式：
    - 单选：['B']
    - 多选：['A', 'C']
    如果无法提取，返回 None
    """
    if text is None:
        return None

    text = text.strip().upper()

    # 优先从“最终答案”或“答案”字段中提取
    priority_patterns = [
        r"最终答案[:：]\s*([A-E](?:[,，、\s]*[A-E])*)",
        r"答案[:：]\s*([A-E](?:[,，、\s]*[A-E])*)",
        r"FINAL ANSWER[:：]?\s*([A-E](?:[,，、\s]*[A-E])*)",
    ]

    for pattern in priority_patterns:
        m = re.search(pattern, text)
        if m:
            raw = m.group(1)
            opts = sorted(set(re.findall(r"[A-E]", raw)))
            return opts if opts else None

    # 兜底：如果没有明确“答案：...”，尝试抓所有独立出现的 A-E
    matches = re.findall(r"\b[A-E]\b", text)
    if matches:
        return sorted(set(matches))

    return None


def normalize_gold_answer(gold):
    """
    把标准答案统一成列表形式：
    - 'AC' -> ['A', 'C']
    - 'A,C' -> ['A', 'C']
    - ['A', 'C'] -> ['A', 'C']
    """
    if gold is None:
        return None

    if isinstance(gold, str):
        return sorted(set(re.findall(r"[A-E]", gold.upper())))

    if isinstance(gold, list):
        return sorted([str(x).strip().upper() for x in gold])

    return None


def is_correct(pred, gold):
    """
    比较预测答案和标准答案是否一致
    """
    if pred is None:
        return False

    gold = normalize_gold_answer(gold)
    if gold is None:
        return False

    pred = sorted(pred)
    return pred == gold


if __name__ == "__main__":
    examples = [
        "最终答案：A,C",
        "答案：B",
        "分析：xxx\n最终答案：D",
        "FINAL ANSWER: A, D",
        "A B C",
        None,
    ]

    for text in examples:
        print("输入:", text)
        print("输出:", extract_answer(text))
        print("-" * 30)