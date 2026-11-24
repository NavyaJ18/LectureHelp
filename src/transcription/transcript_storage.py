
import json
import math
from pathlib import Path

from src.transcription.transcription_models import (
    TranscriptionSegment,
    TranscriptionResult,
)


def _validate_number(value, field_name, minimum=None, maximum=None):
    """Validate a finite numeric value and optional bounds."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number.")

    if not math.isfinite(value):
        raise ValueError(f"{field_name} must be finite.")

    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}.")

    if maximum is not None and value > maximum:
        raise ValueError(f"{field_name} must not exceed {maximum}.")


def _validate_result(result):
    """Validate a transcription result before saving or returning it."""

    if not isinstance(result, TranscriptionResult):
        raise ValueError("Expected a TranscriptionResult object.")

    if not isinstance(result.audio_file, str) or not result.audio_file.strip():
        raise ValueError("Audio file name must be a non-empty string.")

    if not isinstance(result.language, str) or not result.language.strip():
        raise ValueError("Language must be a non-empty string.")

    _validate_number(
        result.language_probability,
        "Language probability",
        minimum=0,
        maximum=1,
    )

    _validate_number(
        result.duration_seconds,
        "Duration",
        minimum=0,
    )

    if result.duration_seconds == 0:
        raise ValueError("Duration must be greater than zero.")

    if not isinstance(result.segments, list):
        raise ValueError("Segments must be a list.")

    for index, segment in enumerate(result.segments):
        if not isinstance(segment, TranscriptionSegment):
            raise ValueError(f"Segment {index} has an invalid type.")

        _validate_number(segment.start, f"Segment {index} start", minimum=0)
        _validate_number(segment.end, f"Segment {index} end", minimum=0)
        _validate_number(
            segment.confidence,
            f"Segment {index} confidence",
            minimum=0,
            maximum=1,
        )

        if segment.end < segment.start:
            raise ValueError(f"Segment {index} ends before it starts.")

        if not isinstance(segment.text, str) or not segment.text.strip():
            raise ValueError(f"Segment {index} has empty text.")


def save_transcription(
    result: TranscriptionResult,
    output_dir: str = "data/transcripts",
) -> Path:
    """Save a transcription result as a JSON file."""

    _validate_result(result)

    output_directory = Path(output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    audio_stem = Path(result.audio_file).stem

    if not audio_stem:
        raise ValueError("Cannot generate a filename from the audio file.")

    output_path = output_directory / f"{audio_stem}_transcription.json"
    temporary_path = output_path.with_suffix(".tmp")

    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump(
                result.to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
                allow_nan=False,
            )

        temporary_path.replace(output_path)

    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        raise

    return output_path


def load_transcription(transcript_path: str) -> TranscriptionResult:
    """Load and validate a JSON transcription file."""

    file_path = Path(transcript_path).expanduser()

    if not file_path.exists():
        raise FileNotFoundError(
            f"Transcript file not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError("Transcript path must point to a file.")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid transcript JSON: {error}"
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            "Transcript file must contain valid UTF-8 text."
        ) from error

    if not isinstance(data, dict):
        raise ValueError("Transcript JSON must contain an object.")

    required_fields = {
        "audio_file",
        "language",
        "language_probability",
        "duration_seconds",
        "segments",
    }

    if set(data.keys()) != required_fields:
        raise ValueError("Transcript JSON has missing or unexpected fields.")

    if not isinstance(data["segments"], list):
        raise ValueError("Transcript segments must be a list.")

    segments = []

    for index, segment_data in enumerate(data["segments"]):
        if not isinstance(segment_data, dict):
            raise ValueError(f"Segment {index} must be an object.")

        if set(segment_data.keys()) != {"start", "end", "text", "confidence"}:
            raise ValueError(f"Segment {index} has invalid fields.")

        segments.append(
            TranscriptionSegment(
                start=segment_data["start"],
                end=segment_data["end"],
                text=segment_data["text"],
                confidence=segment_data["confidence"],
            )
        )

    result = TranscriptionResult(
        audio_file=data["audio_file"],
        language=data["language"],
        language_probability=data["language_probability"],
        duration_seconds=data["duration_seconds"],
        segments=segments,
    )

    _validate_result(result)

    return result
