
import tempfile
import unittest

from pathlib import Path

from src.audio.audio_validator import validate_audio_file


class TestAudioValidator(unittest.TestCase):

    def test_valid_audio_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_file = Path(temp_dir) / "lecture.wav"
            audio_file.write_bytes(b"sample audio data")

            result = validate_audio_file(str(audio_file))

            self.assertEqual(result, audio_file)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            validate_audio_file("missing_lecture.wav")

    def test_unsupported_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "lecture.txt"
            file_path.write_text("not audio")

            with self.assertRaises(ValueError):
                validate_audio_file(str(file_path))

    def test_empty_audio_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_file = Path(temp_dir) / "empty.wav"
            audio_file.touch()

            with self.assertRaises(ValueError):
                validate_audio_file(str(audio_file))

    def test_directory_instead_of_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                validate_audio_file(temp_dir)


if __name__ == "__main__":
    unittest.main()
