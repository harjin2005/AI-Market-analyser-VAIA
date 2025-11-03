"""Document processing and chunking utilities."""
import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import config

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

class DocumentProcessor:
    """Handles document loading and chunking."""
    
    def __init__(self, chunk_size=None, chunk_overlap=None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def process_document(self, file_path: str) -> List[Document]:
        _, ext = os.path.splitext(file_path)
        text = ""

        if ext.lower() == ".pdf":
            if PyPDF2 is None:
                raise ImportError("PyPDF2 is not installed. Please run: pip install PyPDF2")
            try:
                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
            except Exception as e:
                print(f"Error reading PDF {file_path}: {e}")
                return []
        elif ext.lower() == ".txt":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print(f"Error reading TXT {file_path}: {e}")
                return []
        else:
            print(f"Unsupported file type: {ext}")
            return []

        if not text.strip():
            print(f"No text extracted from document: {file_path}")
            return []

        doc = Document(page_content=text, metadata={"source": file_path})
        chunks = self.text_splitter.split_documents([doc])
        
        chunks = [chunk for chunk in chunks if chunk.page_content.strip()]
        
        print(f"✓ Loaded document from: {file_path}")
        print(f"✓ Created {len(chunks)} chunks")
        print(f"✓ Chunk size: {self.chunk_size}, Overlap: {self.chunk_overlap}")
        
        print(f"[DEBUG] extracted text first 200 chars: {text[:200]}")
        print(f"[DEBUG] Number of chunks after split/filter: {len(chunks)}")
        for i, chunk in enumerate(chunks[:3]):  # Only show first few
            print(f"[DEBUG] chunk {i}: {chunk.page_content[:60]}")
        
        return chunks