
import tempfile
import unittest
import wave

import numpy as np
import soundfile as sf

from pathlib import Path

from src.audio.audio_preprocessor import preprocess_audio


class TestAudioPreprocessor(unittest.TestCase):

    def test_preprocess_stereo_audio(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            input_path = Path(temp_dir) / "lecture.wav"
            output_dir = Path(temp_dir) / "processed"

            sample_rate = 44100
            duration = 2

            # Generate a test signal.
            time = np.linspace(
                0,
                duration,
                sample_rate * duration,
                endpoint=False
            )

            signal = 0.2 * np.sin(2 * np.pi * 440 * time)

            # Create stereo audio.
            stereo_audio = np.column_stack((signal, signal))

            sf.write(input_path, stereo_audio, sample_rate)

            # Preprocess the audio.
            output_path = preprocess_audio(
                str(input_path),
                str(output_dir)
            )

            # Inspect the generated WAV file.
            info = sf.info(str(output_path))

            self.assertTrue(output_path.exists())
            self.assertEqual(info.samplerate, 16000)
            self.assertEqual(info.channels, 1)
            self.assertEqual(info.subtype, "PCM_16")

            self.assertAlmostEqual(
                info.duration,
                duration,
                delta=0.1
            )

    def test_processed_output_is_wav(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            input_path = Path(temp_dir) / "lecture.wav"
            output_dir = Path(temp_dir) / "processed"

            sample_rate = 44100

            with wave.open(str(input_path), "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(
                    b"\x00\x00" * sample_rate
                )

            output_path = preprocess_audio(
                str(input_path),
                str(output_dir)
            )

            self.assertEqual(output_path.suffix, ".wav")
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
