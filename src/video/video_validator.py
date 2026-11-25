from pathlib import Path

SUPPORTED_VIDEO_FORMATS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm",
    ".m4v",
}


def validate_video_file(video_path: str) -> Path:
    """
    Validate a lecture video file.

    Checks:
    1. The path exists.
    2. The path points to a file.
    3. The file extension is supported.
    4. The file is not empty.
    """

    file_path = Path(video_path).expanduser()

    if not file_path.exists():
        raise FileNotFoundError(
            f"Video file not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"The supplied path is not a file: {file_path}"
        )

    if file_path.suffix.lower() not in SUPPORTED_VIDEO_FORMATS:
        raise ValueError(
            f"Unsupported video format: {file_path.suffix}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError("The video file is empty.")

    return file_path