import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from src.audio.audio_metadata import extract_audio_metadata


class TestAudioMetadata(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.audio_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_wav_file(self, file_path):
        """Create a small valid WAV file for testing."""

        with wave.open(str(file_path), "wb") as audio_file:
            audio_file.setnchannels(1)
            audio_file.setsampwidth(2)
            audio_file.setframerate(16000)
            audio_file.writeframes(b"\x00\x00" * 16000)

    def test_extract_wav_metadata(self):
        audio_path = self.audio_dir / "sample.wav"
        self.create_wav_file(audio_path)

        metadata = extract_audio_metadata(str(audio_path))

        self.assertEqual(metadata.file_name, "sample.wav")
        self.assertEqual(metadata.format, ".wav")
        self.assertEqual(metadata.duration_seconds, 1.0)
        self.assertEqual(metadata.sample_rate, 16000)
        self.assertEqual(metadata.channels, 1)

    def test_invalid_audio_content(self):
        audio_path = self.audio_dir / "invalid.wav"
        audio_path.write_text(
            "This is not a valid audio file.",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            extract_audio_metadata(str(audio_path))

    @patch("src.audio.audio_metadata.MutagenFile")
    def test_missing_audio_metadata(self, mock_mutagen):
        audio_path = self.audio_dir / "sample.wav"
        self.create_wav_file(audio_path)

        mock_mutagen.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Unable to read audio metadata",
        ):
            extract_audio_metadata(str(audio_path))


if __name__ == "__main__":
    unittest.main()