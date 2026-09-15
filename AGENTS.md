<!--
SPDX-FileCopyrightText: 2026 Oldemar
SPDX-License-Identifier: MIT
-->

# AGENTS.md — AI Agent Guide for pdf2audiobook-converter-python

## Project Overview
`pdf2audiobook-converter-python` is a lightweight, hardware-accelerated Python utility that extracts text from PDF files (including AES-encrypted official documents) and converts them into spoken audiobooks saved as `.wav` files and translated text documents using open-source Hugging Face models.

The project was originally developed and generated with **Gemini 3.8 Flash**, guided by [@OldemarJesus](https://github.com/OldemarJesus).

---

## Architecture & Codebase Map

The project is architected around a single, unified entry point (`main.py`) backed by the modular package `src/pdf2audiobook`:

```text
pdf2audiobook-converter-python/
├── main.py                          # 🚀 Unique unified CLI entry point (argparse subcommands)
├── src/
│   └── pdf2audiobook/
│       ├── __init__.py              # Package init & version
│       ├── pdf.py                   # PDF text extraction & AES decryption
│       ├── tts.py                   # Piper TTS & Meta MMS speech synthesis
│       └── translator.py            # MarianMT translation with technical term preservation
├── LICENSES/
│   └── MIT.txt                      # REUSE 3.3 canonical MIT license
├── .reuse/
│   └── dep5                         # REUSE dep5 copyright & license metadata
├── requirements.txt                 # Project dependencies
├── CHANGELOG.md                     # Release and update history
├── AGENTS.md                        # Architecture and guidance for AI agents
└── README.md                        # Human-facing documentation
```

### Supported Subcommands in `main.py`:
1. **`ptpt` (European Portuguese / pt-PT — Recommended)**
   - **TTS Engine:** [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) (`piper-tts`, `piper.voice.PiperVoice`).
   - **Model Repository:** [`rhasspy/piper-voices`](https://huggingface.co/rhasspy/piper-voices) (`pt/pt_PT/tugão/medium/pt_PT-tugão-medium.onnx`).
   - **Phonetic Target:** Native European Portuguese (`pt-PT`) phonetics.
   - **Characteristics:** Uses `voice.synthesize_wav(full_text, wav)` for continuous streaming synthesis.
   - **Execution Provider:** ONNX Runtime via CUDA (`onnxruntime-gpu`) when available, falling back to CPU.

2. **`mms-pt` (Brazilian / Multilingual Portuguese)**
   - **TTS Engine:** Meta MMS via Hugging Face Transformers (`VitsTokenizer`, `VitsModel`).
   - **Model Card:** [`facebook/mms-tts-por`](https://huggingface.co/facebook/mms-tts-por).
   - **Execution Provider:** PyTorch CUDA device (`device = "cuda" if torch.cuda.is_available() else "cpu"`).

3. **`mms-en` (English TTS)**
   - **TTS Engine:** Meta MMS via Hugging Face Transformers (`Baghdad99/english_voice_tts`).
   - **Execution Provider:** PyTorch CUDA / CPU.

4. **`translate` (English to Portuguese Neural Machine Translation)**
   - **Translation Engine:** MarianMT (`Helsinki-NLP/opus-mt-tc-big-en-pt`).
   - **Term Preservation:** Uses `TermPreserver` placeholder masking to protect technical keywords (e.g. LLM, CUDA, API, Docker, PyTorch) from translation.

5. **`pipeline` (End-to-End Translation + European Portuguese TTS)**
   - Translates English PDF into Portuguese text and directly synthesizes European Portuguese WAV audio in a single step.

---

## Key Dependencies & Known Gotchas

- **PDF Decryption:** Many Portuguese official/legal documents (e.g. Diário da República, university regulations) use AES encryption without passwords. Standard `pypdf2` will throw `PyPDF2.errors.DependencyError: PyCryptodome is required for AES algorithm` unless **`pycryptodome`** is present in the environment.
- **Piper TTS on CUDA:** When installing `piper-tts`, pip often resolves to standard CPU-only `onnxruntime`. To utilize NVIDIA GPUs, `onnxruntime` must be uninstalled and replaced with `onnxruntime-gpu`.
- **Piper API:** Use `voice.synthesize_wav(full_text, wav)` to write directly into an open `wave.open(output_file, 'wb')` handle. Do not use `voice.synthesize()` without iterating over its audio chunk generator, otherwise an empty 44-byte WAV header is created.
- **NumPy Concatenation for MMS:** Audio waveforms produced by `VitsModel` are 1D arrays; concatenate them using `np.concatenate(audio_pieces)` (1D), **not** with `axis=1`.
- **REUSE Compliance:** All files must follow REUSE 3.3 specification with `SPDX-FileCopyrightText` and `SPDX-License-Identifier` headers, verified via `reuse lint`.

---

## Environment & Development Setup

- Python 3.10+ in a local virtual environment (`.venv`):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

---

## Guidance for AI Agents Modifying This Codebase

- **CLI Conventions:** All new features or parameter adjustments must be wired through `main.py` subcommands with clear help messages and examples in `build_parser()`.
- **Chunking Logic:** Ensure sentence boundaries are preserved when splitting chunks rather than hard splitting on arbitrary character counts.
- **REUSE Compliance:** Always ensure `reuse lint` passes after adding or modifying files.
- **Git Hygiene:** Never commit `.venv/`, `.wav` files, or local `document.pdf` files; respect `.gitignore`.
