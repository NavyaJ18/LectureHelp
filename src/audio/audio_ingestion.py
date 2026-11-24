
from dataclasses import dataclass
from pathlib import Path

from src.audio.audio_validator import validate_audio_file
from src.audio.audio_metadata import (
    AudioMetadata,
    extract_audio_metadata
)
from src.audio.audio_preprocessor import (
    preprocess_audio,
    TARGET_SAMPLE_RATE
)


@dataclass
class AudioIngestionResult:
    """
    Stores the result of the complete audio ingestion pipeline.
    """

    original_metadata: AudioMetadata
    processed_metadata: AudioMetadata
    processed_path: Path


def process_audio(
    audio_path: str,
    output_dir: str = "data/processed"
) -> AudioIngestionResult:
    """
    Execute the complete audio ingestion pipeline.

    Steps:
    1. Validate the input audio.
    2. Extract original audio metadata.
    3. Preprocess the audio.
    4. Extract processed audio metadata.
    5. Verify preprocessing requirements.

    Returns:
        AudioIngestionResult: Original metadata, processed
        metadata and processed audio location.
    """

    processed_path = None

    try:
        # Step 1: Validate the input audio.
        validated_path = validate_audio_file(audio_path)

        # Step 2: Extract original audio metadata.
        original_metadata = extract_audio_metadata(
            str(validated_path)
        )

        # Step 3: Preprocess the original audio.
        processed_path = preprocess_audio(
            str(validated_path),
            output_dir=output_dir
        )

        # Step 4: Verify that the output was generated.
        if not processed_path.exists():
            raise RuntimeError(
                "Audio preprocessing did not generate an output file."
            )

        if processed_path.stat().st_size == 0:
            raise RuntimeError(
                "The processed audio file is empty."
            )

        # Step 5: Extract metadata from processed audio.
        processed_metadata = extract_audio_metadata(
            str(processed_path)
        )

        # Step 6: Verify the expected audio specifications.
        if processed_metadata.sample_rate != TARGET_SAMPLE_RATE:
            raise RuntimeError(
                "Processed audio has an incorrect sample rate."
            )

        if processed_metadata.channels != 1:
            raise RuntimeError(
                "Processed audio is not mono."
            )

        return AudioIngestionResult(
            original_metadata=original_metadata,
            processed_metadata=processed_metadata,
            processed_path=processed_path
        )

    except Exception:
        # Remove generated output if the pipeline fails.
        if processed_path is not None and processed_path.exists():
            processed_path.unlink()

        raise
