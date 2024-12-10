import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import random
import os

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Competitive Exam Quiz App")
        self.master.geometry("600x700")
        
        # Quiz data storage
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        
        # Create main frames
        self.setup_frame = tk.Frame(master)
        self.quiz_frame = tk.Frame(master)
        self.result_frame = tk.Frame(master)
        
        # Setup Frame Widgets
        self.setup_frame_widgets()
        self.setup_frame.pack(expand=True, fill='both')
    
    def setup_frame_widgets(self):
        # Title
        tk.Label(self.setup_frame, text="Quiz Application", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Import Questions Button
        import_btn = tk.Button(self.setup_frame, text="Import Questions", command=self.import_questions)
        import_btn.pack(pady=10)
        
        # Create Questions Button
        create_btn = tk.Button(self.setup_frame, text="Create New Question Set", command=self.create_question_set)
        create_btn.pack(pady=10)
        
        # Existing Question Sets
        tk.Label(self.setup_frame, text="Existing Question Sets:", font=("Arial", 12)).pack(pady=10)
        self.question_sets_listbox = tk.Listbox(self.setup_frame, width=50)
        self.question_sets_listbox.pack(pady=10)
        self.load_existing_question_sets()
        
        # Load Selected Set Button
        load_btn = tk.Button(self.setup_frame, text="Load Selected Set", command=self.load_selected_set)
        load_btn.pack(pady=10)
    
    def load_existing_question_sets(self):
        # List JSON files in a 'question_sets' directory
        if not os.path.exists('question_sets'):
            os.makedirs('question_sets')
        
        question_sets = [f for f in os.listdir('question_sets') if f.endswith('.json')]
        self.question_sets_listbox.delete(0, tk.END)
        for qset in question_sets:
            self.question_sets_listbox.insert(tk.END, qset)
    
    def import_questions(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    imported_questions = json.load(file)
                    
                # Save to question sets directory
                filename = os.path.basename(file_path)
                save_path = os.path.join('question_sets', filename)
                with open(save_path, 'w') as save_file:
                    json.dump(imported_questions, save_file, indent=4)
                
                messagebox.showinfo("Success", f"Questions imported from {filename}")
                self.load_existing_question_sets()
            except Exception as e:
                messagebox.showerror("Error", f"Could not import questions: {str(e)}")
    
    def create_question_set(self):
        CreateQuestionSetWindow(self.master, self)
    
    def load_selected_set(self):
        selection = self.question_sets_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question set")
            return
        
        selected_file = self.question_sets_listbox.get(selection[0])
        file_path = os.path.join('question_sets', selected_file)
        
        try:
            with open(file_path, 'r') as file:
                self.questions = json.load(file)
            
            # Start quiz
            self.start_quiz()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load questions: {str(e)}")
    
    def start_quiz(self):
        if not self.questions:
            messagebox.showwarning("Warning", "No questions available")
            return
        
        # Shuffle questions
        random.shuffle(self.questions)
        
        # Reset quiz state
        self.current_question_index = 0
        self.score = 0
        
        # Hide setup frame, show quiz frame
        self.setup_frame.pack_forget()
        self.quiz_frame_widgets()
        self.quiz_frame.pack(expand=True, fill='both')
    
    def quiz_frame_widgets(self):
        # Clear previous widgets if any
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        
        # Current question
        current_q = self.questions[self.current_question_index]
        
        # Question text
        tk.Label(self.quiz_frame, text=current_q['text'], 
                 font=("Arial", 14), wraplength=500).pack(pady=20)
        
        # Variable to store selected option
        self.selected_option = tk.StringVar()
        
        # Options
        for option in current_q['options']:
            option_radio = tk.Radiobutton(self.quiz_frame, 
                                          text=option, 
                                          variable=self.selected_option, 
                                          value=option,
                                          font=("Arial", 12))
            option_radio.pack(pady=10)
        
        # Submit button
        submit_btn = tk.Button(self.quiz_frame, text="Submit", command=self.check_answer)
        submit_btn.pack(pady=20)
        
        # Progress indicator
        progress_label = tk.Label(self.quiz_frame, 
                                  text=f"Question {self.current_question_index + 1} of {len(self.questions)}",
                                  font=("Arial", 10))
        progress_label.pack(pady=10)
    
    def check_answer(self):
        # Validate option selected
        if not self.selected_option.get():
            messagebox.showwarning("Warning", "Please select an option")
            return
        
        # Check if answer is correct
        current_q = self.questions[self.current_question_index]
        if self.selected_option.get() == current_q['correct_answer']:
            self.score += 1
        
        # Move to next question or end quiz
        self.current_question_index += 1
        
        if self.current_question_index < len(self.questions):
            # Next question
            self.quiz_frame_widgets()
        else:
            # End of quiz
            self.show_results()
    
    def show_results(self):
        # Hide quiz frame
        self.quiz_frame.pack_forget()
        
        # Clear previous result widgets
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Display results
        tk.Label(self.result_frame, text="Quiz Completed!", font=("Arial", 20, "bold")).pack(pady=20)
        
        score_percent = (self.score / len(self.questions)) * 100
        tk.Label(self.result_frame, 
                 text=f"Your Score: {self.score} / {len(self.questions)}", 
                 font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.result_frame, 
                 text=f"Percentage: {score_percent:.2f}%", 
                 font=("Arial", 14)).pack(pady=10)
        
        # Performance message
        if score_percent >= 90:
            performance_msg = "Excellent Performance! 🏆"
        elif score_percent >= 75:
            performance_msg = "Great Job! 👍"
        elif score_percent >= 60:
            performance_msg = "Good Performance 👏"
        else:
            performance_msg = "Keep Practicing 📚"
        
        tk.Label(self.result_frame, 
                 text=performance_msg, 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Restart Quiz Button
        restart_btn = tk.Button(self.result_frame, text="Restart Quiz", command=self.restart_quiz)
        restart_btn.pack(pady=20)
        
        # Show result frame
        self.result_frame.pack(expand=True, fill='both')
    
    def restart_quiz(self):
        # Hide result frame
        self.result_frame.pack_forget()
        
        # Show setup frame
        self.setup_frame.pack(expand=True, fill='both')

class CreateQuestionSetWindow:
    def __init__(self, master, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel(master)
        self.window.title("Create Question Set")
        self.window.geometry("500x600")
        
        # Questions list
        self.questions = []
        
        # Question Set Name
        tk.Label(self.window, text="Question Set Name:", font=("Arial", 12)).pack(pady=10)
        self.set_name_entry = tk.Entry(self.window, width=50)
        self.set_name_entry.pack(pady=10)
        
        # Question Text
        tk.Label(self.window, text="Question Text:", font=("Arial", 12)).pack(pady=10)
        self.question_text = tk.Text(self.window, height=3, width=50)
        self.question_text.pack(pady=10)
        
        # Options Frame
        options_frame = tk.Frame(self.window)
        options_frame.pack(pady=10)
        
        # Option Entries
        self.option_entries = []
        for i in range(4):
            label = tk.Label(options_frame, text=f"Option {i+1}:")
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(options_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.option_entries.append(entry)
        
        # Correct Answer Dropdown
        tk.Label(self.window, text="Correct Answer:", font=("Arial", 12)).pack(pady=10)
        self.correct_answer = tk.StringVar()
        correct_answer_dropdown = ttk.Combobox(self.window, textvariable=self.correct_answer, width=47)
        correct_answer_dropdown.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        
        add_btn = tk.Button(btn_frame, text="Add Question", command=self.add_question)
        add_btn.pack(side=tk.LEFT, padx=10)
        
        save_btn = tk.Button(btn_frame, text="Save Question Set", command=self.save_question_set)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # Questions Listbox
        tk.Label(self.window, text="Added Questions:", font=("Arial", 12)).pack(pady=10)
        self.questions_listbox = tk.Listbox(self.window, width=70, height=5)
        self.questions_listbox.pack(pady=10)
        
        # Update correct answer dropdown
        def update_correct_answer_options(*args):
            options = [entry.get() for entry in self.option_entries if entry.get()]
            correct_answer_dropdown['values'] = options
        
        for entry in self.option_entries:
            entry.bind('<KeyRelease>', update_correct_answer_options)
    
    def add_question(self):
        # Validate inputs
        question_text = self.question_text.get("1.0", tk.END).strip()
        options = [entry.get().strip() for entry in self.option_entries]
        correct_answer = self.correct_answer.get()
        
        # Check validations
        if not question_text:
            messagebox.showwarning("Warning", "Please enter question text")
            return
        
        if len(set(options)) < 4 or any(not opt for opt in options):
            messagebox.showwarning("Warning", "Please enter 4 unique options")
            return
        
        if not correct_answer:
            messagebox.showwarning("Warning", "Please select a correct answer")
            return
        
        # Create question dictionary
        question = {
            'text': question_text,
            'options': options,
            'correct_answer': correct_answer
        }
        
        # Add to questions list
        self.questions.append(question)
        
        # Update listbox
        self.questions_listbox.insert(tk.END, question_text[:50] + "...")
        
        # Clear inputs
        self.question_text.delete("1.0", tk.END)
        for entry in self.option_entries:
            entry.delete(0, tk.END)
        self.correct_answer.set('')
    
    def save_question_set(self):
        # Validate set name and questions
        set_name = self.set_name_entry.get().strip()
        
        if not set_name:
            messagebox.showwarning("Warning", "Please enter a name for the question set")
            return
        
        if not self.questions:
            messagebox.showwarning("Warning", "No questions added")
            return
        
        # Ensure question sets directory exists
        if not os.path.exists('question_sets'):
            os.makedirs('question_sets')
        
        # Save to JSON
        filename = os.path.join('question_sets', f"{set_name}.json")
        with open(filename, 'w') as f:
            json.dump(self.questions, f, indent=4)
        
        messagebox.showinfo("Success", f"Question set '{set_name}' saved successfully")
        
        # Refresh parent app's question sets
        self.parent_app.load_existing_question_sets()
        
        # Close window
        self.window.destroy()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
