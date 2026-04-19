import os
import time
import argparse
import pandas as pd

from src.data_utils import load_exam_data, preprocess_dataset
from src.llm_client import build_model, build_basic_chain
from src.evaluate import evaluate_dataset, summarize_metrics
from src.retriever import load_kb, SimpleKeywordRetriever


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="data/1.exam.json")
    parser.add_argument("--strategy", type=str, default="baseline")
    parser.add_argument("--model_name", type=str, default="deepseek-chat")
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--output", type=str, default="outputs")
    parser.add_argument("--kb_path", type=str, default="data/pharma_kb.txt")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    data = load_exam_data(args.data)
    data = preprocess_dataset(data)

    model = build_model(
        model_name=args.model_name,
        temperature=args.temperature,
        timeout=180
    )
    chain = build_basic_chain(model)

    retriever = None
    if args.strategy in ["rag", "rag_cot"]:
        kb_chunks = load_kb(args.kb_path)
        retriever = SimpleKeywordRetriever(kb_chunks)

    start_all = time.time()

    df = evaluate_dataset(
        dataset=data,
        chain=chain,
        strategy=args.strategy,
        retriever=retriever
    )

    total_time = time.time() - start_all

    metrics = summarize_metrics(df)
    metrics["model"] = args.model_name
    metrics["strategy"] = args.strategy
    metrics["total_time_sec"] = round(total_time, 2)
    metrics["samples_per_sec"] = round(len(data) / total_time, 4) if total_time > 0 else 0

    print(metrics)

    df.to_csv(
        f"{args.output}/predictions_{args.model_name}_{args.strategy}.csv",
        index=False,
        encoding="utf-8-sig"
    )

    pd.DataFrame([metrics]).to_csv(
        f"{args.output}/metrics_{args.model_name}_{args.strategy}.csv",
        index=False,
        encoding="utf-8-sig"
    )


if __name__ == "__main__":
    main()