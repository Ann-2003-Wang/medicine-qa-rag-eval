import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def build_model(
    model_name: str = "deepseek-chat",
    temperature: float = 0.5,
    timeout: int = 180,
):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    if not api_key:
        raise ValueError("请先设置环境变量 DEEPSEEK_API_KEY")

    model = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        timeout=timeout,
    )
    return model


def build_basic_chain(model):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI assistant. Please answer the user's question."),
            ("user", "{input}")
        ]
    )
    return prompt | model | StrOutputParser()


def ask_model(chain, text: str) -> str:
    return chain.invoke({"input": text})