import os
from re import T
import pandas as pd
from openpyxl import load_workbook

# Test 1
def extract_tables_from_excel(file_path):
    
    excel_data = pd.read_excel(file_path, sheet_name=None)
    
    tables = {}
    for sheet_name, data in excel_data.items():
        tables[sheet_name] = data
    
    for table_name, table_data in tables.items():
        print(f"Table: {table_name}")
        print(table_data)
    return tables

# Test 2
def extract_xls_2(filename):
    df = pd.read_excel(filename, sheet_name = "SalesOrders", engine='openpyxl')

    header = df.head()
    print(header)

# Test 3 (Final version)
def extract_xls_3(filename):
    wb = load_workbook(filename)
    ws = wb["SalesOrders"]

    table_contents = []
    for table_name, data in ws.tables.items():
        data = ws[data]
        content = [[cell.value for cell in ent] for ent in data]
        

        header = [content.replace(" ", "_") for content in content[0]]
        for content_chunk in content:
            for i in range(len(content_chunk)):
                content_chunk[i] = str(content_chunk[i])
            
            print(content_chunk)
        chunks = []
        for i in range(1, len(content), 10):
            if i == 0:
                continue
            current_chunk = content[i:i+10]
            combinded_chunk = [header] + current_chunk
            chunks.append(combinded_chunk)
        

        chunk_strings = []
        for chunk in chunks:
            chunk_strings.append("| "+" | \n | ".join([" | ".join(row) for row in chunk]))

        table_contents.append(chunk_strings)

    return table_contents

file_path = './SampleData_3.xlsx'
current_dir = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(current_dir, file_path)
#tables = extract_tables_from_excel(file_path)
#tables = extract_xls_2(absolute_path)
extract_xls_3(absolute_path)
