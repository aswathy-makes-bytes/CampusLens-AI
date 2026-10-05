import fitz
import os

PDF_FOLDER = "documents"

for filename in os.listdir(PDF_FOLDER):

    if filename.lower().endswith(".pdf"):

        pdf_path = os.path.join(PDF_FOLDER, filename)

        print(f"\n📄 Reading: {filename}")

        document = fitz.open(pdf_path)

        for page_number, page in enumerate(document, start=1):

            text = page.get_text()

            print(f"\n--- Page {page_number} ---")
            print(text[:1000])

        document.close()