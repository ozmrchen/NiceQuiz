# calculus.py
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