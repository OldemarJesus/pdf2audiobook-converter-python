# SPDX-FileCopyrightText: 2026 Oldemar
# SPDX-License-Identifier: MIT

import re
import torch
from transformers import MarianMTModel, MarianTokenizer

DEFAULT_PRESERVE_TERMS = [
    "AI", "API", "APIs", "LLM", "LLMs", "Machine Learning", "Deep Learning",
    "Framework", "Backend", "Frontend", "Fullstack", "DevOps", "CI/CD",
    "Cloud", "Docker", "Kubernetes", "Microservices", "Database", "SQL", "NoSQL",
    "Dataset", "Token", "Tokens", "Tokenizer", "Embeddings", "Prompt", "Prompts",
    "Fine-tuning", "Zero-shot", "Few-shot", "RAG", "Transformer", "Transformers",
    "GPU", "CPU", "CUDA", "TensorFlow", "PyTorch", "ONNX", "Hugging Face",
    "Python", "JavaScript", "TypeScript", "Rust", "Go", "Git", "GitHub",
    "Open Source", "Benchmark", "Pipeline", "Endpoint", "Deploy", "Deployment"
]


class TermPreserver:
    """Protects specified terms/acronyms from translation using temporary mask tokens."""

    def __init__(self, terms: list[str] = None):
        self.terms = sorted(terms or DEFAULT_PRESERVE_TERMS, key=len, reverse=True)

    def mask(self, text: str) -> tuple[str, dict[str, str]]:
        mapping = {}
        counter = 0

        for term in self.terms:
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

            def replace_match(match):
                nonlocal counter
                placeholder = f"__TERM_{counter}__"
                mapping[placeholder] = match.group(0)
                counter += 1
                return placeholder

            text = pattern.sub(replace_match, text)

        return text, mapping

    def unmask(self, text: str, mapping: dict[str, str]) -> str:
        for placeholder, original in mapping.items():
            text = re.sub(rf"\s*{re.escape(placeholder)}\s*", f" {original} ", text)
        return re.sub(r"\s+", " ", text).strip()


def split_sentences_for_translation(text: str, max_words: int = 60) -> list[str]:
    """Splits text into clean sentence/clause segments for MarianMT."""
    raw_sentences = re.split(r"(?<=[.?!;])\s+", text)
    chunks = []

    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        words = sentence.split()
        if len(words) <= max_words:
            chunks.append(sentence)
        else:
            for i in range(0, len(words), max_words):
                chunks.append(" ".join(words[i:i + max_words]))
    return chunks


def translate_english_to_portuguese(
    text: str,
    output_path: str = "translated_document_pt.txt",
    custom_terms: list[str] = None,
    model_name: str = "Helsinki-NLP/opus-mt-tc-big-en-pt",
    device: str = None,
    batch_size: int = 16,
) -> str:
    """Translates English text into Portuguese while preserving technical terms.

    Args:
        text: Input English text.
        output_path: Path to save the translated text.
        custom_terms: Additional technical terms to keep untranslated.
        model_name: MarianMT model ID.
        device: 'cuda' or 'cpu'.
        batch_size: Sentence batch size for neural MT inference.

    Returns:
        Full translated Portuguese text string.
    """
    if not text.strip():
        raise ValueError("Input text is empty.")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[{device.upper()}] Loading translation model '{model_name}'...")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).to(device)
    model.eval()

    sentences = split_sentences_for_translation(text)
    print(f"Translating {len(sentences)} sentence segments...")

    preserve_list = DEFAULT_PRESERVE_TERMS + (custom_terms if custom_terms else [])
    preserver = TermPreserver(preserve_list)
    translated_segments = []

    with torch.no_grad():
        for i in range(0, len(sentences), batch_size):
            batch_sentences = sentences[i:i + batch_size]
            masked_batch = []
            mappings = []

            for sent in batch_sentences:
                masked_text, mapping = preserver.mask(sent)
                masked_batch.append(masked_text)
                mappings.append(mapping)

            inputs = tokenizer(
                masked_batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(device)

            translated_tokens = model.generate(**inputs, max_length=512, num_beams=4)
            decoded_batch = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)

            for decoded, mapping in zip(decoded_batch, mappings):
                unmasked_text = preserver.unmask(decoded, mapping)
                translated_segments.append(unmasked_text)

            current_count = min(i + batch_size, len(sentences))
            if current_count % 32 == 0 or current_count == len(sentences):
                print(f"  Translated {current_count}/{len(sentences)} segments...")

    full_translated_text = " ".join(translated_segments)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_translated_text)
        print(f"[SUCCESS] Translated text saved to: {output_path}")

    return full_translated_text
