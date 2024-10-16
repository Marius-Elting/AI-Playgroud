from typing import Any, Literal
from Ingestion.ingest_pdf import PdfIngestion
from Services import QdrantService
from Ingestion.ingest_xls import ExcelIngestion


class DocumentController:

    def __init__(self):
        pass

    def ingest_excel(self, document) -> list[Any] | Literal['No tables found']:
        excel_ingestion = ExcelIngestion()
        qdrant_service = QdrantService()
        tables: list[Any] = excel_ingestion.extract_tables(file=document)
        if tables == None:
            return "No tables found"
        for table in tables:
            qdrant_service.insert_vectors(content=table, collection_name="exceldocuments")
        print(tables)
        return tables
    
    def ingest_pdf(self, document) -> None:
        pdf_ingestion = PdfIngestion()
        qdrant_service = QdrantService()
        chunks: list[Any] = pdf_ingestion.ingest_pdf(document_bytes=document)
        if chunks == None:
            return "No chunks found"
        qdrant_service.insert_vectors(content=chunks, collection_name="pdfdocuments")
        print(chunks)
        pass