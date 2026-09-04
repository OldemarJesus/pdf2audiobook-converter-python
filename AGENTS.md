# AGENTS.md — AI Agent Guide for pdf2audiobook-converter-python

## Project Overview
`pdf2audiobook-converter-python` is a lightweight, hardware-accelerated Python utility that extracts text from PDF files (including AES-encrypted official documents) and converts them into spoken Portuguese audiobooks saved as `.wav` files using open-source Hugging Face models.

The project was originally developed and completely generated with **Gemini 3.8 Flash**, guided by [@OldemarJesus](https://github.com/OldemarJesus).

---

## Architecture & Codebase Map

The project contains two complementary converter scripts:

1. **`pdf2audiobook_ptpt.py` (European Portuguese / pt-PT — Recommended)**
   - **TTS Engine:** [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) (`piper-tts`, `piper.voice.PiperVoice` — formerly Rhasspy Piper).
   - **Model Repository:** [`rhasspy/piper-voices`](https://huggingface.co/rhasspy/piper-voices) on Hugging Face Hub.
   - **Model Files:** `pt/pt_PT/tugão/medium/pt_PT-tugão-medium.onnx` and `pt/pt_PT/tugão/medium/pt_PT-tugão-medium.onnx.json`.
   - **Phonetic Target:** Native European Portuguese (`pt-PT`) phonetics.
   - **Characteristics:** Zero text-chunking required. Uses `voice.synthesize_wav(full_text, wav)` for direct continuous streaming synthesis.
   - **Execution Provider:** ONNX Runtime via CUDA (`onnxruntime-gpu`) when available, falling back to CPU.
   - **Output:** `portuguese_pt_audiobook.wav`.

2. **`pdf2audiobook.py` (Brazilian/Multilingual Portuguese)**
   - **TTS Engine:** Meta's Massively Multilingual Speech (MMS) via Hugging Face Transformers (`VitsTokenizer`, `VitsModel`).
   - **Model Card:** [`facebook/mms-tts-por`](https://huggingface.co/facebook/mms-tts-por) on Hugging Face Hub.
   - **Phonetic Target:** Portuguese (predominantly Brazilian phonetics).
   - **Characteristics:** Splits text into 500-character chunks to avoid token and memory limits, feeds each chunk to the model, and concatenates 1D audio waveform NumPy arrays using `np.concatenate(audio_pieces)` before writing with `scipy.io.wavfile.write`.
   - **Execution Provider:** PyTorch CUDA device (`device = "cuda" if torch.cuda.is_available() else "cpu"`).
   - **Output:** `portuguese_audiobook.wav`.

---

## Key Dependencies & Known Gotchas

- **PDF Decryption:** Many Portuguese official/legal documents (e.g. Diário da República, university regulations) use AES encryption without passwords. Standard `pypdf2` will throw `PyPDF2.errors.DependencyError: PyCryptodome is required for AES algorithm` unless **`pycryptodome`** is present in the environment.
- **Piper TTS on CUDA:** When installing `piper-tts`, pip often resolves to standard CPU-only `onnxruntime`. To utilize NVIDIA GPUs, `onnxruntime` must be uninstalled and replaced with `onnxruntime-gpu`.
- **Piper API:** Use `voice.synthesize_wav(full_text, wav)` to write directly into an open `wave.open(output_file, 'wb')` handle. Do not use `voice.synthesize()` without iterating over its audio chunk generator, otherwise an empty 44-byte WAV header is created.
- **NumPy Concatenation for MMS:** Audio waveforms produced by `VitsModel` are 1D arrays; concatenate them using `np.concatenate(audio_pieces)` (1D), **not** with `axis=1`.
- **Input File Convention:** By default, both scripts look for `document.pdf` located in the root workspace directory.

---

## Environment & Development Setup

- Python 3.10+ in a local virtual environment (`.venv`):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- **Dependencies (`requirements.txt`):**
  - `torch`, `transformers`, `accelerate`
  - `pypdf2`, `pycryptodome`
  - `scipy`, `numpy`
  - `piper-tts`, `huggingface-hub`, `onnxruntime-gpu`

---

## Guidance for AI Agents Modifying This Codebase

- **Input Flexibility:** If extending the scripts with CLI arguments, prefer `argparse` allowing users to specify arbitrary input PDF paths and custom output filenames while preserving `document.pdf` as the default.
- **Chunking Logic:** If modifying `pdf2audiobook.py`, ensure sentence boundaries are preserved when splitting chunks rather than hard splitting on arbitrary character counts.
- **Git Hygiene:** Never commit `.venv/`, `.wav` files, or local `document.pdf` files; respect `.gitignore`.
