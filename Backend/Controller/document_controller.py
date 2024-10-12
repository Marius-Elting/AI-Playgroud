from Services import QdrantService
from Ingestion.ingest_xls import ExcelIngestion


class DocumentController:

    def __init__(self):
        pass

    def ingest_document(self, document):
        excel_ingestion = ExcelIngestion()
        qdrant_service = QdrantService()
        tables = excel_ingestion.extract_tables(document)
        if tables == None:
            return "No tables found"
        for table in tables:
            qdrant_service.insert_vectors(table)
        print(tables)
        return tables