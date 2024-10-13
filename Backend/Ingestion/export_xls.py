import io
from fastapi.responses import StreamingResponse
import pandas as pd

class ExcelExporter:

    def export_data_to_excel(self, data) -> StreamingResponse:
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        
        return  StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=output.xlsx"})
