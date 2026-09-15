# SPDX-FileCopyrightText: 2026 Oldemar
# SPDX-License-Identifier: MIT

import re
import wave
import numpy as np
import scipy.io.wavfile
import torch
from huggingface_hub import hf_hub_download
from transformers import VitsTokenizer, VitsModel


def chunk_text_by_sentence(text: str, max_chars: int = 450) -> list[str]:
    """Splits text into chunks respecting sentence boundaries to prevent memory/token limits.

    Args:
        text: Input text string.
        max_chars: Maximum character limit per chunk.

    Returns:
        List of text chunks.
    """
    raw_sentences = re.split(r"(?<=[.?!;])\s+", text.strip())
    chunks = []
    current_chunk = ""

    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(sentence) > max_chars:
            # Subdivide overly long sentences by words
            words = sentence.split()
            for word in words:
                if len(current_chunk) + len(word) + 1 < max_chars:
                    current_chunk += (" " if current_chunk else "") + word
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = word
        else:
            if len(current_chunk) + len(sentence) + 1 < max_chars:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def synthesize_piper_ptpt(
    text: str,
    output_path: str = "portuguese_pt_audiobook.wav",
    device: str = None,
    repo_id: str = "rhasspy/piper-voices",
    model_name: str = "pt/pt_PT/tugão/medium/pt_PT-tugão-medium",
) -> str:
    """Synthesizes European Portuguese (pt-PT) audio using Piper TTS.

    Args:
        text: Text to speak.
        output_path: Destination WAV file path.
        device: 'cuda' or 'cpu' (auto-detected if None).
        repo_id: Hugging Face repo ID for Piper voices.
        model_name: Relative path to voice model within repo.

    Returns:
        Output file path.
    """
    from piper.voice import PiperVoice

    if not text.strip():
        raise ValueError("Input text is empty.")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    use_gpu = (device == "cuda")
    print(f"[{device.upper()}] Downloading/loading European Portuguese Piper model (tugão)...")

    model_file = hf_hub_download(repo_id=repo_id, filename=f"{model_name}.onnx")
    config_file = hf_hub_download(repo_id=repo_id, filename=f"{model_name}.onnx.json")

    voice = PiperVoice.load(model_file, config_path=config_file, use_cuda=use_gpu)

    print(f"Generating pt-PT audiobook to '{output_path}'...")
    with wave.open(output_path, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    print(f"[SUCCESS] European Portuguese audiobook saved to: {output_path}")
    return output_path


def synthesize_vits_mms(
    text: str,
    model_id: str,
    output_path: str,
    device: str = None,
    chunk_size: int = 450,
) -> str:
    """Synthesizes speech using Hugging Face VitsModel (e.g. Meta MMS).

    Args:
        text: Input text string.
        model_id: Hugging Face model identifier.
        output_path: Destination WAV file path.
        device: 'cuda' or 'cpu' (auto-detected if None).
        chunk_size: Character limit per chunk.

    Returns:
        Output file path.
    """
    if not text.strip():
        raise ValueError("Input text is empty.")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[{device.upper()}] Loading VITS model '{model_id}'...")
    tokenizer = VitsTokenizer.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id).to(device)
    model.eval()

    chunks = chunk_text_by_sentence(text, max_chars=chunk_size)
    print(f"Synthesizing {len(chunks)} text chunks...")

    audio_pieces = []
    with torch.no_grad():
        for i, chunk in enumerate(chunks, 1):
            inputs = tokenizer(chunk, return_tensors="pt").to(device)
            outputs = model(**inputs)
            waveform = outputs.waveform[0].cpu().numpy()
            audio_pieces.append(waveform)
            if i % 10 == 0 or i == len(chunks):
                print(f"  Processed chunk {i}/{len(chunks)}")

    if not audio_pieces:
        raise RuntimeError("No audio was generated.")

    final_audio = np.concatenate(audio_pieces)
    sample_rate = model.config.sampling_rate

    scipy.io.wavfile.write(output_path, rate=sample_rate, data=final_audio)
    print(f"[SUCCESS] Audiobook saved to: {output_path}")
    return output_path
