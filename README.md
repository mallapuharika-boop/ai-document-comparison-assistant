# AI Document Comparison Assistant

## Overview
The AI Document Comparison Assistant is a Python-based web application that compares two PDF documents using Google's Gemini AI. It identifies similarities, differences, key details, and generates a downloadable comparison report.

## Features
- Upload two PDF documents.
- Extract text from PDF files.
- Compare documents using Gemini AI.
- Display summaries, similarities, and differences.
- Highlight important details.
- Download the comparison report as a DOCX file.

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- PyPDF
- Python-docx

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mallapuharika-boop/ai-document-comparison-assistant.git
   ```

2. Open the project folder:
   ```bash
   cd ai-document-comparison-assistant
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project folder and add your own Gemini API key:
   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Security
Keep your API key private. Never commit your `.env` file or expose your API key publicly.

## Limitations
Comparison quality depends on the extracted PDF text and the AI model's response. Scanned PDFs may require OCR support.
