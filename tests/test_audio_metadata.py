
import tempfile
import unittest
import wave

from pathlib import Path

from src.audio.audio_metadata import extract_audio_metadata


class TestAudioMetadata(unittest.TestCase):

    def test_extract_wav_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            audio_file = Path(temp_dir) / "lecture.wav"

            # Create a one-second WAV recording.
            with wave.open(str(audio_file), "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(b"\x00\x00" * 44100)

            metadata = extract_audio_metadata(str(audio_file))

            self.assertEqual(metadata.file_name, "lecture.wav")
            self.assertEqual(metadata.format, ".wav")
            self.assertEqual(metadata.sample_rate, 44100)
            self.assertEqual(metadata.channels, 1)
            self.assertAlmostEqual(metadata.duration_seconds, 1.0)

    def test_invalid_audio_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            audio_file = Path(temp_dir) / "invalid.wav"
            audio_file.write_text("This is not an audio recording.")

            with self.assertRaises(ValueError):
                extract_audio_metadata(str(audio_file))


if __name__ == "__main__":
    unittest.main()
