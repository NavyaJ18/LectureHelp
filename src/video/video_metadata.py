from dataclasses import dataclass

import cv2

from src.video.video_validator import validate_video_file


@dataclass
class VideoMetadata:
    """Store technical metadata extracted from a video."""

    file_name: str
    format: str
    duration_seconds: float
    fps: float
    frame_count: int
    width: int
    height: int


def extract_video_metadata(video_path: str) -> VideoMetadata:
    """Extract video metadata using OpenCV."""

    file_path = validate_video_file(video_path)
    capture = cv2.VideoCapture(str(file_path))

    try:
        if not capture.isOpened():
            raise ValueError(
                f"Unable to open video file: {file_path.name}"
            )

        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if fps <= 0 or frame_count <= 0:
            raise ValueError(
                "Invalid video frame rate or frame count."
            )

        if width <= 0 or height <= 0:
            raise ValueError("Invalid video resolution.")

        duration = frame_count / fps

        return VideoMetadata(
            file_name=file_path.name,
            format=file_path.suffix.lower(),
            duration_seconds=round(duration, 2),
            fps=round(fps, 2),
            frame_count=int(frame_count),
            width=int(width),
            height=int(height),
        )

    finally:
        capture.release()