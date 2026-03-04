from flask import Flask, render_template, request
import pdfplumber
from docx import Document
from summarizer import summarize_text

app = Flask(__name__)

def extract_text_from_pdf(file_stream) -> str:
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text)
    return "\n".join(text_parts)

def extract_text_from_docx(file_stream) -> str:
    doc = Document(file_stream)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    error = ""

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            error = "Please upload a PDF or DOCX file."
            return render_template("index.html", summary=summary, error=error)

        filename = file.filename.lower()

        try:
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file)
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(file)
            else:
                error = "Unsupported file type. Please upload .pdf or .docx"
                return render_template("index.html", summary=summary, error=error)

            if len(text.strip()) < 50:
                error = "The document text is too short or could not be extracted."
            else:
                summary = summarize_text(text, n_sentences=4)

        except Exception as e:
            error = f"Error while processing the file: {e}"

    return render_template("index.html", summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
