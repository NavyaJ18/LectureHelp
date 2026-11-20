
from pathlib import Path


SUPPORTED_AUDIO_FORMATS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
}


def validate_audio_file(audio_path: str) -> Path:
    """
    Validate a lecture audio file.

    Checks:
    1. The path exists.
    2. The path points to a file.
    3. The file extension is supported.
    4. The file is not empty.

    Returns:
        Path: The validated audio file path.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is invalid or unsupported.
    """

    file_path = Path(audio_path).expanduser()

    # Check whether the path exists.
    if not file_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {file_path}"
        )

    # Ensure the path points to a file, not a directory.
    if not file_path.is_file():
        raise ValueError(
            f"The supplied path is not a file: {file_path}"
        )

    # Check the audio format.
    if file_path.suffix.lower() not in SUPPORTED_AUDIO_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {file_path.suffix}"
        )

    # Reject empty files.
    if file_path.stat().st_size == 0:
        raise ValueError("The audio file is empty.")

    return file_path
