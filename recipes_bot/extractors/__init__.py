"""Text extraction from videos (audio transcription, OCR, etc.)."""

from .audio import transcribe, transcribe_to_chunks
from .models import Source, TextChunk

__all__ = ["TextChunk", "Source", "transcribe", "transcribe_to_chunks"]
