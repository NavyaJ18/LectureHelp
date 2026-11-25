import json
import unittest

from src.transcription.transcription_models import (
    TranscriptionSegment,
    TranscriptionResult,
)


class TestTranscriptionModels(unittest.TestCase):

    def test_multiple_segments_serialization(self):
        result = TranscriptionResult(
            audio_file="long_lecture.wav",
            language="en",
            language_probability=0.97,
            duration_seconds=120.0,
            segments=[
                TranscriptionSegment(
                    start=0.0,
                    end=5.0,
                    text="First segment.",
                    confidence=0.91,
                ),
                TranscriptionSegment(
                    start=5.0,
                    end=12.5,
                    text="Second segment.",
                    confidence=0.88,
                ),
            ],
        )

        data = result.to_dict()

        self.assertEqual(len(data["segments"]), 2)
        self.assertEqual(data["segments"][0]["start"], 0.0)
        self.assertEqual(data["segments"][1]["end"], 12.5)
        self.assertEqual(
            data["segments"][1]["text"],
            "Second segment.",
        )
        
    def setUp(self):
        self.segment = TranscriptionSegment(
            start=0.0,
            end=5.2,
            text="Introduction to machine learning.",
            confidence=0.95,
        )

        self.result = TranscriptionResult(
            audio_file="lecture.wav",
            language="en",
            language_probability=0.98,
            duration_seconds=60.0,
            segments=[self.segment],
        )

    def test_segment_fields(self):
        self.assertEqual(self.segment.start, 0.0)
        self.assertEqual(self.segment.end, 5.2)
        self.assertEqual(
            self.segment.text,
            "Introduction to machine learning.",
        )
        self.assertEqual(self.segment.confidence, 0.95)

    def test_result_to_dict(self):
        data = self.result.to_dict()

        self.assertEqual(data["audio_file"], "lecture.wav")
        self.assertEqual(data["language"], "en")
        self.assertEqual(len(data["segments"]), 1)
        self.assertEqual(
            data["segments"][0]["text"],
            "Introduction to machine learning.",
        )

    def test_result_to_json(self):
        json_output = self.result.to_json()
        data = json.loads(json_output)

        self.assertEqual(data["audio_file"], "lecture.wav")
        self.assertEqual(data["segments"][0]["start"], 0.0)

    def test_json_preserves_unicode(self):
        result = TranscriptionResult(
            audio_file="lecture.wav",
            language="hi",
            language_probability=0.99,
            duration_seconds=10.0,
            segments=[
                TranscriptionSegment(
                    start=0.0,
                    end=5.0,
                    text="नमस्ते",
                    confidence=0.9,
                )
            ],
        )

        json_output = result.to_json()

        self.assertIn("नमस्ते", json_output)


if __name__ == "__main__":
    unittest.main()