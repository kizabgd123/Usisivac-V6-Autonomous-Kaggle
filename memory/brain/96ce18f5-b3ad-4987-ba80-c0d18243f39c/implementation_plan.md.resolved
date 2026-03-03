# Implementation Plan - Scanned PDF to Text (OCR)

This plan outlines the steps to convert a scanned PDF (images only) into a searchable text file using Tesseract OCR.

## Proposed Changes

### Environment Setup
- Install system dependencies: `tesseract-ocr`, `libtesseract-dev`, `poppler-utils`.
- Install Python libraries: `pytesseract`, `pdf2image`, `Pillow`.

### [NEW] [pdf_to_text.py](file:///home/kizabgd/Desktop/Istrazivanje/scripts/pdf_to_text.py)
Create a utility script to handle multi-page OCR.
- **Input**: Path to PDF file.
- **Logic**:
    1. Use `pdf2image` to convert each page into a high-DPI image.
    2. Iterate through images and use `pytesseract.image_to_string`.
    3. Aggregate all text with page separators.
- **Output**: A text file with the same basename as the PDF.

## Verification Plan

### Automated Tests
Run the script on the target file and check if the output file exists and is non-empty.
```bash
python3 scripts/pdf_to_text.py /home/kizabgd/Desktop/Istrazivanje/scans/scan_20260224_175019.pdf
```

### Manual Verification
- View the generated `.txt` file using `head` or `cat`.
- Check for common OCR errors or language issues (the user's previous requests were in Serbian, so I should ensure Tesseract supports Serbian if necessary).
