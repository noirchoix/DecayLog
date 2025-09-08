from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import PyPDF2
import tempfile
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from docx import Document
from reportlab.pdfgen import canvas
from pydub import AudioSegment
from pydub.utils import which
from typing import Optional, List

# === Configure ffmpeg/ffprobe paths ===
ffmpeg_path = which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
ffprobe_path = which("ffprobe") or r"C:\ffmpeg\bin\ffprobe.exe"

os.environ["FFMPEG_BINARY"] = ffmpeg_path
os.environ["FFPROBE_BINARY"] = ffprobe_path

app = FastAPI()

# === Middleware for CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Mount static for audio files ===
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# === Helpers ===
def split_text_safe(text: str, limit: int = 250) -> List[str]:
    """Split text into chunks under `limit` characters, preserving word boundaries."""
    words = text.split()
    chunks, current = [], ""

    for word in words:
        # +1 for the space when joining
        if len(current) + len(word) + 1 <= limit:
            current += (" " if current else "") + word
        else:
            chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks


def text_to_audio(text: str, out_path: Optional[str] = None) -> str:
    """
    Convert text (any length) to speech and save as MP3.
    Splits text safely into ≤250 char chunks and concatenates audio.
    """
    if not text.strip():
        raise ValueError("Text for audio conversion is empty.")

    # Split safely
    chunks = split_text_safe(text, limit=250)
    print(f"Splitting text into {len(chunks)} chunks.")

    tmp_files: list[str] = []

    try:
        # Generate per-chunk audio files
        for i, chunk in enumerate(chunks):
            tts = gTTS(text=chunk, lang="en", tld="com", slow=False)

            # Create temp file, close handle immediately
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name

            tts.save(tmp_path)
            tmp_files.append(tmp_path)
            print(f"Chunk {i+1}: {len(chunk)} chars saved => {tmp_path}")

        # Concatenate with pydub
        combined = AudioSegment.empty()
        for f in tmp_files:
            combined += AudioSegment.from_mp3(f)

        # Save final output
        if not out_path:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_final:
                out_path = tmp_final.name

        combined.export(out_path, format="mp3")
        print(f"Final audio file => {out_path}")

        return out_path

    finally:
        # Cleanup temp chunk files, even on error
        for f in tmp_files:
            try:
                os.remove(f)
            except PermissionError:
                print(f"Warning: could not remove {f}, file still in use.")

# === Endpoints ===
@app.post("/text-to-audio")
async def text_to_audio_endpoint(content: str = Form(...)):
    """Convert plain text to audio."""
    audio_path = text_to_audio(content)
    return FileResponse(audio_path, media_type="audio/mpeg", filename="labnotes.mp3")


@app.post("/pdf-to-audio")
async def pdf_to_audio(file: UploadFile = File(...), merge: str = Form("true")):
    """Convert uploaded PDF to audio (split by page, with optional merge)."""
    merge_bool = merge.lower() == "true"

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name

    reader = PyPDF2.PdfReader(pdf_path)
    chunks = [(i, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    chunks = [(i, text.strip()) for i, text in chunks if text.strip()]

    if not chunks:
        return JSONResponse({"error": "No text could be extracted from the PDF."}, status_code=400)

    base_id = uuid.uuid4().hex
    file_urls = []
    audio_segments = []

    # print number of chunks
    print(f"Number of text chunks (pages with text): {len(chunks)}")

    # Generate per-page audio
    for i, text in chunks:
        chunk_path = f"static/{base_id}_page{i+1}.mp3"
        text_to_audio(text, chunk_path)
        print(f"Generated audio for page {i+1}: {chunk_path}")
        file_urls.append(f"/static/{base_id}_page{i+1}.mp3")
        audio_segments.append(AudioSegment.from_mp3(chunk_path))

    os.remove(pdf_path)

    # Merge into single file if requested
    if merge_bool and audio_segments:
        final_audio = audio_segments[0]
        for seg in audio_segments[1:]:
            final_audio += seg
        merged_path = f"static/{base_id}_merged.mp3"
        final_audio.export(merged_path, format="mp3")
        return {
            "mode": "merged",
            "url": f"/static/{base_id}_merged.mp3",
            "files": file_urls,
        }

    return {"mode": "split", "files": file_urls}


@app.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    """Convert uploaded Word document to PDF."""
    if not file or not file.filename:
        return {"error": "No file uploaded"}

    filename = file.filename or ""
    if not filename.lower().endswith(".docx"):
        return {"error": "Please upload a .docx file"}

    # Save uploaded file temporarily
    temp_docx = f"temp_{file.filename}"
    with open(temp_docx, "wb") as f:
        f.write(await file.read())

    # Load DOCX
    doc = Document(temp_docx)

    # Convert to PDF
    pdf_filename = temp_docx.replace(".docx", ".pdf")
    c = canvas.Canvas(pdf_filename)
    y = 800  # start position for writing

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            c.drawString(50, y, text)
            y -= 20
            if y < 50:  # start new page if too low
                c.showPage()
                y = 800

    c.save()

    # Cleanup temp docx
    os.remove(temp_docx)

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)
