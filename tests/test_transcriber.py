
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.transcription.transcriber import AudioTranscriber


class TestAudioTranscriber(unittest.TestCase):

    @patch("src.transcription.transcriber.WhisperModel")
    def setUp(self, mock_whisper_model):
        self.mock_model = MagicMock()
        mock_whisper_model.return_value = self.mock_model

        self.transcriber = AudioTranscriber()

    @patch("src.transcription.transcriber.validate_audio_file")
    def test_successful_transcription(self, mock_validate):

        mock_validate.return_value.name = "lecture.wav"

        mock_segment = SimpleNamespace(
            start=0.0,
            end=4.5,
            text=" Today we study neural networks. ",
            avg_logprob=-0.2
        )

        mock_info = SimpleNamespace(
            language="en",
            language_probability=0.98,
            duration=120.0
        )

        self.mock_model.transcribe.return_value = (
            iter([mock_segment]),
            mock_info
        )

        result = self.transcriber.transcribe("lecture.wav")

        self.assertEqual(result.audio_file, "lecture.wav")
        self.assertEqual(result.language, "en")
        self.assertEqual(len(result.segments), 1)

        self.assertEqual(
            result.segments[0].text,
            "Today we study neural networks."
        )

        self.assertEqual(result.segments[0].start, 0.0)
        self.assertEqual(result.segments[0].end, 4.5)

    @patch("src.transcription.transcriber.validate_audio_file")
    def test_empty_transcription(self, mock_validate):

        mock_validate.return_value.name = "lecture.wav"

        mock_info = SimpleNamespace(
            language="en",
            language_probability=0.95,
            duration=60.0
        )

        self.mock_model.transcribe.return_value = (
            iter([]),
            mock_info
        )

        result = self.transcriber.transcribe("lecture.wav")

        self.assertEqual(len(result.segments), 0)

    @patch("src.transcription.transcriber.validate_audio_file")
    def test_transcription_failure(self, mock_validate):

        mock_validate.return_value.name = "lecture.wav"

        self.mock_model.transcribe.side_effect = Exception(
            "Model execution error"
        )

        with self.assertRaises(RuntimeError):
            self.transcriber.transcribe("lecture.wav")


if __name__ == "__main__":
    unittest.main()
