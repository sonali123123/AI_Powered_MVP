"""
Article → {headline, date, country, category}
All heavy lifting lives here so FastAPI & Streamlit stay thin.
"""
from __future__ import annotations

from newspaper import Article
import spacy, pycountry
from transformers import pipeline
import torch
from datetime import datetime


class NewsMetadataExtractor:
    """Scrape & enrich a single news-article URL."""

    def __init__(
        self,
        labels: list[str] | None = None,
        spacy_model: str = "en_core_web_lg",
    ):
        # ↓ load NLP assets once – they stay in RAM across requests
        self.nlp = spacy.load(spacy_model)
        self.labels = labels or ["Trade", "Economy", "Politics", "Tech", "Sports"]
        self.classifier = pipeline(
            task="zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1,
        )

    # -------------  public single-call method  -------------
    def extract(self, url: str) -> dict:
        meta = self._fetch_article(url)
        meta["country"]  = self._detect_country(meta["text"])
        meta["category"] = self._classify(meta["text"])
        # Convert datetime to ISO 8601 string if date exists
        if isinstance(meta["date"], datetime):
            meta["date"] = meta["date"].isoformat()
        return {k: meta[k] for k in ["headline", "date", "country", "category"]}

    # -------------  internals  -------------
    @staticmethod
    def _fetch_article(url: str) -> dict:
        art = Article(url)
        art.download();  art.parse()
        return {"headline": art.title,
                "date": art.publish_date,
                "text": art.text}

    def _detect_country(self, text: str) -> str | None:
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                try:
                    return pycountry.countries.lookup(ent.text).name
                except LookupError:
                    continue
        return None

    def _classify(self, text: str) -> str:
        # clip to first 512 chars for speed
        out = self.classifier(text[:512], self.labels, multi_label=False)
        return out["labels"][0]
