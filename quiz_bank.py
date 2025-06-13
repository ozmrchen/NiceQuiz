# quiz_bank.py

import os
import json

def load_quizzes_from_directory(directory: str) -> dict:
    """
    Load all quiz JSON files from a specified directory.
    Each file should contain:
      {
        "title": "Quiz Title",
        "questions": [ list of questions ]
      }

    Returns:
        A dictionary of quizzes with filename (without .json) as key,
        and the quiz content (dict with title + questions) as value.
    """
    quizzes = {}

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return quizzes

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    quiz_content = json.load(f)

                quiz_name = filename[:-5]  # Strip '.json'

                # Validate format
                if (isinstance(quiz_content, dict)
                        and 'questions' in quiz_content
                        and isinstance(quiz_content['questions'], list)):

                    quizzes[quiz_name] = quiz_content
                    print(f"Loaded quiz: {quiz_name} ({len(quiz_content['questions'])} questions)")

                else:
                    print(f"Warning: {filename} does not contain a valid quiz format. Skipping.")

            except Exception as e:
                print(f"Failed to load {filename}: {e}")

    return quizzes

# Load quizzes from the quiz_bank directory
quiz_data = load_quizzes_from_directory('quiz_bank')