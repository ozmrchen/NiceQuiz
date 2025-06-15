import json
import os
from datetime import datetime


def save_quiz_result(student_name, quiz_name, answers, score):
    # Create results directory
    os.makedirs('results', exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"results/{quiz_name}_{student_name}_{timestamp}.json"

    # Save result
    result = {
        'student_name': student_name,
        'quiz_name': quiz_name,
        'answers': answers,
        'score': score,
        'completed_at': timestamp
    }

    with open(filename, 'w') as f:
        json.dump(result, f)