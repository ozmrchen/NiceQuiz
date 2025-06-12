from nicegui import ui, app
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import base64
import os

# Enhanced quiz data structure with math equations and images
quiz_data = {
    "Algebra Basics": [
        {
            "question": "Solve for x: $2x + 5 = 13$",
            "options": ["$x = 3$", "$x = 4$", "$x = 5$", "$x = 6$"],
            "correct": 1,
            "explanation": "Subtract 5 from both sides: $2x = 8$, then divide by 2: $x = 4$",
            "image": None
        },
        {
            "question": "What is the slope of the line passing through points $(2, 3)$ and $(6, 11)$?",
            "options": ["$m = 1$", "$m = 2$", "$m = 3$", "$m = 4$"],
            "correct": 1,
            "explanation": "Using slope formula: $m = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{11 - 3}{6 - 2} = \\frac{8}{4} = 2$",
            "image": None
        },
        {
            "question": "Expand: $(x + 3)^2$",
            "options": ["$x^2 + 6x + 9$", "$x^2 + 3x + 9$", "$x^2 + 6x + 6$", "$x^2 + 9$"],
            "correct": 0,
            "explanation": "$(x + 3)^2 = x^2 + 2(x)(3) + 3^2 = x^2 + 6x + 9$",
            "image": None
        }
    ],
    "Geometry": [
        {
            "question": "What is the area of a circle with radius $r = 5$ cm?",
            "options": ["$25\\pi$ cm²", "$10\\pi$ cm²", "$5\\pi$ cm²", "$\\pi$ cm²"],
            "correct": 0,
            "explanation": "Area of circle = $\\pi r^2 = \\pi \\times 5^2 = 25\\pi$ cm²",
            "image": None
        },
        {
            "question": "In a right triangle, if one angle is $30°$, what is the other acute angle?",
            "options": ["$45°$", "$60°$", "$90°$", "$120°$"],
            "correct": 1,
            "explanation": "In a triangle, angles sum to $180°$. With one right angle ($90°$) and one $30°$ angle: $180° - 90° - 30° = 60°$",
            "image": None
        }
    ],
    "Calculus": [
        {
            "question": "What is $\\frac{d}{dx}[x^3 + 2x^2 - 5x + 1]$?",
            "options": ["$3x^2 + 4x - 5$", "$3x^2 + 2x - 5$", "$x^3 + 4x - 5$", "$3x^2 + 4x - 1$"],
            "correct": 0,
            "explanation": "Using power rule: $\\frac{d}{dx}[x^n] = nx^{n-1}$, so $\\frac{d}{dx}[x^3 + 2x^2 - 5x + 1] = 3x^2 + 4x - 5$",
            "image": None
        },
        {
            "question": "Evaluate: $\\int_0^2 (3x^2 + 1) dx$",
            "options": ["$8$", "$9$", "$10$", "$11$"],
            "correct": 2,
            "explanation": "$\\int (3x^2 + 1) dx = x^3 + x + C$. Evaluating from 0 to 2: $(2^3 + 2) - (0^3 + 0) = 8 + 2 = 10$",
            "image": None
        }
    ]
}


class QuizSession:
    def __init__(self):
        self.current_quiz = None
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.start_time = None
        self.quiz_completed = False
        self.selected_answer = None


# Global quiz session
session = QuizSession()


def create_image_display(image_path: str, alt_text: str = "Question diagram") -> str:
    """Create HTML for displaying images in questions"""
    if not image_path:
        return ""

    return f'''
    <div class="my-4 text-center">
        <img src="{image_path}" alt="{alt_text}" class="max-w-full h-auto mx-auto border rounded-lg shadow-sm" style="max-height: 300px;">
    </div>
    '''


def create_home_page():
    """Create the main quiz selection page"""
    ui.page_title('Nice Quiz Server - Test Your Knowledge')

    with ui.column().classes('w-full max-w-2xl mx-auto p-6'):
        ui.html('<h1 class="text-3xl font-bold text-center mb-6">📊 Nice Quiz Server</h1>')
        ui.html('<p class="text-center mb-8 text-gray-600">Select a quiz to test your understanding</p>')

        with ui.card().classes('w-full'):
            ui.html('<h2 class="text-xl font-semibold mb-4">Available Quizzes</h2>')

            for quiz_name, questions in quiz_data.items():
                with ui.row().classes('w-full justify-between items-center p-4 border rounded'):
                    with ui.column():
                        ui.html(f'<h3 class="font-medium">{quiz_name}</h3>')
                        ui.html(f'<p class="text-sm text-gray-500">{len(questions)} questions</p>')

                    ui.button('Start Quiz',
                              on_click=lambda q=quiz_name: start_quiz(q),
                              color='primary')



def start_quiz(quiz_name: str):
    """Initialize and start a quiz"""
    session.current_quiz = quiz_name
    session.current_question = 0
    session.score = 0
    session.answers = []
    session.start_time = datetime.now()
    session.quiz_completed = False
    session.selected_answer = None

    ui.navigate.to('/quiz')


@ui.page('/quiz')
def quiz_page():
    """Display the quiz questions with math rendering"""
    if not session.current_quiz:
        ui.navigate.to('/')
        return

    questions = quiz_data[session.current_quiz]

    if session.current_question >= len(questions):
        ui.navigate.to('/results')
        return

    current_q = questions[session.current_question]

    ui.page_title(f'Quiz: {session.current_quiz}')

    with ui.column().classes('w-full max-w-3xl mx-auto p-6'):
        # Progress bar
        progress = (session.current_question + 1) / len(questions) * 100
        ui.html(f'<div class="w-full bg-gray-200 rounded-full h-2 mb-4">'
                f'<div class="bg-blue-600 h-2 rounded-full" style="width: {progress}%"></div></div>')

        # Question header
        ui.html(
            f'<h2 class="text-xl font-semibold mb-2">Question {session.current_question + 1} of {len(questions)}</h2>')

        # Question text with math rendering
        # ui.html(f'<h3 class="text-lg mb-4">{current_q["question"]}</h3>')
        ui.markdown(f"{current_q['question']}", extras=['latex'])

        # Display image if present
        if current_q.get("image"):
            ui.html(create_image_display(current_q["image"]))

        # Answer options using NiceGUI radio component
        session.selected_answer = None
        answer_radio = ui.radio(
            options={i: '' for i, option in enumerate(current_q["options"])},  # Empty labels
            value=None
        ).classes('mb-6')

        # Teleport math content to each radio button label
        for i, option in enumerate(current_q["options"]):
            with ui.teleport(f'#{answer_radio.html_id} > div:nth-child({i + 1}) .q-radio__label'):
                ui.markdown(f"{chr(65 + i)}) {option}", extras=['latex'])  # A), B), C), etc.

        def update_selected_answer(value):
            session.selected_answer = value

        answer_radio.on('update:model-value', update_selected_answer)

        # Navigation buttons
        with ui.row().classes('w-full justify-between'):
            if session.current_question > 0:
                ui.button('Previous',
                          on_click=lambda: go_to_question(session.current_question - 1),
                          color='secondary')
            else:
                ui.html('<div></div>')  # Spacer

            ui.button('Next' if session.current_question < len(questions) - 1 else 'Finish',
                      on_click=lambda: submit_answer(answer_radio.value),
                      color='primary')



def go_to_question(question_num: int):
    """Navigate to a specific question"""
    session.current_question = question_num
    ui.navigate.to('/quiz')


def submit_answer(selected_option: int):
    """Submit answer and move to next question or results"""
    if selected_option is None:
        ui.notify('Please select an answer', type='warning')
        return

    questions = quiz_data[session.current_quiz]
    current_q = questions[session.current_question]

    # Store the answer
    is_correct = selected_option == current_q["correct"]
    session.answers.append({
        'question': current_q["question"],
        'selected': selected_option,
        'correct': current_q["correct"],
        'is_correct': is_correct,
        'explanation': current_q["explanation"],
        'image': current_q.get("image")
    })

    if is_correct:
        session.score += 1

    session.current_question += 1

    if session.current_question >= len(questions):
        session.quiz_completed = True
        ui.navigate.to('/results')
    else:
        ui.navigate.to('/quiz')


@ui.page('/results')
def results_page():
    """Display quiz results with math rendering"""
    if not session.quiz_completed:
        ui.navigate.to('/')
        return

    questions = quiz_data[session.current_quiz]
    total_questions = len(questions)
    percentage = round((session.score / total_questions) * 100)

    ui.page_title('Quiz Results')

    with ui.column().classes('w-full max-w-4xl mx-auto p-6'):
        # Results header
        ui.html('<h1 class="text-3xl font-bold text-center mb-6">🎉 Quiz Complete!</h1>')

        with ui.card().classes('w-full mb-6'):
            ui.html(f'<h2 class="text-2xl font-semibold mb-4">{session.current_quiz} Results</h2>')

            # Score display
            color = 'text-green-600' if percentage >= 70 else 'text-yellow-600' if percentage >= 50 else 'text-red-600'
            ui.html(f'<div class="text-center mb-4">'
                    f'<p class="text-4xl font-bold {color}">{session.score}/{total_questions}</p>'
                    f'<p class="text-xl">Score: {percentage}%</p>'
                    f'</div>')

            # Performance message
            if percentage >= 90:
                message = "Excellent work! You've mastered this topic! 🌟"
            elif percentage >= 70:
                message = "Good job! You have a solid understanding. 👍"
            elif percentage >= 50:
                message = "Not bad! Consider reviewing the material. 📚"
            else:
                message = "Keep studying! Practice makes perfect. 💪"

            ui.html(f'<p class="text-center text-lg mb-4">{message}</p>')

        # Detailed results
        ui.html('<h3 class="text-xl font-semibold mb-4">Question Review</h3>')

        for i, answer in enumerate(session.answers):
            with ui.card().classes('w-full mb-4'):
                status_icon = "✅" if answer['is_correct'] else "❌"
                status_color = "text-green-600" if answer['is_correct'] else "text-red-600"

                ui.html(f'<div class="mb-2">'
                        f'<span class="text-lg">{status_icon}</span> '
                        f'<span class="font-medium">Question {i + 1}</span>'
                        f'</div>')

                # Question with math
                ui.html(f'<p class="mb-2"><strong>Q:</strong> {answer["question"]}</p>')

                # Display image if present
                if answer.get("image"):
                    ui.html(create_image_display(answer["image"]))

                options = quiz_data[session.current_quiz][i]["options"]

                # Selected answer with math
                ui.html(f'<p class="mb-2"><strong>Your answer:</strong> '
                        f'<span class="{status_color}">{options[answer["selected"]]}</span></p>')

                if not answer['is_correct']:
                    ui.html(f'<p class="mb-2"><strong>Correct answer:</strong> '
                            f'<span class="text-green-600">{options[answer["correct"]]}</span></p>')

                # Explanation with math
                ui.html(f'<p class="text-sm text-gray-600"><strong>Explanation:</strong> {answer["explanation"]}</p>')

        # Action buttons
        with ui.row().classes('w-full justify-center gap-4 mt-6'):
            ui.button('Take Another Quiz',
                      on_click=lambda: ui.navigate.to('/'),
                      color='primary')
            ui.button('Retake This Quiz',
                      on_click=lambda: start_quiz(session.current_quiz),
                      color='secondary')



# Set up the main page
@ui.page('/')
def main_page():
    create_home_page()


if __name__ in {"__main__", "__mp_main__"}:
    # Run the server
    ui.run(
        title='Nice Quiz Server',
        port=8080,
        show=True,
        reload=False
    )