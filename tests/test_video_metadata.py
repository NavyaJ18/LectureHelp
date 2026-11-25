import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import cv2

from src.video.video_metadata import extract_video_metadata


class TestVideoMetadata(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.video_path = Path(self.temp_dir.name) / "lecture.mp4"
        self.video_path.write_bytes(b"mock video content")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("src.video.video_metadata.cv2.VideoCapture")
    def test_extract_video_metadata(self, mock_capture):
        mock_video = MagicMock()
        mock_video.isOpened.return_value = True

        mock_video.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FPS: 30.0,
            cv2.CAP_PROP_FRAME_COUNT: 1800.0,
            cv2.CAP_PROP_FRAME_WIDTH: 1920.0,
            cv2.CAP_PROP_FRAME_HEIGHT: 1080.0,
        }[prop]

        mock_capture.return_value = mock_video

        metadata = extract_video_metadata(str(self.video_path))

        self.assertEqual(metadata.file_name, "lecture.mp4")
        self.assertEqual(metadata.format, ".mp4")
        self.assertEqual(metadata.duration_seconds, 60.0)
        self.assertEqual(metadata.fps, 30.0)
        self.assertEqual(metadata.frame_count, 1800)
        self.assertEqual(metadata.width, 1920)
        self.assertEqual(metadata.height, 1080)

        mock_video.release.assert_called_once()

    @patch("src.video.video_metadata.cv2.VideoCapture")
    def test_unreadable_video(self, mock_capture):
        mock_video = MagicMock()
        mock_video.isOpened.return_value = False
        mock_capture.return_value = mock_video

        with self.assertRaisesRegex(ValueError, "Unable to open video"):
            extract_video_metadata(str(self.video_path))

        mock_video.release.assert_called_once()

    @patch("src.video.video_metadata.cv2.VideoCapture")
    def test_invalid_frame_rate(self, mock_capture):
        mock_video = MagicMock()
        mock_video.isOpened.return_value = True
        mock_video.get.return_value = 0

        mock_capture.return_value = mock_video

        with self.assertRaisesRegex(ValueError, "Invalid video frame rate"):
            extract_video_metadata(str(self.video_path))

        mock_video.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()