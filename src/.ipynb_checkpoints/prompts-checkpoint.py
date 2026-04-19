MULTIPLE_CHOICE_PROMPT = """请回答下面的多选题，请直接输出正确答案选项，不要输出其他内容。

题目：
{question}

选项：
{options}
"""


STRICT_FORMAT_PROMPT = """请回答下面的多选题。
你必须严格按照指定格式输出，不能输出其他无关内容。

题目：
{question}

选项：
{options}

输出格式：
最终答案：<选项>
"""


COT_PROMPT = """请回答下面的多选题。
请先简要分析，再输出最终答案。

题目：
{question}

选项：
{options}

输出格式：
分析：...
最终答案：...
"""


OPTION_ELIMINATION_PROMPT = """请回答下面的多选题。
请逐项判断每个选项是否正确，再给出最终答案。

题目：
{question}

选项：
{options}

输出格式：
A：正确/错误，原因
B：正确/错误，原因
C：正确/错误，原因
D：正确/错误，原因
最终答案：...
"""


ROLE_PROMPT = """你是一名经验丰富的药学考试专家，请根据专业药学知识回答下面的多选题。

题目：
{question}

选项：
{options}

要求：
1. 先简要分析
2. 最后给出最终答案

输出格式：
分析：...
最终答案：...
"""


REFLECTION_PROMPT = """请回答下面的多选题。
先给出初步答案，然后检查自己的答案是否有错误，最后输出修正后的最终答案。

题目：
{question}

选项：
{options}

输出格式：
初步分析：...
初步答案：...
自我检查：...
最终答案：...
"""


KNOWLEDGE_GUIDED_PROMPT = """请基于药学专业知识回答下面的多选题。
请先提取题干中的关键知识点，再分析选项，最后给出答案。

题目：
{question}

选项：
{options}

输出格式：
关键知识点：...
分析：...
最终答案：...
"""


FEW_SHOT_PROMPT = """下面先给出示例，再回答新题。

示例1：
题目：
阿司匹林的不良反应包括：
A: 胃肠道刺激
B: 呼吸抑制
C: 出血风险增加
D: 肝功能改善
分析：阿司匹林常见不良反应包括胃肠道刺激和出血风险增加。
最终答案：A,C

现在回答下面的问题：

题目：
{question}

选项：
{options}

输出格式：
分析：...
最终答案：...
"""


MULTI_SELECT_STRICT_PROMPT = """请回答下面的多选题。
注意：这是多选题，可能有一个或多个正确选项，不能漏选，也不能多选。

题目：
{question}

选项：
{options}

请逐项判断后输出答案。

输出格式：
分析：...
最终答案：...
"""


RAG_PROMPT = """请结合下面给出的参考知识回答多选题。

参考知识：
{context}

题目：
{question}

选项：
{options}

输出格式：
分析：...
最终答案：...
"""


RAG_COT_PROMPT = """请结合下面给出的参考知识回答多选题，并逐步推理。

参考知识：
{context}

题目：
{question}

选项：
{options}

要求：
1. 提取题干关键信息
2. 逐项判断
3. 最后输出最终答案

输出格式：
关键信息：...
逐项判断：...
最终答案：...
"""
#对应的builder函数
def build_baseline_prompt(sample: dict) -> str:
    return MULTIPLE_CHOICE_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_strict_prompt(sample: dict) -> str:
    return STRICT_FORMAT_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_cot_prompt(sample: dict) -> str:
    return COT_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_option_elimination_prompt(sample: dict) -> str:
    return OPTION_ELIMINATION_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_role_prompt(sample: dict) -> str:
    return ROLE_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_reflection_prompt(sample: dict) -> str:
    return REFLECTION_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_knowledge_guided_prompt(sample: dict) -> str:
    return KNOWLEDGE_GUIDED_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_few_shot_prompt(sample: dict) -> str:
    return FEW_SHOT_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_multi_select_strict_prompt(sample: dict) -> str:
    return MULTI_SELECT_STRICT_PROMPT.format(
        question=sample["question"],
        options=sample["options_text"]
    )


def build_rag_prompt(sample: dict, context: str) -> str:
    return RAG_PROMPT.format(
        context=context,
        question=sample["question"],
        options=sample["options_text"]
    )


def build_rag_cot_prompt(sample: dict, context: str) -> str:
    return RAG_COT_PROMPT.format(
        context=context,
        question=sample["question"],
        options=sample["options_text"]
    )