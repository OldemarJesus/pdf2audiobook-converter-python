import torch
import PyPDF2
import scipy.io.wavfile
import numpy as np
from transformers import VitsTokenizer, VitsModel

# 1. Set up the GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 2. Load the Hugging Face Model and Tokenizer
model_id = "facebook/mms-tts-por"
tokenizer = VitsTokenizer.from_pretrained(model_id)
model = VitsModel.from_pretrained(model_id).to(device)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text

def chunk_text(text, max_chars=500):
    """Splits text into smaller chunks to prevent memory/token limits."""
    words = text.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        if len(current_chunk) + len(word) < max_chars:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
            
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# 3. Process the PDF
pdf_filename = "document.pdf" # Replace with your actual PDF path
full_text = extract_text_from_pdf(pdf_filename)

# 4. Convert Text to Speech in Chunks
text_chunks = chunk_text(full_text)
audio_pieces = []

print("Generating audio...")
model.eval()
with torch.no_grad():
    for i, chunk in enumerate(text_chunks):
        # Move tokenized inputs to your RTX 3060
        inputs = tokenizer(chunk, return_tensors="pt").to(device)
        
        # Generate the audio waveform
        outputs = model(**inputs)
        
        # Move the waveform back to CPU to save it
        waveform = outputs.waveform[0].cpu().numpy()
        audio_pieces.append(waveform)
        print(f"Processed chunk {i+1}/{len(text_chunks)}")

# 5. Concatenate and Save
final_audio = np.concatenate(audio_pieces) # Removed axis=1
sample_rate = model.config.sampling_rate
output_file = "portuguese_audiobook.wav"

# Removed [0] from final_audio since it's already a 1D array
scipy.io.wavfile.write(output_file, rate=sample_rate, data=final_audio) 
print(f"Audiobook successfully saved as {output_file}")
