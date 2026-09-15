#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Oldemar
# SPDX-License-Identifier: MIT

"""pdf2audiobook CLI — Unified entry point for PDF audio conversion and translation."""

import os
import sys
import argparse

# Add repository root to python path to allow direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="🎙️ pdf2audiobook-converter-python — Convert PDFs into high-quality spoken audiobooks and translate documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Utilities & Usage Examples:
-----------------------------------------------------------------------------------------------
1. European Portuguese pt-PT Audiobook (Piper TTS - tugão) [RECOMMENDED]:
   python main.py ptpt --pdf document.pdf --output pt_audiobook.wav
   python main.py ptpt --text translated_document_pt.txt --output pt_audiobook.wav

2. Portuguese Audiobook (Meta MMS):
   python main.py mms-pt --pdf document.pdf --output pt_audiobook.wav

3. English Audiobook (Meta MMS):
   python main.py mms-en --pdf document.pdf --output en_audiobook.wav

4. Translate English PDF to Portuguese (Preserving Technical Terms):
   python main.py translate --pdf document.pdf --output translated_document_pt.txt --terms Kubernetes PyTorch

5. End-to-End Pipeline (Translate English PDF -> pt-PT Audiobook):
   python main.py pipeline --pdf document.pdf --output-txt translated_pt.txt --output-audio pt_audiobook.wav
-----------------------------------------------------------------------------------------------
        """,
    )

    subparsers = parser.add_subparsers(
        title="Commands / Utilities",
        dest="command",
        metavar="<command>",
        required=True,
    )

    # -------------------------------------------------------------
    # 1. ptpt: European Portuguese (Piper TTS)
    # -------------------------------------------------------------
    p_ptpt = subparsers.add_parser(
        "ptpt",
        help="Convert PDF or text to European Portuguese (pt-PT) audio using Piper TTS (tugão).",
        description="Convert PDF or plain text to European Portuguese (pt-PT) audio using Piper TTS (tugão model on CUDA/CPU).",
    )
    p_ptpt.add_argument("--pdf", default="document.pdf", help="Path to input PDF file (default: document.pdf)")
    p_ptpt.add_argument("--text", default=None, help="Path to plain text file (takes priority over PDF if provided)")
    p_ptpt.add_argument("--output", default="portuguese_pt_audiobook.wav", help="Output WAV file name (default: portuguese_pt_audiobook.wav)")
    p_ptpt.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Inference device: 'cuda' or 'cpu' (default: auto-detect)")

    # -------------------------------------------------------------
    # 2. mms-pt: Portuguese (Meta MMS)
    # -------------------------------------------------------------
    p_mms_pt = subparsers.add_parser(
        "mms-pt",
        help="Convert PDF or text to Portuguese audio using Meta MMS (facebook/mms-tts-por).",
        description="Convert PDF or plain text to Portuguese speech using Meta MMS VITS model (facebook/mms-tts-por).",
    )
    p_mms_pt.add_argument("--pdf", default="document.pdf", help="Path to input PDF file (default: document.pdf)")
    p_mms_pt.add_argument("--text", default=None, help="Path to plain text file (takes priority over PDF if provided)")
    p_mms_pt.add_argument("--output", default="portuguese_audiobook.wav", help="Output WAV file name (default: portuguese_audiobook.wav)")
    p_mms_pt.add_argument("--chunk-size", type=int, default=450, help="Max character limit per chunk (default: 450)")
    p_mms_pt.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Inference device: 'cuda' or 'cpu' (default: auto-detect)")

    # -------------------------------------------------------------
    # 3. mms-en: English (Meta MMS)
    # -------------------------------------------------------------
    p_mms_en = subparsers.add_parser(
        "mms-en",
        help="Convert PDF or text to English audio using Meta MMS (Baghdad99/english_voice_tts).",
        description="Convert PDF or plain text to English speech using Meta MMS VITS model (Baghdad99/english_voice_tts).",
    )
    p_mms_en.add_argument("--pdf", default="document.pdf", help="Path to input PDF file (default: document.pdf)")
    p_mms_en.add_argument("--text", default=None, help="Path to plain text file (takes priority over PDF if provided)")
    p_mms_en.add_argument("--output", default="english_audiobook.wav", help="Output WAV file name (default: english_audiobook.wav)")
    p_mms_en.add_argument("--chunk-size", type=int, default=450, help="Max character limit per chunk (default: 450)")
    p_mms_en.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Inference device: 'cuda' or 'cpu' (default: auto-detect)")

    # -------------------------------------------------------------
    # 4. translate: English to Portuguese Translation
    # -------------------------------------------------------------
    p_trans = subparsers.add_parser(
        "translate",
        help="Translate English PDF or text to Portuguese, preserving key technical terms.",
        description="Translate English PDF/text to Portuguese using Helsinki-NLP/opus-mt-tc-big-en-pt while preserving technical terminology.",
    )
    p_trans.add_argument("--pdf", default="document.pdf", help="Path to input PDF file (default: document.pdf)")
    p_trans.add_argument("--text", default=None, help="Path to plain text file (takes priority over PDF if provided)")
    p_trans.add_argument("--output", default="translated_document_pt.txt", help="Output translated text file (default: translated_document_pt.txt)")
    p_trans.add_argument("--terms", nargs="*", default=None, help="Additional technical terms to preserve without translation")
    p_trans.add_argument("--batch-size", type=int, default=16, help="Sentence batch size for neural MT inference (default: 16)")
    p_trans.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Inference device: 'cuda' or 'cpu' (default: auto-detect)")

    # -------------------------------------------------------------
    # 5. pipeline: Translate English PDF -> pt-PT Audiobook WAV
    # -------------------------------------------------------------
    p_pipe = subparsers.add_parser(
        "pipeline",
        help="Full pipeline: Translate English PDF to Portuguese AND generate European Portuguese audio.",
        description="Translate an English PDF document into Portuguese with technical term preservation and immediately synthesize it into European Portuguese (pt-PT) audio.",
    )
    p_pipe.add_argument("--pdf", default="document.pdf", help="Path to input English PDF file (default: document.pdf)")
    p_pipe.add_argument("--output-txt", default="translated_document_pt.txt", help="Path to intermediate translated text file (default: translated_document_pt.txt)")
    p_pipe.add_argument("--output-audio", default="portuguese_pt_audiobook.wav", help="Path to final output WAV audiobook (default: portuguese_pt_audiobook.wav)")
    p_pipe.add_argument("--terms", nargs="*", default=None, help="Additional technical terms to preserve")
    p_pipe.add_argument("--device", choices=["cuda", "cpu"], default=None, help="Inference device: 'cuda' or 'cpu' (default: auto-detect)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Lazy import modules only when executing commands to make --help instant
    from src.pdf2audiobook.pdf import load_input_text

    try:
        if args.command == "ptpt":
            from src.pdf2audiobook.tts import synthesize_piper_ptpt
            text = load_input_text(pdf_path=args.pdf, text_path=args.text)
            synthesize_piper_ptpt(text=text, output_path=args.output, device=args.device)

        elif args.command == "mms-pt":
            from src.pdf2audiobook.tts import synthesize_vits_mms
            text = load_input_text(pdf_path=args.pdf, text_path=args.text)
            synthesize_vits_mms(
                text=text,
                model_id="facebook/mms-tts-por",
                output_path=args.output,
                device=args.device,
                chunk_size=args.chunk_size,
            )

        elif args.command == "mms-en":
            from src.pdf2audiobook.tts import synthesize_vits_mms
            text = load_input_text(pdf_path=args.pdf, text_path=args.text)
            synthesize_vits_mms(
                text=text,
                model_id="Baghdad99/english_voice_tts",
                output_path=args.output,
                device=args.device,
                chunk_size=args.chunk_size,
            )

        elif args.command == "translate":
            from src.pdf2audiobook.translator import translate_english_to_portuguese
            text = load_input_text(pdf_path=args.pdf, text_path=args.text)
            translate_english_to_portuguese(
                text=text,
                output_path=args.output,
                custom_terms=args.terms,
                device=args.device,
                batch_size=args.batch_size,
            )

        elif args.command == "pipeline":
            from src.pdf2audiobook.translator import translate_english_to_portuguese
            from src.pdf2audiobook.tts import synthesize_piper_ptpt

            print("=== Step 1/2: Extracting & Translating English PDF ===")
            text = load_input_text(pdf_path=args.pdf)
            translated_text = translate_english_to_portuguese(
                text=text,
                output_path=args.output_txt,
                custom_terms=args.terms,
                device=args.device,
            )

            print("\n=== Step 2/2: Synthesizing European Portuguese Audio ===")
            synthesize_piper_ptpt(
                text=translated_text,
                output_path=args.output_audio,
                device=args.device,
            )
            print(f"\n🎉 [PIPELINE COMPLETE] Audiobook ready at '{args.output_audio}'!")

    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
