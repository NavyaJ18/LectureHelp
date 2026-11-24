
import json
import tempfile
import unittest
from pathlib import Path

from src.transcription.transcript_storage import (
    save_transcription,
    load_transcription,
)
from src.transcription.transcription_models import (
    TranscriptionSegment,
    TranscriptionResult,
)


class TestTranscriptStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)

        self.result = TranscriptionResult(
            audio_file="sample_lecture_processed.wav",
            language="en",
            language_probability=0.9719,
            duration_seconds=54.7,
            segments=[
                TranscriptionSegment(
                    start=0.0,
                    end=4.88,
                    text="Welcome to this short lecture.",
                    confidence=0.92,
                ),
                TranscriptionSegment(
                    start=4.88,
                    end=12.96,
                    text="Today we study artificial intelligence.",
                    confidence=0.89,
                ),
            ],
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_successful_save(self):
        output_path = save_transcription(
            self.result,
            output_dir=str(self.output_dir),
        )

        self.assertTrue(output_path.exists())
        self.assertEqual(
            output_path.name,
            "sample_lecture_processed_transcription.json",
        )

    def test_successful_load(self):
        output_path = save_transcription(
            self.result,
            output_dir=str(self.output_dir),
        )

        loaded_result = load_transcription(str(output_path))

        self.assertEqual(loaded_result.audio_file, self.result.audio_file)
        self.assertEqual(loaded_result.language, self.result.language)
        self.assertEqual(
            loaded_result.language_probability,
            self.result.language_probability,
        )
        self.assertEqual(
            loaded_result.duration_seconds,
            self.result.duration_seconds,
        )
        self.assertEqual(len(loaded_result.segments), 2)
        self.assertEqual(
            loaded_result.segments[0].text,
            self.result.segments[0].text,
        )

    def test_missing_file(self):
        missing_path = self.output_dir / "missing.json"

        with self.assertRaises(FileNotFoundError):
            load_transcription(str(missing_path))

    def test_malformed_json(self):
        invalid_path = self.output_dir / "invalid.json"
        invalid_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_transcription(str(invalid_path))

    def test_invalid_segment_timestamp(self):
        self.result.segments[0].end = -1.0

        with self.assertRaises(ValueError):
            save_transcription(
                self.result,
                output_dir=str(self.output_dir),
            )

    def test_invalid_confidence(self):
        self.result.segments[0].confidence = 1.5

        with self.assertRaises(ValueError):
            save_transcription(
                self.result,
                output_dir=str(self.output_dir),
            )

    def test_invalid_json_structure(self):
        invalid_path = self.output_dir / "invalid_structure.json"

        invalid_path.write_text(
            json.dumps({"audio_file": "lecture.wav"}),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_transcription(str(invalid_path))

    def test_empty_segments(self):
        self.result.segments = []

        output_path = save_transcription(
            self.result,
            output_dir=str(self.output_dir),
        )

        loaded_result = load_transcription(str(output_path))

        self.assertEqual(loaded_result.segments, [])


if __name__ == "__main__":
    unittest.main()
