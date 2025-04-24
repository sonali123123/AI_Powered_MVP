import os
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




class AirtableClient:
    def __init__(self):
        token = os.getenv("AIRTABLE_TOKEN")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_TABLE", "Articles")
        if not token or not base_id:
            raise RuntimeError("Missing Airtable environment variables!")
        self.table = Table(token, base_id, table_name)

    def add_article(self, record: dict):
        """
        record format:
        {
            'headline': 'Some headline',
            'date': '2025-04-24T11:54:19+00:00',
            'country': 'India',
            'category': 'Politics'
        }
        """
        airtable_record = {
            "Headline": record["headline"],
            "Date": record["date"],
            "Country": record["country"] or "",
            "Category": record["category"]
        }
        self.table.create(airtable_record)
