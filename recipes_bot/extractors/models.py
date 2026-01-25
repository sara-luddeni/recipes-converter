"""Data models for text extraction from videos."""

from dataclasses import dataclass
from typing import List, Literal, Optional

Source = Literal["audio", "ocr"]


@dataclass
class TextChunk:
    """A chunk of text extracted from a video with timestamp information."""
    
    source: Source
    start_s: float
    end_s: float
    text: str
    confidence: Optional[float] = None


@dataclass
class Recipe:
    """Structured recipe information extracted from transcript."""
    
    title: str
    ingredients: List[str]
    instructions: List[str]
