"""Audio extraction and transcription from video files."""

import subprocess
from pathlib import Path
from typing import List
import tempfile

import whisper

from .models import TextChunk

# Cache the Whisper model after first load
_model = None


def get_whisper_model():
    """Get or load the Whisper model (cached after first load)."""
    global _model
    if _model is None:
        _model = whisper.load_model("small")
    return _model


def extract_audio_wav(video_path: str, output_path: str) -> str:
    """
    Extracts the audio track from a video file and saves it as a WAV file in 16 kHz mono PCM format.

    Args:
        video_path (str): Path to the input video file (e.g., .mp4).
        output_path (str): Path for the output WAV file. (This argument is ignored; output will always be next to the video with the same name and '.wav' extension.)

    Returns:
        str: Path to the extracted WAV audio file.

    Raises:
        FileNotFoundError: If the input video file or ffmpeg is not found.
        RuntimeError: If ffmpeg fails to extract the audio or times out.
    """
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True,
            timeout=5,
        )
    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
    ) as e:
        raise FileNotFoundError(
            "ffmpeg is required but not found. Please install ffmpeg: "
            "https://ffmpeg.org/download.html"
        ) from e

    # Extract audio: 16kHz mono WAV (optimal for Whisper)
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file
        "-i",
        str(video),
        "-vn",  # No video
        "-acodec",
        "pcm_s16le",  # PCM 16-bit little-endian
        "-ar",
        "16000",  # 16kHz sample rate
        "-ac",
        "1",  # Mono
        str(output_path),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            timeout=300,  # 5 minute timeout
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract audio from video: {e}") from e
    except subprocess.TimeoutExpired:
        raise RuntimeError("Audio extraction timed out") from TimeoutError

    return str(output_path)


def transcribe_to_chunks(video_path: str) -> List[TextChunk]:
    """
    Transcribe audio from video file and return timestamped text chunks.

    Args:
        video_path: Path to input video file (.mp4)

    Returns:
        List of TextChunk objects with transcribed text and timestamps

    Raises:
        FileNotFoundError: If video file or ffmpeg not found
        RuntimeError: If transcription fails
    """
    # Extract audio
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        audio_path = temp_audio.name
        extract_audio_wav(video_path, audio_path)

        try:
            # Load model (cached after first load)
            model = get_whisper_model()

            # Transcribe with segments
            result = model.transcribe(audio_path)

            # Convert segments to TextChunk objects
            chunks: List[TextChunk] = []
            for segment in result.get("segments", []):
                chunks.append(
                    TextChunk(
                        source="audio",
                        start_s=float(segment["start"]),
                        end_s=float(segment["end"]),
                        text=segment["text"].strip(),
                        confidence=None,  # Whisper doesn't provide segment-level confidence
                    )
                )

            return chunks

        except Exception as e:
            raise RuntimeError(f"Failed to transcribe audio: {e}") from e
        finally:
            # Clean up temporary audio file
            audio_file = Path(audio_path)
            if audio_file.exists() and audio_file != Path(video_path):
                try:
                    audio_file.unlink()
                except OSError:
                    pass  # Ignore cleanup errors


def transcribe(video_path: str) -> str:
    """
    Transcribe audio from video file and return full transcript as text.

    Args:
        video_path: Path to input video file (.mp4)

    Returns:
        Full transcript text as a single string

    Raises:
        FileNotFoundError: If video file or ffmpeg not found
        RuntimeError: If transcription fails
    """
    # Extract audio
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        audio_path = temp_audio.name
        extract_audio_wav(video_path, audio_path)

        try:
            # Load model (cached after first load)
            model = get_whisper_model()

            # Transcribe
            result = model.transcribe(audio_path)

            # Return full text
            return result.get("text", "").strip()

        except Exception as e:
            raise RuntimeError(f"Failed to transcribe audio: {e}") from e
        finally:
            # Clean up temporary audio file
            audio_file = Path(audio_path)
            if audio_file.exists() and audio_file != Path(video_path):
                try:
                    audio_file.unlink()
                except OSError:
                    pass  # Ignore cleanup errors
