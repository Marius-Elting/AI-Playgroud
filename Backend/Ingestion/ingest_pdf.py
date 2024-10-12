import fitz

class PdfIngestion:
    def ingest_pdf(self, document_bytes):
        
        doc = fitz.open(stream=document_bytes, filetype="pdf")
        chunks = []
        for page in doc:
            text = page.get_text()
            chunks.extend(self.chunk_text(text))
        return chunks

    def chunk_text(self, text):
        max_chunk_size = 1500
        chunks = []
        section_delimiter = "\n"  # Assuming sections are separated by two newlines

        while len(text) > max_chunk_size:
            next_section_index = text.find(section_delimiter, max_chunk_size)
            if next_section_index == -1:
                break  # No more sections found, exit the loop
            chunk = text[:next_section_index + len(section_delimiter)]
            chunks.append(chunk)
            text = text[next_section_index + len(section_delimiter):]

        chunks.append(text)
        return chunks