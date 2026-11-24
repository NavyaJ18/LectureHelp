
from pathlib import Path

from src.transcription import AudioTranscriber


def main():
    audio_path = input(
        "Enter processed WAV file path: "
    ).strip()

    file_path = Path(audio_path)

    if not file_path.exists() or not file_path.is_file():
        print("Audio file not found.")
        return

    print("\nLoading Faster-Whisper model...")

    transcriber = AudioTranscriber(
        model_size="base",
        save_transcripts=True,
    )

    print("Model loaded. Starting transcription...\n")

    result = transcriber.transcribe(str(file_path))

    print("=" * 60)
    print("TRANSCRIPTION RESULTS")
    print("=" * 60)

    print("Audio file:", result.audio_file)
    print("Language:", result.language)
    print("Language probability:", result.language_probability)
    print("Duration:", result.duration_seconds, "seconds")

    print("\nTRANSCRIPT:")
    print("-" * 60)

    for segment in result.segments:
        print(
            f"[{segment.start:.2f}s - {segment.end:.2f}s] "
            f"{segment.text}"
        )

    transcript_path = (
        Path("data/transcripts")
        / f"{file_path.stem}_transcription.json"
    )

    print("\nTranscript automatically saved to:", transcript_path)


if __name__ == "__main__":
    main()
