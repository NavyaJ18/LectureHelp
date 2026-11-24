
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.transcription.transcriber import AudioTranscriber


class TestAudioTranscriber(unittest.TestCase):

    def setUp(self):
        self.model_patcher = patch(
            "src.transcription.transcriber.WhisperModel"
        )
        self.save_patcher = patch(
            "src.transcription.transcriber.save_transcription"
        )
        self.validate_patcher = patch(
            "src.transcription.transcriber.validate_audio_file"
        )

        self.mock_whisper_model = self.model_patcher.start()
        self.mock_save = self.save_patcher.start()
        self.mock_validate = self.validate_patcher.start()

        self.addCleanup(self.model_patcher.stop)
        self.addCleanup(self.save_patcher.stop)
        self.addCleanup(self.validate_patcher.stop)

        self.mock_model = MagicMock()
        self.mock_whisper_model.return_value = self.mock_model

        self.mock_validate.return_value = Path("lecture.wav")

        self.transcriber = AudioTranscriber()

    def configure_empty_transcription(self):
        mock_info = SimpleNamespace(
            language="en",
            language_probability=0.95,
            duration=60.0,
        )

        self.mock_model.transcribe.return_value = (
            iter([]),
            mock_info,
        )

    def test_successful_transcription(self):
        mock_segment = SimpleNamespace(
            start=0.0,
            end=4.5,
            text=" Today we study neural networks. ",
            avg_logprob=-0.2,
        )

        mock_info = SimpleNamespace(
            language="en",
            language_probability=0.98,
            duration=120.0,
        )

        self.mock_model.transcribe.return_value = (
            iter([mock_segment]),
            mock_info,
        )

        result = self.transcriber.transcribe("lecture.wav")

        self.assertEqual(result.audio_file, "lecture.wav")
        self.assertEqual(result.language, "en")
        self.assertEqual(len(result.segments), 1)
        self.assertEqual(
            result.segments[0].text,
            "Today we study neural networks.",
        )

        self.mock_save.assert_called_once_with(
            result,
            output_dir="data/transcripts",
        )

    def test_empty_transcription(self):
        self.configure_empty_transcription()

        result = self.transcriber.transcribe("lecture.wav")

        self.assertEqual(len(result.segments), 0)

        self.mock_save.assert_called_once_with(
            result,
            output_dir="data/transcripts",
        )

    def test_custom_transcript_directory(self):
        self.configure_empty_transcription()

        custom_dir = "custom_transcripts"

        transcriber = AudioTranscriber(
            transcript_dir=custom_dir
        )

        result = transcriber.transcribe("lecture.wav")

        self.mock_save.assert_called_once_with(
            result,
            output_dir=custom_dir,
        )

    def test_transcription_failure(self):
        self.mock_model.transcribe.side_effect = Exception(
            "Model execution error"
        )

        with self.assertRaises(RuntimeError):
            self.transcriber.transcribe("lecture.wav")

        self.mock_save.assert_not_called()

    def test_saving_can_be_disabled(self):
        self.configure_empty_transcription()

        transcriber = AudioTranscriber(save_transcripts=False)
        result = transcriber.transcribe("lecture.wav")

        self.assertEqual(len(result.segments), 0)
        self.assertEqual(result.language, "en")
        self.assertEqual(result.duration_seconds, 60.0)

        self.mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
