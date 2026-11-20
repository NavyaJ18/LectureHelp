
from dataclasses import dataclass
from pathlib import Path

from mutagen import File as MutagenFile

from src.audio.audio_validator import validate_audio_file


@dataclass
class AudioMetadata:
    """Stores technical information about an audio file."""

    file_name: str
    format: str
    duration_seconds: float
    sample_rate: int
    channels: int
    bitrate: int | None


def extract_audio_metadata(audio_path: str) -> AudioMetadata:
    """
    Extract technical metadata from an audio file.

    Returns:
        AudioMetadata: Information about the recording.
    """

    # First validate the input file.
    file_path = validate_audio_file(audio_path)

    # Read audio metadata using Mutagen.
    try:
        audio = MutagenFile(str(file_path))

        if audio is None or audio.info is None:
            raise ValueError("Unable to read audio metadata.")

        info = audio.info

        duration = getattr(info, "length", None)
        sample_rate = getattr(info, "sample_rate", None)
        channels = getattr(info, "channels", None)
        bitrate = getattr(info, "bitrate", None)

        if duration is None or sample_rate is None or channels is None:
            raise ValueError("Required audio metadata is missing.")

        if duration <= 0 or sample_rate <= 0 or channels <= 0:
            raise ValueError("Invalid audio metadata values.")

        return AudioMetadata(
            file_name=file_path.name,
            format=file_path.suffix.lower(),
            duration_seconds=round(duration, 2),
            sample_rate=int(sample_rate),
            channels=int(channels),
            bitrate=int(bitrate) if bitrate is not None else None
        )

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            f"Could not extract metadata from {file_path.name}: {error}"
        ) from error
