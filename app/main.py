
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.services.document import extract_text_from_file
from pypdf.errors import PdfReadError


app = FastAPI(title="AI Recruitment Assistant")


@app.get("/")
def root():
    return {"message": "AI Recruitment Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    file_extension = file.filename.lower().rsplit(".", 1)[-1]

    if file_extension not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if file_extension == "pdf" and not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    try:
        extracted_text = extract_text_from_file(
            file_content,
            file_extension
        )
    except (ValueError, UnicodeDecodeError, PdfReadError) as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not extract text: {str(error)}"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the uploaded file"
        )

    return {
        "filename": file.filename,
        "file_type": file_extension,
        "file_size": len(file_content),
        "extracted_text": extracted_text,
        "character_count": len(extracted_text),
        "message": "File uploaded and processed successfully"
    }
