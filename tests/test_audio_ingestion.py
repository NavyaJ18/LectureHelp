
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.audio.audio_ingestion import process_audio
from src.audio.audio_metadata import AudioMetadata


class TestAudioIngestion(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name) / "processed"
        self.output_dir.mkdir()

        self.input_path = Path(self.temp_dir.name) / "lecture.mp3"
        self.input_path.write_bytes(b"dummy audio")

        self.processed_path = self.output_dir / "lecture_processed.wav"
        self.processed_path.write_bytes(b"processed audio")

        self.original_metadata = AudioMetadata(
            file_name="lecture.mp3",
            format=".mp3",
            duration_seconds=120.0,
            sample_rate=44100,
            channels=2,
            bitrate=128000
        )

        self.processed_metadata = AudioMetadata(
            file_name="lecture_processed.wav",
            format=".wav",
            duration_seconds=120.0,
            sample_rate=16000,
            channels=1,
            bitrate=None
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("src.audio.audio_ingestion.preprocess_audio")
    @patch("src.audio.audio_ingestion.extract_audio_metadata")
    @patch("src.audio.audio_ingestion.validate_audio_file")
    def test_successful_audio_ingestion(
        self,
        mock_validate,
        mock_metadata,
        mock_preprocess
    ):
        mock_validate.return_value = self.input_path

        mock_metadata.side_effect = [
            self.original_metadata,
            self.processed_metadata
        ]

        mock_preprocess.return_value = self.processed_path

        result = process_audio(
            str(self.input_path),
            str(self.output_dir)
        )

        self.assertEqual(
            result.original_metadata.sample_rate,
            44100
        )

        self.assertEqual(
            result.processed_metadata.sample_rate,
            16000
        )

        self.assertEqual(
            result.processed_metadata.channels,
            1
        )

        self.assertEqual(
            result.processed_path,
            self.processed_path
        )

        self.assertTrue(result.processed_path.exists())

    @patch("src.audio.audio_ingestion.validate_audio_file")
    def test_invalid_input_raises_error(self, mock_validate):

        mock_validate.side_effect = FileNotFoundError(
            "Audio file not found"
        )

        with self.assertRaises(FileNotFoundError):
            process_audio(
                str(self.input_path),
                str(self.output_dir)
            )

    @patch("src.audio.audio_ingestion.preprocess_audio")
    @patch("src.audio.audio_ingestion.extract_audio_metadata")
    @patch("src.audio.audio_ingestion.validate_audio_file")
    def test_incorrect_sample_rate_removes_output(
        self,
        mock_validate,
        mock_metadata,
        mock_preprocess
    ):
        mock_validate.return_value = self.input_path

        mock_metadata.side_effect = [
            self.original_metadata,
            AudioMetadata(
                file_name="lecture_processed.wav",
                format=".wav",
                duration_seconds=120.0,
                sample_rate=44100,
                channels=1,
                bitrate=None
            )
        ]

        mock_preprocess.return_value = self.processed_path

        with self.assertRaises(RuntimeError):
            process_audio(
                str(self.input_path),
                str(self.output_dir)
            )

        self.assertFalse(self.processed_path.exists())


if __name__ == "__main__":
    unittest.main()
