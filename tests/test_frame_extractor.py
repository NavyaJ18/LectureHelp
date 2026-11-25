import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import cv2

from src.video.frame_extractor import extract_video_frames


class TestFrameExtractor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.video_path = Path(self.temp_dir.name) / "lecture.mp4"
        self.video_path.write_bytes(b"mock video content")

        self.output_dir = Path(self.temp_dir.name) / "frames"

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("src.video.frame_extractor.cv2.imwrite")
    @patch("src.video.frame_extractor.cv2.VideoCapture")
    def test_successful_frame_extraction(
        self,
        mock_capture,
        mock_imwrite,
    ):
        mock_video = MagicMock()
        mock_video.isOpened.return_value = True
        mock_video.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FPS: 30.0,
            cv2.CAP_PROP_FRAME_COUNT: 300.0,
        }[prop]

        mock_video.read.return_value = (
            True,
            np.zeros((100, 100, 3), dtype=np.uint8),
        )

        mock_capture.return_value = mock_video
        mock_imwrite.return_value = True

        frames = extract_video_frames(
            str(self.video_path),
            output_dir=str(self.output_dir),
            interval_seconds=5,
        )

        self.assertEqual(len(frames), 2)
        self.assertTrue(all(path.suffix == ".jpg" for path in frames))
        self.assertEqual(mock_imwrite.call_count, 2)
        mock_video.release.assert_called_once()

    def test_invalid_interval(self):
        with self.assertRaisesRegex(
            ValueError,
            "positive number",
        ):
            extract_video_frames(
                str(self.video_path),
                interval_seconds=0,
            )

    @patch("src.video.frame_extractor.cv2.VideoCapture")
    def test_unreadable_video(self, mock_capture):
        mock_video = MagicMock()
        mock_video.isOpened.return_value = False
        mock_capture.return_value = mock_video

        with self.assertRaisesRegex(
            ValueError,
            "Unable to open video",
        ):
            extract_video_frames(
                str(self.video_path),
                output_dir=str(self.output_dir),
            )

        mock_video.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()