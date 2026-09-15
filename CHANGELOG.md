<!--
SPDX-FileCopyrightText: 2026 Oldemar
SPDX-License-Identifier: MIT
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-15

### Added
- **Unified CLI Entry Point (`main.py`):** Single entry point with subcommands (`ptpt`, `mms-pt`, `mms-en`, `translate`, `pipeline`) and rich contextual `--help` documentation with usage examples.
- **Modular Package Structure (`src/pdf2audiobook`):** Separated concerns into `pdf.py` (extraction & decryption), `tts.py` (Piper TTS & Meta MMS synthesis), and `translator.py` (MarianMT with technical term preservation).
- **English Speech Synthesis (`mms-en`):** Support for English audiobooks using `Baghdad99/english_voice_tts` via VITS.
- **English-to-Portuguese Translation (`translate`):** MarianMT neural machine translation (`Helsinki-NLP/opus-mt-tc-big-en-pt`) with customizable term preservation (`TermPreserver`) for tech/coding acronyms.
- **End-to-End Pipeline (`pipeline`):** One-step translation and European Portuguese audio synthesis from English PDFs.
- **REUSE 3.3 Compliance:** Full compliance with the Free Software Foundation Europe (FSFE) REUSE standard (`LICENSES/MIT.txt`, `.reuse/dep5`, and SPDX headers across all repository files).

## [1.0.0] - 2026-09-04

### Added
- **Initial project scaffolding:** Complete PDF-to-audiobook pipeline using Hugging Face Text-to-Speech models.
- **European Portuguese support (`pdf2audiobook_ptpt.py`):**
  - Integrated [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) engine.
  - Configured automated model download for `rhasspy/piper-voices` ([pt_PT-tugão-medium](https://huggingface.co/rhasspy/piper-voices)).
  - Direct continuous audio streaming using `voice.synthesize_wav()` to eliminate audio chunking.
  - CUDA GPU acceleration via `onnxruntime-gpu`.
- **Multilingual / Brazilian Portuguese support (`pdf2audiobook.py`):**
  - Integrated Meta's MMS model ([facebook/mms-tts-por](https://huggingface.co/facebook/mms-tts-por)) via Hugging Face `transformers` (`VitsModel`, `VitsTokenizer`).
  - Implemented sentence chunking algorithm to preserve token and GPU memory boundaries.
  - Corrected NumPy 1D audio waveform concatenation for seamless WAV assembly.
- **PDF Extraction & Decryption:**
  - Added PDF text extraction via `PyPDF2`.
  - Added AES decryption support via `pycryptodome` for official documents (e.g. Diário da República, academic regulations).
- **Documentation & Compliance:**
  - Comprehensive `README.md` with usage, setup, and troubleshooting instructions.
  - AI Transparency and Disclosure statement (EU AI Act compliance).
  - Open-source model provenance and Hugging Face model card documentation.
  - `AGENTS.md` context and architecture specification for AI agent pair programming.
  - MIT `LICENSE` declaration.
