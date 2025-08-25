import json
import os
import openai
from dotenv import load_dotenv

load_dotenv()


class QuizGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load the knowledge base file."""
        with open("quiz_knowledge_base.md", 'r') as f:
            return f.read()

    def generate_quiz(self, instruction):
        """Generate a quiz based on instruction."""
        prompt = f"""
Knowledge Base:
{self.knowledge_base}

Instruction: {instruction}

Create a quiz as JSON with this structure:
{{
    "title": "Quiz Title",
    "questions": [
        {{
            "question": "Question text?",
            "type": "multiple_choice",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A"
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Clean and parse response
        quiz_json = response.choices[0].message.content.strip()
        if quiz_json.startswith('```json'):
            quiz_json = quiz_json[7:-3]

        return json.loads(quiz_json)

    def save_quiz(self, quiz_data, filename=None):
        """Save quiz to file."""
        if not filename:
            filename = f"{quiz_data['title'].replace(' ', '_')}.json"

        with open(filename, 'w') as f:
            json.dump(quiz_data, f, indent=2)

        return filename

    def print_summary(self, quiz_data):
        """Print quiz summary."""
        print(f"Title: {quiz_data['title']}")
        print(f"Questions: {len(quiz_data['questions'])}")
        print(f"First question: {quiz_data['questions'][0]['question']}")


# Usage
if __name__ == "__main__":
    generator = QuizGenerator()

    instruction = input("Enter quiz instruction: ")
    quiz = generator.generate_quiz(instruction)
    filename = generator.save_quiz(quiz)

    print(f"Quiz saved to: {filename}")
    generator.print_summary(quiz)