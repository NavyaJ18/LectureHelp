
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from src.audio.audio_validator import validate_audio_file


TARGET_SAMPLE_RATE = 16000


def preprocess_audio(
    audio_path: str,
    output_dir: str = "data/processed"
) -> Path:
    """
    Preprocess lecture audio for speech recognition.

    Operations:
    1. Load audio and resample to 16 kHz.
    2. Convert audio to mono.
    3. Normalize audio amplitude.
    4. Save the processed audio as WAV.

    Returns:
        Path: Location of the processed audio file.
    """

    # Validate the original audio.
    file_path = validate_audio_file(audio_path)

    # Create the output directory if it doesn't exist.
    processed_dir = Path(output_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_path = processed_dir / f"{file_path.stem}_processed.wav"

    try:
        # Load, resample and convert to mono.
        audio, sample_rate = librosa.load(
            str(file_path),
            sr=TARGET_SAMPLE_RATE,
            mono=True
        )

        if audio.size == 0:
            raise ValueError("The audio recording contains no samples.")

        # Check for invalid numerical values.
        if not np.all(np.isfinite(audio)):
            raise ValueError("Audio contains invalid numerical values.")

        # Normalize peak amplitude.
        audio = librosa.util.normalize(audio)

        # Save as a 16-bit PCM WAV file.
        sf.write(
            str(output_path),
            audio,
            sample_rate,
            subtype="PCM_16"
        )

        return output_path

    except Exception as error:
        # Remove an incomplete output file if one was created.
        if output_path.exists():
            output_path.unlink()

        if isinstance(error, ValueError):
            raise

        raise RuntimeError(
            f"Audio preprocessing failed: {error}"
        ) from error
