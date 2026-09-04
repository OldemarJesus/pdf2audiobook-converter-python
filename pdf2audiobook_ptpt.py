import torch
import PyPDF2
import wave
from huggingface_hub import hf_hub_download
from piper.voice import PiperVoice

# 1. Automatically download the pt-PT (tugão) model files from Hugging Face
print("Downloading European Portuguese model...")
repo_id = "rhasspy/piper-voices"
model_file = hf_hub_download(repo_id=repo_id, filename="pt/pt_PT/tugão/medium/pt_PT-tugão-medium.onnx")
config_file = hf_hub_download(repo_id=repo_id, filename="pt/pt_PT/tugão/medium/pt_PT-tugão-medium.onnx.json")

# 2. Load Piper TTS onto your RTX 3060 (use_cuda=True)
print("Loading model onto GPU...")
device = "cuda" if torch.cuda.is_available() else "cpu"
use_gpu = device == "cuda"
voice = PiperVoice.load(model_file, config_path=config_file, use_cuda=use_gpu)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                # Replace newlines with spaces to help the TTS engine read smoothly
                text += extracted.replace('\n', ' ') + " "
    return text

# 3. Extract Text from PDF
pdf_filename = "document.pdf"
print(f"Extracting text from {pdf_filename}...")
full_text = extract_text_from_pdf(pdf_filename)

# 4. Generate the Audiobook
output_file = "portuguese_pt_audiobook.wav"
print("Generating audio on GPU...")

# Use synthesize_wav to write the generated audio directly to the file
with wave.open(output_file, 'wb') as wav:
    voice.synthesize_wav(full_text, wav)

print(f"Audiobook successfully saved as {output_file}!")
