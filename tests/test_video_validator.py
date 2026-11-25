import tempfile
import unittest
from pathlib import Path

from src.video.video_validator import validate_video_file


class TestVideoValidator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.video_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_video_file(self):
        video_path = self.video_dir / "lecture.mp4"
        video_path.write_bytes(b"sample video content")

        result = validate_video_file(str(video_path))

        self.assertEqual(result, video_path)
        self.assertTrue(result.exists())

    def test_missing_video_file(self):
        video_path = self.video_dir / "missing.mp4"

        with self.assertRaises(FileNotFoundError):
            validate_video_file(str(video_path))

    def test_unsupported_video_format(self):
        video_path = self.video_dir / "lecture.txt"
        video_path.write_text("not a video", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            "Unsupported video format",
        ):
            validate_video_file(str(video_path))

    def test_empty_video_file(self):
        video_path = self.video_dir / "empty.mp4"
        video_path.touch()

        with self.assertRaisesRegex(
            ValueError,
            "empty",
        ):
            validate_video_file(str(video_path))

    def test_directory_instead_of_file(self):
        video_path = self.video_dir / "lecture.mp4"
        video_path.mkdir()

        with self.assertRaisesRegex(
            ValueError,
            "not a file",
        ):
            validate_video_file(str(video_path))

    def test_uppercase_video_extension(self):
        video_path = self.video_dir / "lecture.MP4"
        video_path.write_bytes(b"sample video content")

        result = validate_video_file(str(video_path))

        self.assertEqual(result.suffix, ".MP4")


if __name__ == "__main__":
    unittest.main()