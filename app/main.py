

from app.extractor import NewsMetadataExtractor
from app.airtable_client import AirtableClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
extractor = NewsMetadataExtractor()
airtable = AirtableClient()

class URLIn(BaseModel):
    url: str  # Changed from HttpUrl to str

@app.post("/extract")
def extract_and_store(url_in: URLIn):
    try:
        data = extractor.extract(url_in.url)
        airtable.add_article(data)
        return {"message": "Data extracted and stored successfully!", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
