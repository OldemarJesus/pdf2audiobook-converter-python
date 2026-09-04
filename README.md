# pdf2audiobook-converter-python

Convert PDF documents into spoken Portuguese audiobooks (`.wav`) using open-source Hugging Face Text-to-Speech (TTS) models running directly on your GPU (NVIDIA CUDA) or CPU.

> 🤖 **AI Disclosure & Transparency:** This project was scaffolded using AI-assisted code generation (**Gemini 3.8 Flash**) and thoroughly reviewed, tested, and refined by humans ([@OldemarJesus](https://github.com/OldemarJesus)).

---

## 🎯 Goal & Features

- **Extract & Decrypt:** Extracts text directly from any standard or AES-encrypted PDF (e.g. university regulations, Diário da República official publications).
- **Two Language Flavors:**
  - 🇵🇹 **European Portuguese (pt-PT):** Uses **[Piper TTS](https://github.com/OHF-Voice/piper1-gpl)** (formerly Rhasspy Piper) with the native **`pt_PT-tugão-medium`** model downloaded automatically from Hugging Face (`rhasspy/piper-voices`). Extremely fast, lightweight, and natural European Portuguese pronunciation.
  - 🇧🇷 **Portuguese (Meta MMS):** Uses Meta's Massively Multilingual Speech model **`facebook/mms-tts-por`** via Hugging Face `transformers` with automated text chunking and NumPy audio concatenation.
- **Hardware Accelerated:** Leverages NVIDIA GPUs via CUDA (`torch` with CUDA and `onnxruntime-gpu`) with fallback to CPU.

---

## 📂 Project Structure

```text
pdf2audiobook-converter-python/
├── document.pdf                  # ⚠️ Required: Put your input PDF here
├── pdf2audiobook_ptpt.py         # Converter using European Portuguese (Piper TTS - tugão)
├── pdf2audiobook.py              # Converter using Meta MMS Portuguese model
├── requirements.txt              # Project package dependencies
├── .gitignore                    # Prevents committing venv, audio outputs, and PDFs
├── LICENSE                       # MIT License
├── CHANGELOG.md                  # Project history and release notes
├── AGENTS.md                     # AI agent architecture and context guide
└── README.md                     # Project documentation
```

---

## 📋 Prerequisites

- **Python:** Python 3.10+ (tested up to Python 3.14)
- **GPU (Recommended):** NVIDIA GPU with CUDA support (e.g., RTX 3060 12GB VRAM or similar) for blazing fast synthesis. CPU execution is also supported.
- **Input File:** A PDF file named **`document.pdf`** must be placed in the project root directory alongside the scripts.

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

> **Note:** If you are using Windows:
> ```powershell
> .venv\Scripts\activate
> ```

### 3. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Breakdown of key packages:
- **`torch`**, **`transformers`**, **`accelerate`**: For running Meta's MMS model.
- **`pypdf2`**, **`pycryptodome`**: For parsing and decrypting AES-encrypted PDFs.
- **`piper-tts`**, **`huggingface-hub`**: For fast European Portuguese neural TTS and model downloading.
- **`onnxruntime-gpu`**: To enable hardware GPU acceleration with Piper on NVIDIA CUDA.
- **`scipy`**, **`numpy`**: For audio sample synthesis and WAV file assembly.

> 💡 **GPU Acceleration Note for Piper:**
> `piper-tts` might install standard `onnxruntime` (CPU) as a dependency. If you see the warning:
> `UserWarning: Specified provider 'CUDAExecutionProvider' is not in available provider names`
> ensure `onnxruntime-gpu` is installed:
> ```bash
> pip uninstall onnxruntime -y
> pip install onnxruntime-gpu
> ```

---

## 🚀 How to Use

### Step 1: Place your PDF

Place the PDF document you want to convert into the root of this directory and name it **`document.pdf`**:

```bash
cp /path/to/your/file.pdf document.pdf
```

> ⚠️ **Important:** Both scripts look for `document.pdf` in the current working folder by default.

---

### Step 2: Run the converter

Ensure your virtual environment is active:
```bash
source .venv/bin/activate
```

#### Option A: European Portuguese (pt-PT) — *Recommended*
Runs the high-speed Piper TTS `tugão` model:

```bash
python pdf2audiobook_ptpt.py
```
- **Model:** `rhasspy/piper-voices` (`pt/pt_PT/tugão/medium`)
- **Output:** `portuguese_pt_audiobook.wav`

#### Option B: Portuguese (Meta MMS)
Runs Meta's MMS VITS model:

```bash
python pdf2audiobook.py
```
- **Model:** `facebook/mms-tts-por`
- **Output:** `portuguese_audiobook.wav`

---

## 🔬 Model Provenance & Training Data

This project relies exclusively on open-source, permissively licensed speech synthesis models hosted on Hugging Face:

| Voice / Language | Engine | Model ID / Repository | License |
| :--- | :--- | :--- | :--- |
| **European Portuguese (pt-PT)** | [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) | [`rhasspy/piper-voices` (pt_PT-tugão-medium)](https://huggingface.co/rhasspy/piper-voices) | MIT / Open Data |
| **Portuguese (Multilingual/BR)** | Meta MMS | [`facebook/mms-tts-por`](https://huggingface.co/facebook/mms-tts-por) | CC-BY-NC 4.0 / Open Access |

---

## 🎯 Scope of Intended Use & Compliance

- **Intended Purpose:** Personal, academic, and accessibility utility for local text-to-speech conversion of PDF documents.
- **Data Privacy & Governance:** All model inference, text extraction, and audio processing run **100% locally** on your machine. No document text or generated audio is transmitted to cloud APIs or external third parties.
- **Risk Posture:** Classified as **Minimal Risk** under EU AI Act guidelines; this utility performs local format shifting without autonomous decision-making or safety-critical implications.

---

## 🤖 AI Disclosure & Acknowledgments

This project was scaffolded using AI-assisted code generation (**Gemini 3.8 Flash**), with iterative architecture design, debugging, human oversight, and testing guided by [@OldemarJesus](https://github.com/OldemarJesus).

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
