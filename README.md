# QuizApp

This is a desktop quiz application built using Python's Tkinter library, designed to help students practice for competitive exams. The application allows users to import, create, and take quizzes with multiple-choice questions.
Features

Import Questions: Load existing question sets from JSON files
Create Question Sets: Manually create new question sets with custom questions
Quiz Functionality:

Randomized question order
Multiple-choice questions
Immediate scoring
Performance feedback


User-Friendly Interface:

Simple navigation between setup, quiz, and results screens
Progress tracking during the quiz
Performance evaluation with encouraging messages



Prerequisites

Python 3.x
Tkinter (usually comes pre-installed with Python)

Ensure you have Python installed on your system

Running the Application
python quiz.py

How to Use
Importing Questions

Click "Import Questions"
Select a JSON file containing quiz questions
The question set will be saved and listed in existing sets

Creating a Question Set

Click "Create New Question Set"
Enter a set name
Add questions:

Enter question text
Provide 4 unique options
Select the correct answer


Save the question set

Taking a Quiz

Select a question set from the list
Click "Load Selected Set"
Answer questions by selecting options
View your score and performance at the end
Option to restart the quiz

Question Set JSON Format
Each question should follow this structure:
jsonCopy[
  {
    "text": "Question text here",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer": "Correct Option"
  }
]
Scoring

Correct answers increase your score
Performance is evaluated based on percentage:

90% and above: Excellent Performance 🏆
75-89%: Great Job 👍
60-74%: Good Performance 👏
Below 60%: Keep Practicing 📚



