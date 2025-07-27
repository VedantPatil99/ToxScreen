from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import pandas as pd
from io import BytesIO
from utils.perspective import analyze_single_text, analyze_texts
from utils.report_generator import generate_report_zip

app = FastAPI()

class TextPayload(BaseModel):
    text: str

@app.post("/analyze-text/")
def analyze_text(payload: TextPayload):
    return analyze_single_text(payload.text)

@app.post("/analyze-excel/")
async def analyze_excel(file: UploadFile = File(...)):
    input_bytes = await file.read()
    df = pd.read_excel(BytesIO(input_bytes))

    result_df = analyze_texts(df)
    zip_bytes = generate_report_zip(result_df)

    return StreamingResponse(BytesIO(zip_bytes), media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=toxicity_output.zip"
    })