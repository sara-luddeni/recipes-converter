"""Tests for audio extraction and transcription."""

import pathlib
import shutil
import subprocess
import tempfile

import pytest

from recipes_bot.extractors.audio import extract_audio_wav, transcribe, transcribe_to_chunks
from recipes_bot.extractors.models import TextChunk

def test_ffmpeg_available():
    """Test that ffmpeg is available."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        raise RuntimeError("ffmpeg not available")

def test_extract_audio_wav():
    """Test that audio extraction produces a valid WAV file."""

    fixture_video = pathlib.Path(__file__).parent.parent / "fixture/test_video.mp4"
    assert fixture_video.exists(), f"Fixture not found! as {str(fixture_video)}"

    
    with tempfile.TemporaryDirectory() as tmpdir:
        
        audio_path = extract_audio_wav(str(fixture_video), tmpdir+"/audio.wav")
        assert pathlib.Path(audio_path).exists(), "Audio file should exist"
        
        with open(audio_path, 'rb') as f:
            header = f.read(12)
            assert header[0:4] == b'RIFF', "Should be a valid WAV file (RIFF signature)"
            assert header[8:12] == b'WAVE', "Should be a valid WAV file (WAVE signature)"
        
        pathlib.Path(audio_path).unlink(missing_ok=True)


def test_extract_audio_wav_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        extract_audio_wav("nonexistent_video.mp4", "/dev/null")


def test_transcribe_to_chunks():
    """Test that transcription returns valid chunks with timestamps."""

    fixture_video = pathlib.Path(__file__).parent.parent / "fixture/test_video.mp4"
    with tempfile.TemporaryDirectory() as tmpdir:

        chunks = transcribe_to_chunks(str(fixture_video))
        
        assert isinstance(chunks, list), "Should return a list"
        assert len(chunks) > 0, "Should return at least one chunk"
        
        for chunk in chunks:
            assert isinstance(chunk, TextChunk), "Each item should be a TextChunk"
            assert chunk.source == "audio", "Source should be 'audio'"
            assert isinstance(chunk.start_s, (int, float)), "start_s should be a number"
            assert isinstance(chunk.end_s, (int, float)), "end_s should be a number"
            assert chunk.start_s >= 0, "start_s should be non-negative"
            assert chunk.end_s > chunk.start_s, "end_s should be greater than start_s"
            assert isinstance(chunk.text, str), "text should be a string"
            assert len(chunk.text.strip()) > 0, "text should not be empty"
        
        # Verify timestamps are sequential
        for i in range(1, len(chunks)):
            assert chunks[i].start_s >= chunks[i-1].start_s, "Chunks should be in chronological order"
            # Chunks may overlap slightly, but generally end before next starts
            # (Whisper segments can have small overlaps, so we're lenient here)


def test_transcribe_to_chunks_nonexistent_file():
    """Test that transcribe_to_chunks raises error for nonexistent file."""
    with pytest.raises(FileNotFoundError):
        transcribe_to_chunks("nonexistent_video.mp4")


def test_transcribe():
    """Test that transcription returns valid text string."""
    fixture_video = pathlib.Path(__file__).parent.parent / "fixture/test_video.mp4"

    with tempfile.TemporaryDirectory() as tmpdir:

        transcript = transcribe(str(fixture_video))
        assert isinstance(transcript, str), "Should return a string"
        assert len(transcript.strip()) > 0, "Transcript should not be empty"


def test_transcribe_nonexistent_file():
    """Test that transcribe raises error for nonexistent file."""
    with pytest.raises(FileNotFoundError):
        transcribe("nonexistent_video.mp4")
