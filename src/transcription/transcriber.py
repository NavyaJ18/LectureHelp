
import math

from faster_whisper import WhisperModel

from src.audio.audio_validator import validate_audio_file
from src.transcription.transcription_models import (
    TranscriptionSegment,
    TranscriptionResult,
)
from src.transcription.transcript_storage import save_transcription


MODEL_SIZE = "base"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"


class AudioTranscriber:

    def __init__(
        self,
        model_size: str = MODEL_SIZE,
        device: str = DEVICE,
        compute_type: str = COMPUTE_TYPE,
        save_transcripts: bool = True,
        transcript_dir: str = "data/transcripts",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

        self.save_transcripts = save_transcripts
        self.transcript_dir = transcript_dir

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> TranscriptionResult:

        file_path = validate_audio_file(audio_path)

        try:
            segments, info = self.model.transcribe(
                str(file_path),
                language=language,
                beam_size=5,
                vad_filter=True,
            )

            transcription_segments = []

            for segment in segments:
                text = segment.text.strip()

                if not text:
                    continue

                # This is a confidence-like score, not a calibrated probability.
                confidence = math.exp(segment.avg_logprob)
                confidence = min(1.0, max(0.0, confidence))

                transcription_segments.append(
                    TranscriptionSegment(
                        start=round(segment.start, 2),
                        end=round(segment.end, 2),
                        text=text,
                        confidence=round(confidence, 4),
                    )
                )

            result = TranscriptionResult(
                audio_file=file_path.name,
                language=info.language,
                language_probability=round(
                    info.language_probability, 4
                ),
                duration_seconds=round(info.duration, 2),
                segments=transcription_segments,
            )

            if self.save_transcripts:
                save_transcription(
                    result,
                    output_dir=self.transcript_dir,
                )

            return result

        except Exception as error:
            raise RuntimeError(
                f"Transcription failed for {file_path.name}: {error}"
            ) from error
