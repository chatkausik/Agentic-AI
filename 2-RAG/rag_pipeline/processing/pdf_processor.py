import os
import logging
from typing import List
from datetime import datetime
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import camelot  # for table extraction

from .chunking import SemanticChunker
from ..models.data_models import DocumentChunk

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Comprehensive PDF processing with text, image, and table extraction"""
    
    def __init__(self):
        self.chunker = SemanticChunker()
        
    def extract_text_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF"""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_images(self, pdf_path: str) -> List[str]:
        """Extract and OCR images from PDF"""
        doc = fitz.open(pdf_path)
        image_texts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_data = pix.tobytes("png")
                    # Save temporarily and OCR
                    temp_path = f"temp_img_{page_num}_{img_index}.png"
                    with open(temp_path, "wb") as f:
                        f.write(img_data)
                    
                    try:
                        ocr_text = pytesseract.image_to_string(temp_path)
                        if ocr_text.strip():
                            image_texts.append(ocr_text)
                    except:
                        pass
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                
                pix = None
        
        doc.close()
        return image_texts
    
    def extract_tables(self, pdf_path: str) -> List[str]:
        """Extract tables using camelot"""
        table_texts = []
        try:
            tables = camelot.read_pdf(pdf_path, pages='all')
            for table in tables:
                df = table.df
                table_text = df.to_string(index=False)
                table_texts.append(table_text)
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
        
        return table_texts
    
    def process_pdf(self, pdf_path: str) -> List[DocumentChunk]:
        """Process PDF and return semantic chunks"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract all content
        text_content = self.extract_text_pymupdf(pdf_path)
        image_texts = self.extract_images(pdf_path)
        table_texts = self.extract_tables(pdf_path)
        
        # Combine all content
        all_content = text_content + "\n".join(image_texts) + "\n".join(table_texts)
        
        # Perform semantic chunking
        chunks = self.chunker.chunk_text(all_content)
        
        # Create DocumentChunk objects
        document_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk = DocumentChunk(
                text=chunk_text,
                metadata={
                    "source": pdf_path,
                    "chunk_index": i,
                    "timestamp": datetime.now().isoformat()
                },
                chunk_id=f"{os.path.basename(pdf_path)}_{i}"
            )
            document_chunks.append(chunk)
        
        logger.info(f"Created {len(document_chunks)} semantic chunks")
        return document_chunks