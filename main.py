
"""
LectureHelp
AI-powered Lecture Understanding & Learning Assistant

Application entry point.
"""

def display_welcome():
    """Display the application welcome message."""
    print("=" * 55)
    print("              WELCOME TO LECTUREHELP")
    print("=" * 55)
    print("Your AI-powered lecture learning assistant.")
    print()
    print("Planned capabilities:")
    print("1. Lecture audio transcription")
    print("2. Automated notes and summaries")
    print("3. Key concept and definition extraction")
    print("4. Flashcard and quiz generation")
    print("5. Conversational Q&A using RAG")
    print("=" * 55)


def main():
    """Run the LectureHelp application."""
    display_welcome()


if __name__ == "__main__":
    main()
