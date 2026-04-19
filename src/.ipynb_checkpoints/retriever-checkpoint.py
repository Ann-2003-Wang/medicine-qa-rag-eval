import re
from pathlib import Path
from typing import List
from pypdf import PdfReader


def read_txt_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def normalize_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_len:
            break
        start = max(0, end - overlap)

    return chunks


def load_single_kb_file(path: Path, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    suffix = path.suffix.lower()

    if suffix in [".txt", ".md"]:
        text = read_txt_file(path)
    elif suffix == ".pdf":
        text = read_pdf_file(path)
    else:
        return []

    return chunk_text(text, chunk_size=chunk_size, overlap=overlap)


def load_kb(kb_path: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    """
    支持：
    - 单个文件：txt / md / pdf
    - 一个目录：自动读取目录下所有 txt / md / pdf
    """
    path = Path(kb_path)

    if not path.exists():
        raise FileNotFoundError(f"知识库路径不存在: {kb_path}")

    all_chunks = []

    if path.is_file():
        all_chunks.extend(load_single_kb_file(path, chunk_size, overlap))
    else:
        for file_path in sorted(path.rglob("*")):
            if file_path.suffix.lower() in [".txt", ".md", ".pdf"]:
                file_chunks = load_single_kb_file(file_path, chunk_size, overlap)
                all_chunks.extend(file_chunks)

    if not all_chunks:
        raise ValueError(f"没有从知识库中读取到任何内容: {kb_path}")

    return all_chunks


def tokenize_for_retrieval(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9\-\+\.]*", text)
    return tokens


class SimpleKeywordRetriever:
    def __init__(self, kb_chunks: List[str]):
        self.kb_chunks = kb_chunks
        self.chunk_tokens = [tokenize_for_retrieval(chunk) for chunk in kb_chunks]

    def score_chunk(self, query: str, chunk: str, chunk_tokens: List[str]) -> float:
        query_tokens = tokenize_for_retrieval(query)
        if not query_tokens:
            return 0.0

        token_set = set(chunk_tokens)
        overlap_score = sum(1 for tok in query_tokens if tok in token_set)

        chunk_lower = chunk.lower()
        substring_score = 0
        for tok in set(query_tokens):
            if tok in chunk_lower:
                substring_score += 0.3

        return overlap_score + substring_score

    def search(self, query: str, top_k: int = 3) -> List[str]:
        scored = []
        for chunk, chunk_tokens in zip(self.kb_chunks, self.chunk_tokens):
            score = self.score_chunk(query, chunk, chunk_tokens)
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = [chunk for score, chunk in scored[:top_k] if score > 0]

        if not results:
            results = self.kb_chunks[:top_k]

        return results


def build_context(docs: List[str]) -> str:
    return "\n\n".join([f"[知识片段{i+1}]\n{doc}" for i, doc in enumerate(docs)])