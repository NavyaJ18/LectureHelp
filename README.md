
# LectureHelp

An AI-powered lecture understanding and learning assistant.

## Planned Features

- Lecture audio transcription using Whisper
- Automated lecture notes and summaries
- Important concept and definition extraction
- AI-generated flashcards and quizzes
- Retrieval-Augmented Generation (RAG)
- Conversational question answering over lecture content

## Technology Stack

- Python
- Whisper
- Natural Language Processing
- Large Language Models
- Sentence Transformers
- ChromaDB
- FastAPI
- Streamlit

## Project Status

Currently under development.


## Speech-to-Text Transcription

LectureHelp uses Faster-Whisper to convert processed lecture audio into timestamped text segments.


### Transcript JSON Schema

Each transcription is stored as a JSON document.

Example:

```json
{
    "audio_file": "sample_lecture_processed.wav",
    "language": "en",
    "language_probability": 0.9719,
    "duration_seconds": 54.7,
    "segments": [
        {
            "start": 0.0,
            "end": 4.88,
            "text": "Welcome to this short lecture.",
            "confidence": 0.92
        },
        {
            "start": 4.88,
            "end": 12.96,
            "text": "Today we study artificial intelligence.",
            "confidence": 0.89
        }
    ]
}
```
A manual smoke test is also available through `python test_transcription.py`.

**Field descriptions:**

| Field | Description |
|---|---|
| `audio_file` | Source audio filename |
| `language` | Detected language code |
| `language_probability` | Language detection probability |
| `duration_seconds` | Audio duration in seconds |
| `segments` | List of recognized speech segments |
| `start` | Segment start timestamp |
| `end` | Segment end timestamp |
| `text` | Recognized speech |
| `confidence` | Confidence-like score derived from average log probability |

The confidence-like score is not a calibrated probability of transcription correctness.

### Features

- Speech recognition using the Faster-Whisper model.
- Automatic language detection.
- Language probability estimation.
- Segment-level timestamps.
- Confidence-like scores derived from Whisper's average log probability.
- Automatic JSON transcript persistence.
- Option to disable automatic transcript saving.
- Support for custom transcript output directories.

### Transcription Workflow

1. Load the preprocessed audio file.
2. Initialize the Faster-Whisper model.
3. Generate timestamped transcription segments.
4. Extract language and recognition metadata.
5. Convert segments into structured Python dataclasses.
6. Validate and save the transcription as JSON.

### Output Structure

Transcripts are saved by default in:

`data/transcripts/`

Each transcript contains:
- Original audio filename
- Detected language
- Language probability
- Audio duration
- Segment start and end timestamps
- Transcribed text
- Confidence-like score

### Example Usage

```python
from src.transcription import AudioTranscriber

transcriber = AudioTranscriber(model_size="base")

result = transcriber.transcribe(
    "data/processed/sample_lecture_processed.wav"
)

for segment in result.segments:
    print(
        f"[{segment.start:.2f}s - {segment.end:.2f}s] "
        f"{segment.text}"
    )
```

## Development Progress

### Completed

- [x] Audio file validation and format checking.
- [x] Audio metadata extraction.
- [x] Audio preprocessing and normalization.
- [x] Conversion to 16 kHz mono WAV format.
- [x] Audio ingestion pipeline.
- [x] Faster-Whisper integration.
- [x] Automatic language detection.
- [x] Timestamped speech transcription.
- [x] Structured transcription data models.
- [x] JSON transcript storage and loading.
- [x] Transcript validation.
- [x] Unit tests for audio and transcription modules.

### Upcoming

- [ ] Video ingestion and frame extraction.
- [ ] Slide change detection.
- [ ] OCR-based slide text extraction.
- [ ] Text and visual embeddings.
- [ ] Vector database integration.
- [ ] Retrieval-Augmented Generation (RAG).
- [ ] Lecture summaries and structured notes.
- [ ] Automatic quiz generation.
- [ ] Streamlit user interface.
- [ ] End-to-end integration and evaluation.
