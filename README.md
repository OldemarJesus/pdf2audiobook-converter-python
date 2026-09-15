<!--
SPDX-FileCopyrightText: 2026 Oldemar
SPDX-License-Identifier: MIT
-->

# pdf2audiobook-converter-python

[![REUSE status](https://api.reuse.software/badge/github.com/OldemarJesus/pdf2audiobook-converter-python)](https://api.reuse.software/info/github.com/OldemarJesus/pdf2audiobook-converter-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CUDA Accelerated](https://img.shields.io/badge/CUDA-Hardware%20Accelerated-76B900.svg)](https://developer.nvidia.com/cuda-zone)

Convert PDF documents into high-quality spoken audiobooks (`.wav`) and translated text using open-source Hugging Face models running 100% locally on your NVIDIA GPU (CUDA) or CPU.

> 🤖 **AI Disclosure & Transparency:** This project was scaffolded using AI-assisted code generation (**Gemini 3.8 Flash**) and thoroughly reviewed, tested, and refined with human oversight ([@OldemarJesus](https://github.com/OldemarJesus)).

---

## 🎯 Goal & Features

- **Unique Unified CLI (`main.py`):** Single entry point with subcommands, comprehensive `--help`, and intuitive examples for every utility.
- **Extract & Decrypt:** Extracts text directly from standard and AES-encrypted PDFs (e.g. Diário da República, official notices, academic regulations).
- **Multilingual Speech Synthesis (TTS):**
  - 🇵🇹 **European Portuguese (pt-PT) — *Recommended*:** High-speed streaming synthesis using **[Piper TTS](https://github.com/OHF-Voice/piper1-gpl)** with the **`pt_PT-tugão-medium`** ONNX model (`rhasspy/piper-voices`).
  - 🇧🇷 **Portuguese (Meta MMS):** Uses Meta's Massively Multilingual Speech model **`facebook/mms-tts-por`** via Hugging Face `transformers` VITS with sentence-boundary chunking.
  - 🇬🇧 **English (Meta MMS):** English speech synthesis using **`Baghdad99/english_voice_tts`** via VITS.
- **English-to-Portuguese Neural Translation (`translate`):** Translates English PDFs using **`Helsinki-NLP/opus-mt-tc-big-en-pt`** while masking and preserving technical terminology (e.g. AI, CUDA, LLM, Docker, Kubernetes, PyTorch).
- **End-to-End Pipeline (`pipeline`):** One-step translation of English PDFs into Portuguese followed immediately by European Portuguese audiobook synthesis.
- **Hardware Accelerated:** Optimized for NVIDIA CUDA GPUs (`torch` + `onnxruntime-gpu`) with automatic fallback to CPU.
- **REUSE 3.3 Compliant:** Fully adheres to the Free Software Foundation Europe (FSFE) REUSE licensing standard.

---

## 📂 Project Structure

```text
pdf2audiobook-converter-python/
├── main.py                          # 🚀 Unified CLI entry point
├── src/
│   └── pdf2audiobook/
│       ├── __init__.py              # Package metadata
│       ├── pdf.py                   # PDF text extraction & AES decryption
│       ├── tts.py                   # Piper TTS & Meta MMS audio synthesis
│       └── translator.py            # MarianMT translation with technical term preservation
├── LICENSES/
│   └── MIT.txt                      # Canonical MIT license (REUSE compliant)
├── .reuse/
│   └── dep5                         # REUSE metadata configuration
├── requirements.txt                 # Project dependencies
├── CHANGELOG.md                     # Release notes & version history
├── AGENTS.md                        # AI agent guide & architecture specification
└── README.md                        # Project documentation
```

---

## 📋 Prerequisites

- **Python:** Python 3.10+ (tested up to Python 3.14)
- **GPU (Recommended):** NVIDIA GPU with CUDA support (e.g., RTX 3060 12GB VRAM or higher) for rapid synthesis. CPU execution is fully supported.
- **Input File:** Place your PDF in the workspace (default: `document.pdf`) or pass `--pdf /path/to/file.pdf` / `--text /path/to/file.txt`.

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/OldemarJesus/pdf2audiobook-converter-python.git
cd pdf2audiobook-converter-python
```

### 2. Create and activate a virtual environment (`.venv`)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Note for Windows:**
> ```powershell
> .venv\Scripts\activate
> ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> 💡 **GPU Acceleration for Piper TTS:**
> If you see `UserWarning: Specified provider 'CUDAExecutionProvider' is not in available provider names`, ensure `onnxruntime-gpu` is installed:
> ```bash
> pip uninstall onnxruntime -y
> pip install onnxruntime-gpu
> ```

---

## 🚀 Unified CLI Usage (`main.py`)

Run `python main.py --help` to display the global overview and available utilities:

```bash
python main.py --help
```

```text
usage: python main.py [-h] <command> ...

🎙️ pdf2audiobook-converter-python — Convert PDFs into high-quality spoken audiobooks and translate documents.

Commands / Utilities:
  ptpt        Convert PDF or text to European Portuguese (pt-PT) audio using Piper TTS (tugão).
  mms-pt      Convert PDF or text to Portuguese audio using Meta MMS (facebook/mms-tts-por).
  mms-en      Convert PDF or text to English audio using Meta MMS (Baghdad99/english_voice_tts).
  translate   Translate English PDF or text to Portuguese, preserving key technical terms.
  pipeline    Full pipeline: Translate English PDF to Portuguese AND generate European Portuguese audio.
```

---

### 1. European Portuguese (pt-PT) Audiobook — *Recommended*

Generates fast, natural European Portuguese audio using the Piper `tugão` model.

```bash
# Convert default document.pdf
python main.py ptpt

# Convert custom PDF with custom output name
python main.py ptpt --pdf my_doc.pdf --output my_audiobook.wav

# Convert plain text file (e.g. translated text)
python main.py ptpt --text translated_document_pt.txt --output pt_audiobook.wav
```

---

### 2. Portuguese Audiobook (Meta MMS)

Synthesizes speech using Meta's Massively Multilingual Speech VITS model.

```bash
python main.py mms-pt --pdf document.pdf --output portuguese_audiobook.wav
```

---

### 3. English Audiobook (Meta MMS)

Synthesizes English speech from a PDF or text file.

```bash
python main.py mms-en --pdf document.pdf --output english_audiobook.wav
```

---

### 4. Translate English PDF to Portuguese (Preserving Technical Terms)

Translates English text to Portuguese using MarianMT while protecting domain acronyms and technical terms (e.g., *LLM*, *CUDA*, *API*, *Docker*, *PyTorch*).

```bash
# Basic translation
python main.py translate --pdf document.pdf --output translated_document_pt.txt

# Translation preserving additional custom terms
python main.py translate --pdf document.pdf --output translated_document_pt.txt --terms Rust LangChain Ollama
```

---

### 5. End-to-End Pipeline (Translate + Speak)

Translates an English PDF into Portuguese and directly synthesizes European Portuguese audio in a single command:

```bash
python main.py pipeline --pdf english_document.pdf --output-txt translated_pt.txt --output-audio final_audiobook.wav
```

---

## 🔬 Model Provenance & Licensing

All models used in this project are open-source and hosted on Hugging Face:

| Utility / Target | Engine / Framework | Model Repository | Model License |
| :--- | :--- | :--- | :--- |
| **European Portuguese (pt-PT)** | [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) | [`rhasspy/piper-voices` (pt_PT-tugão-medium)](https://huggingface.co/rhasspy/piper-voices) | MIT / Open Data |
| **Portuguese (Multilingual)** | Meta MMS (VITS) | [`facebook/mms-tts-por`](https://huggingface.co/facebook/mms-tts-por) | CC-BY-NC 4.0 / Open Access |
| **English TTS** | Meta MMS (VITS) | [`Baghdad99/english_voice_tts`](https://huggingface.co/Baghdad99/english_voice_tts) | CC-BY-NC 4.0 / Open Access |
| **EN → PT Translation** | MarianMT | [`Helsinki-NLP/opus-mt-tc-big-en-pt`](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt) | CC-BY-4.0 / Open Data |

---

## 🎯 Scope of Intended Use & Compliance

- **Data Privacy:** 100% local processing. No PDF text or synthesized audio is transmitted to external cloud APIs.
- **Risk Posture:** Classified as **Minimal Risk** under EU AI Act guidelines; performs local format shifting without autonomous decision-making.
- **REUSE 3.3 Compliance:** This project complies with the [REUSE Specification](https://reuse.software/) version 3.3. Verify compliance at any time with:
  ```bash
  reuse lint
  ```

---

## 📄 License

The source code of this project is licensed under the [MIT License](LICENSES/MIT.txt).
See individual model cards above for respective model weight terms.
