from Ingestion.ingest_pdf import PdfIngestion
from Services import QdrantService
from Ingestion.ingest_xls import ExcelIngestion


class DocumentController:

    def __init__(self):
        pass

    def ingest_excel(self, document):
        excel_ingestion = ExcelIngestion()
        qdrant_service = QdrantService()
        tables = excel_ingestion.extract_tables(document)
        if tables == None:
            return "No tables found"
        for table in tables:
            qdrant_service.insert_vectors(table, "exceldocuments")
        print(tables)
        return tables
    
    def ingest_pdf(self, document):
        pdf_ingestion = PdfIngestion()
        qdrant_service = QdrantService()
        chunks = pdf_ingestion.ingest_pdf(document)
        if chunks == None:
            return "No chunks found"
        qdrant_service.insert_vectors(chunks, "pdfdocuments")
        print(chunks)
        pass