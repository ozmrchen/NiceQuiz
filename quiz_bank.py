# Enhanced quiz data structure with math equations and images
y8_myexam = {
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
}

calculus = {
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

learning_survey = {
    "Learning Behaviours": [
        {
            "question": "Communication: Sharing ideas clearly and listening respectfully.\n\nHow often do you demonstrate this behaviour?",
            "options": ["Never", "Inconsistently", "Often", "Consistently", "Always"],
            "correct": 4,
            "explanation": "This question is for self-assessment; there is no correct answer.",
            "image": None
        },
        {
            "question": "Collaboration: Working effectively with others toward a common goal.\n\nHow often do you demonstrate this behaviour?",
            "options": ["Never", "Inconsistently", "Often", "Consistently", "Always"],
            "correct": 4,
            "explanation": "This question is for self-assessment; there is no correct answer.",
            "image": None
        },
        {
            "question": "Engaged Learning: Actively participating in lessons and completing learning tasks.\n\nHow often do you demonstrate this behaviour?",
            "options": ["Never", "Inconsistently", "Often", "Consistently", "Always"],
            "correct": 4,
            "explanation": "This question is for self-assessment; there is no correct answer.",
            "image": None
        },
        {
            "question": "Behaviour: Following class expectations and demonstrating self-control.\n\nHow often do you demonstrate this behaviour?",
            "options": ["Never", "Inconsistently", "Often", "Consistently", "Always"],
            "correct": 4,
            "explanation": "This question is for self-assessment; there is no correct answer.",
            "image": None
        }
    ]
}


# Allow adding multiple quizzes
quiz_data = {}
quiz_data.update(learning_survey)
quiz_data.update(calculus)
