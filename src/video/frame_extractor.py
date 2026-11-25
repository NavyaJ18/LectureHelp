from pathlib import Path

import cv2

from src.video.video_validator import validate_video_file


def extract_video_frames(
    video_path: str,
    output_dir: str = "data/frames",
    interval_seconds: float = 5.0,
) -> list[Path]:
    """
    Extract video frames at fixed time intervals.

    Args:
        video_path: Input lecture video.
        output_dir: Directory where extracted frames are saved.
        interval_seconds: Time between extracted frames.

    Returns:
        Paths of successfully saved frame images.
    """

    if (
        isinstance(interval_seconds, bool)
        or not isinstance(interval_seconds, (int, float))
        or interval_seconds <= 0
    ):
        raise ValueError("Frame interval must be a positive number.")

    file_path = validate_video_file(video_path)

    frames_dir = Path(output_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(file_path))
    extracted_frames = []

    try:
        if not capture.isOpened():
            raise ValueError(
                f"Unable to open video file: {file_path.name}"
            )

        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)

        if fps <= 0 or frame_count <= 0:
            raise ValueError("Invalid video properties.")

        duration = frame_count / fps
        interval_frames = max(1, round(interval_seconds * fps))

        frame_index = 0
        saved_count = 0

        while frame_index < frame_count:
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

            success, frame = capture.read()

            if not success:
                break

            output_path = (
                frames_dir
                / f"{file_path.stem}_frame_{saved_count:05d}.jpg"
            )

            if not cv2.imwrite(str(output_path), frame):
                raise RuntimeError(
                    f"Failed to save extracted frame: {output_path}"
                )

            extracted_frames.append(output_path)
            saved_count += 1
            frame_index += interval_frames

        return extracted_frames

    except Exception:
        for frame_path in extracted_frames:
            if frame_path.exists():
                frame_path.unlink()
        raise

    finally:
        capture.release()