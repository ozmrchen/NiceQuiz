import secrets
from nicegui import ui, app
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import base64, uuid
import os
from quiz_bank import quiz_data
from quiz_results.recorder import save_quiz_result


# Function to get or create storage secret
def get_storage_secret():
    secret_file = '.storage_secret'

    if os.path.exists(secret_file):
        # Read existing secret
        with open(secret_file, 'r') as f:
            return f.read().strip()
    else:
        # Generate new secret and save it
        secret = secrets.token_hex(32)
        with open(secret_file, 'w') as f:
            f.write(secret)
        # Make file readable only by owner (Unix/Linux/Mac)
        if os.name != 'nt':  # Not Windows
            os.chmod(secret_file, 0o600)
        return secret


# Dictionary to store user sessions
sessions = {}


class QuizSession:
    def __init__(self):
        self.current_quiz = None
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.start_time = None
        self.quiz_completed = False
        self.selected_answer = None


def get_user_session() -> QuizSession:
    # Use a simple approach - try to get from user storage, fallback to generating new session
    try:
        # Try to get existing session ID from user storage
        user_data = app.storage.user
        session_id = user_data.get('session_id')

        # Check if student name is missing
        if not user_data.get('student_name'):
            ui.navigate.to('/dashboard')

        if not session_id:
            # Generate new session ID and store it. ie session_0, session_1, etc.
            session_id = str(uuid.uuid4())
            user_data['session_id'] = session_id

    except Exception:
        # Fallback: use a simple counter-based approach
        session_id = f"session_{len(sessions)}"

    if session_id not in sessions:
        sessions[session_id] = QuizSession()

    return sessions[session_id]


def create_image_display(image_path: str, alt_text: str = "Question diagram") -> str:
    """Create HTML for displaying images in questions"""
    if not image_path:
        return ""

    return f'''
    <div class="my-4 text-center">
        <img src="{image_path}" alt="{alt_text}" class="max-w-full h-auto mx-auto border rounded-lg shadow-sm" style="max-height: 300px;">
    </div>
    '''


# Set up the main page
@ui.page('/')
def main_page():
    """Create the main quiz selection page"""
    ui.page_title('Nice Quiz Server - Test Your Knowledge')

    user_data = app.storage.user

    # Check if student name is set, if not redirect to dashboard
    if not user_data.get('student_name'):
        ui.navigate.to('/dashboard')

    with ui.column().classes('w-full max-w-2xl mx-auto p-6'):
        ui.html('<h1 class="text-3xl font-bold text-center mb-6">📊 Nice Quiz Server</h1>')
        ui.html('<p class="text-center mb-8 text-gray-600">Select a quiz to test your understanding</p>')

        with ui.card().classes('w-full'):
            ui.html('<h2 class="text-xl font-semibold mb-4">Available Quizzes</h2>')

            for quiz_name, quiz_content in quiz_data.items():
                questions = quiz_content['questions']
                title = quiz_content.get('title', quiz_name)

                with ui.row().classes('w-full justify-between items-center p-4 border rounded'):
                    with ui.column():
                        ui.html(f'<h3 class="font-medium">{title}</h3>')
                        ui.html(f'<p class="text-sm text-gray-500">{len(questions)} questions</p>')

                    ui.button('Start Quiz',
                              on_click=lambda q=quiz_name: start_quiz(q),
                              color='primary')


def start_quiz(quiz_name: str):
    """Initialize and start a quiz"""
    session = get_user_session()
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
    session = get_user_session()
    if not session.current_quiz:
        ui.navigate.to('/')
        return

    questions = quiz_data[session.current_quiz]['questions']

    if session.current_question >= len(questions):
        ui.navigate.to('/results')
        return

    current_q = questions[session.current_question]

    ui.page_title(f'Quiz: {quiz_data[session.current_quiz].get("title", session.current_quiz)}')

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
    session = get_user_session()
    session.current_question = question_num
    ui.navigate.to('/quiz')


def submit_answer(selected_option: int):
    """Submit answer and move to next question or results"""
    session = get_user_session()
    if selected_option is None:
        ui.notify('Please select an answer', type='warning')
        return

    questions = quiz_data[session.current_quiz]['questions']
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
    session = get_user_session()
    if not session.quiz_completed:
        ui.navigate.to('/')
        return

    questions = quiz_data[session.current_quiz]['questions']
    title = quiz_data[session.current_quiz].get('title', session.current_quiz)
    total_questions = len(questions)
    percentage = round((session.score / total_questions) * 100)

    ui.page_title('Quiz Results')

    with ui.column().classes('w-full max-w-4xl mx-auto p-6'):
        # Results header
        ui.html('<h1 class="text-3xl font-bold text-center mb-6">🎉 Quiz Complete!</h1>')

        with ui.card().classes('w-full mb-6'):
            ui.html(f'<h2 class="text-2xl font-semibold mb-4">{title} Results</h2>')

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
                # ui.html(f'<p class="mb-2"><strong>Q:</strong> {answer["question"]}</p>')
                ui.markdown(f"{answer['question']}", extras=['latex'])

                # Display image if present
                if answer.get("image"):
                    ui.html(create_image_display(answer["image"]))

                options = quiz_data[session.current_quiz]["questions"][i]["options"]

                # Selected answer with math
                ui.markdown(
                    f"<p class='mb-2 {status_color}'><strong>Your answer:</strong> {options[answer['selected']]}</p>",
                    extras=['latex'])

                if not answer['is_correct']:
                    # ui.html(f'<p class="mb-2"><strong>Correct answer:</strong> '
                    #         f'<span class="text-green-600">{options[answer["correct"]]}</span></p>')
                    ui.markdown(f"<p class='mb-2'><strong>Correct answer:</strong> {options[answer['correct']]}</p>",
                                extras=['latex'])

                # Explanation with math
                ui.markdown(
                    f"<p class='text-sm text-gray-600'><strong>Explanation:</strong> {answer['explanation']}</p>",
                    extras=['latex']
                )

        # Record quiz result
        user_data = app.storage.user
        save_quiz_result(
            student_name=user_data['student_name'],
            quiz_name=session.current_quiz,
            answers=[ans['selected'] for ans in session.answers],
            score=f"{session.score}/{total_questions}"
        )

        # Action buttons
        with ui.row().classes('w-full justify-center gap-4 mt-6'):
            ui.button('Take Another Quiz',
                      on_click=lambda: ui.navigate.to('/'),
                      color='primary')
            ui.button('Retake This Quiz',
                      on_click=lambda: start_quiz(session.current_quiz),
                      color='secondary')


@ui.page('/dashboard')
def dashboard():
    user_data = app.storage.user
    session_id = user_data.get('session_id', 'Unknown')
    current_name = user_data.get('student_name', '')

    with ui.column().classes('w-full max-w-md mx-auto p-6'):
        ui.html('<h1 class="text-3xl font-bold text-center mb-6">📊 Nice Quiz Dashboard</h1>')
        ui.html('<p class="text-center mb-8 text-gray-600">View Statistics</p>')

        # Name entry
        if current_name:
            ui.html(f'<p class="mb-4">Welcome, <strong>{current_name}</strong>!</p>')
        else:
            name_input = ui.input('Your Name', value=current_name)
            ui.button('Save Name', on_click=lambda: save_name(name_input.value))

        # Start quiz button
        if current_name:
            # Show session ID as account id and student name
            ui.html(f'<p>ID: {session_id[:6]} Name: {current_name}</p>')
            ui.button('Start Quiz', on_click=lambda: ui.navigate.to('/'))


def save_name(name):
    user_data = app.storage.user
    user_data['student_name'] = name
    ui.navigate.reload()  # Refresh to show updated info


# Run the server
ui.run(
    title='Nice Quiz Server',
    port=8080,
    show=True,
    reload=False,
    storage_secret=get_storage_secret(),
)
