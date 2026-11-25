"""Data models used to represent speech transcription results."""

from dataclasses import dataclass, asdict
import json


@dataclass
class TranscriptionSegment:
    """Represent one timestamped segment of a transcript."""

    start: float
    end: float
    text: str
    confidence: float


@dataclass
class TranscriptionResult:
    """Store the complete transcription output for an audio file."""

    audio_file: str
    language: str
    language_probability: float
    duration_seconds: float
    segments: list[TranscriptionSegment]

    def to_dict(self) -> dict:
        """Convert the transcription result into a dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize the transcription result as formatted JSON."""
        return json.dumps(
            self.to_dict(),
            indent=4,
            ensure_ascii=False
        )