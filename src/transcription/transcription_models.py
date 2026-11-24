
from dataclasses import dataclass, asdict
import json


@dataclass
class TranscriptionSegment:
    start: float
    end: float
    text: str
    confidence: float


@dataclass
class TranscriptionResult:
    audio_file: str
    language: str
    language_probability: float
    duration_seconds: float
    segments: list[TranscriptionSegment]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=4,
            ensure_ascii=False
        )
