'''
这个文件本质上就是：
1. 选 prompt 策略: get_prompt_by_strategy(...)
2. 跑整份数据集: evaluate_dataset(...)
3. 统计最后指标: summarize_metrics(...)
'''

import time
import pandas as pd
from collections import Counter
from tqdm import tqdm

from src.parser import extract_answer, normalize_gold_answer
from src.prompts import (
    build_baseline_prompt,
    build_strict_prompt,
    build_cot_prompt,
    build_option_elimination_prompt,
    build_role_prompt,
    build_reflection_prompt,
    build_knowledge_guided_prompt,
    build_few_shot_prompt,
    build_multi_select_strict_prompt,
    build_rag_prompt,
    build_rag_cot_prompt,
)


def get_prompt_by_strategy(sample: dict, strategy: str, retriever=None):
    """
    根据 strategy 构造 prompt。
    对于 rag / rag_cot，需要额外传入 retriever。
    返回:
        prompt_text, retrieved_docs
    """
    if strategy == "baseline":
        return build_baseline_prompt(sample), None

    elif strategy == "strict":
        return build_strict_prompt(sample), None

    elif strategy == "cot":
        return build_cot_prompt(sample), None

    elif strategy == "option_elimination":
        return build_option_elimination_prompt(sample), None

    elif strategy == "role":
        return build_role_prompt(sample), None

    elif strategy == "reflection":
        return build_reflection_prompt(sample), None

    elif strategy == "knowledge_guided":
        return build_knowledge_guided_prompt(sample), None

    elif strategy == "few_shot":
        return build_few_shot_prompt(sample), None

    elif strategy == "multi_select_strict":
        return build_multi_select_strict_prompt(sample), None

    elif strategy == "rag":
        if retriever is None:
            raise ValueError("strategy='rag' 时必须提供 retriever")
        query = f"{sample['question']}\n{sample['options_text']}"
        docs = retriever.search(query, top_k=3)
        context = "\n\n".join(docs)
        return build_rag_prompt(sample, context), docs

    elif strategy == "rag_cot":
        if retriever is None:
            raise ValueError("strategy='rag_cot' 时必须提供 retriever")
        query = f"{sample['question']}\n{sample['options_text']}"
        docs = retriever.search(query, top_k=3)
        context = "\n\n".join(docs)
        return build_rag_cot_prompt(sample, context), docs

    else:
        raise ValueError(f"Unknown strategy: {strategy}")


# 注意：这是 Self-consistency，不是“自注意力机制”
def run_self_consistency(sample, chain, base_prompt_func, n=5):
    answers = []
    raw_outputs = []

    for _ in range(n):
        prompt = base_prompt_func(sample)
        response = chain.invoke({"input": prompt})
        raw_outputs.append(response)

        pred = extract_answer(response)
        if pred is not None:
            answers.append(tuple(pred))

    if not answers:
        return None, raw_outputs

    final_answer = Counter(answers).most_common(1)[0][0]
    return list(final_answer), raw_outputs


def evaluate_dataset(dataset, chain, strategy: str, retriever=None):
    rows = []

    progress_bar = tqdm(dataset, desc=f"Evaluating [{strategy}]", ncols=100)

    total_correct = 0
    total_success = 0
    total_parsed = 0

    for i, sample in enumerate(progress_bar):
        prompt, retrieved_docs = get_prompt_by_strategy(
            sample,
            strategy,
            retriever=retriever
        )

        start_time = time.time()
        try:
            response = chain.invoke({"input": prompt})
            latency = time.time() - start_time
            success = True
            error_msg = None
        except Exception as e:
            response = None
            latency = time.time() - start_time
            success = False
            error_msg = str(e)

        pred = extract_answer(response) if response else None
        gold = normalize_gold_answer(sample.get("answer"))
        correct = (pred == gold) if (pred is not None and gold is not None) else False

        total_correct += int(correct)
        total_success += int(success)
        total_parsed += int(pred is not None)

        current_acc = total_correct / (i + 1)
        current_api_success = total_success / (i + 1)
        current_parse_success = total_parsed / (i + 1)

        progress_bar.set_postfix({
            "acc": f"{current_acc:.3f}",
            "api_ok": f"{current_api_success:.3f}",
            "parse_ok": f"{current_parse_success:.3f}",
            "latency": f"{latency:.2f}s"
        })

        rows.append({
            "id": sample.get("id", i),
            "strategy": strategy,
            "question": sample.get("question"),
            "options_text": sample.get("options_text"),
            "gold": gold,
            "pred": pred,
            "correct": correct,
            "latency": latency,
            "success": success,
            "error": error_msg,
            "response": response,
            "retrieved_docs": "\n\n".join(retrieved_docs) if retrieved_docs else None,
        })

    return pd.DataFrame(rows)


def summarize_metrics(df: pd.DataFrame):
    n_samples = len(df)

    if n_samples == 0:
        return {
            "n_samples": 0,
            "accuracy": 0.0,
            "avg_latency": 0.0,
            "api_success_rate": 0.0,
            "parse_success_rate": 0.0,
        }

    accuracy = df["correct"].mean()
    avg_latency = df["latency"].mean()
    api_success_rate = df["success"].mean()
    parse_success_rate = df["pred"].notna().mean()

    return {
        "n_samples": int(n_samples),
        "accuracy": round(float(accuracy), 4),
        "avg_latency": round(float(avg_latency), 4),
        "api_success_rate": round(float(api_success_rate), 4),
        "parse_success_rate": round(float(parse_success_rate), 4),
    }