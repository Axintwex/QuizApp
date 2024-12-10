import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import random
import os
import darkdetect  # For system theme detection

class ModernQuizApp:
    def __init__(self, master):
        # Set up modern styling
        self.master = master
        self.master.title("Smart Quiz")
        self.master.geometry("800x700")
        self.master.resizable(False, False)

        # Detect system theme
        self.theme = self.detect_theme()
        self.configure_style()

        # Quiz data storage
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        
        # Create main frames
        self.setup_frame = ttk.Frame(master, style='Main.TFrame')
        self.quiz_frame = ttk.Frame(master, style='Main.TFrame')
        self.result_frame = ttk.Frame(master, style='Main.TFrame')
        
        # Setup Frame Widgets
        self.setup_frame_widgets()
        self.setup_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    def detect_theme(self):
        """Detect system theme and return appropriate color scheme."""
        return 'dark' if darkdetect.isDark() else 'light'
    
    def configure_style(self):
        """Configure modern styling for the application."""
        style = ttk.Style()
        
        # Define color palette
        if self.theme == 'dark':
            bg_color = '#1E1E1E'
            fg_color = '#FFFFFF'
            accent_color = '#3498DB'
            button_bg = '#2C3E50'
        else:
            bg_color = '#F5F5F5'
            fg_color = '#333333'
            accent_color = '#2980B9'
            button_bg = '#ECF0F1'
        
        # Configure overall style
        style.theme_use('clam')  # Modern base theme
        
        # Main Frame Style
        style.configure('Main.TFrame', background=bg_color)
        
        # Title Style
        style.configure('Title.TLabel', 
                        foreground=fg_color, 
                        background=bg_color, 
                        font=('Segoe UI', 20, 'bold'))
        
        # Button Style
        style.configure('Modern.TButton', 
                        background=button_bg, 
                        foreground=fg_color, 
                        font=('Segoe UI', 12),
                        padding=10)
        style.map('Modern.TButton', 
                  background=[('active', accent_color)],
                  foreground=[('active', 'white')])
        
        # Listbox Style
        style.configure('Modern.TListbox', 
                        background=button_bg, 
                        foreground=fg_color,
                        font=('Segoe UI', 10))
        
        # Entry Style
        style.configure('Modern.TEntry', 
                        font=('Segoe UI', 12),
                        padding=5)
    
    def setup_frame_widgets(self):
        # Clear any existing widgets
        for widget in self.setup_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ttk.Label(self.setup_frame, 
                                text="Smart Quiz", 
                                style='Title.TLabel', 
                                anchor='center')
        title_label.pack(pady=20, fill='x')
        
        # Frame for buttons and listbox
        content_frame = ttk.Frame(self.setup_frame, style='Main.TFrame')
        content_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Button Frame
        button_frame = ttk.Frame(content_frame, style='Main.TFrame')
        button_frame.pack(side='left', padx=10, fill='y')
        
        # Import Questions Button
        import_btn = ttk.Button(button_frame, 
                                text="Import Questions", 
                                style='Modern.TButton', 
                                command=self.import_questions)
        import_btn.pack(pady=10, fill='x')
        
        # Create Questions Button
        create_btn = ttk.Button(button_frame, 
                                text="Create Question Set", 
                                style='Modern.TButton', 
                                command=self.create_question_set)
        create_btn.pack(pady=10, fill='x')
        
        # Existing Question Sets
        sets_label = ttk.Label(content_frame, 
                               text="Existing Question Sets", 
                               style='Title.TLabel')
        sets_label.pack(pady=10)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(content_frame)
        listbox_frame.pack(expand=True, fill='both')
        
        self.question_sets_listbox = tk.Listbox(
            listbox_frame, 
            font=('Segoe UI', 12), 
            selectbackground='#3498DB', 
            selectmode=tk.SINGLE
        )
        self.question_sets_listbox.pack(side='left', expand=True, fill='both')
        
        scrollbar = ttk.Scrollbar(listbox_frame, 
                                  orient='vertical', 
                                  command=self.question_sets_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        
        self.question_sets_listbox.config(yscrollcommand=scrollbar.set)
        
        self.load_existing_question_sets()
        
        # Load Selected Set Button
        load_btn = ttk.Button(content_frame, 
                              text="Load Selected Set", 
                              style='Modern.TButton', 
                              command=self.load_selected_set)
        load_btn.pack(side='bottom', pady=20, fill='x')
    
    def load_existing_question_sets(self):
        # Ensure question_sets directory exists
        if not os.path.exists('question_sets'):
            os.makedirs('question_sets')
        
        # List JSON files
        question_sets = [f for f in os.listdir('question_sets') if f.endswith('.json')]
        
        # Clear existing listbox
        self.question_sets_listbox.delete(0, tk.END)
        
        # Populate listbox
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
        ModernCreateQuestionSetWindow(self.master, self)
    
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
        self.quiz_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    def quiz_frame_widgets(self):
        # Clear previous widgets
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        
        # Current question
        current_q = self.questions[self.current_question_index]
        
        # Question container
        question_container = ttk.Frame(self.quiz_frame, style='Main.TFrame')
        question_container.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Question text
        ttk.Label(question_container, 
                  text=current_q['text'], 
                  wraplength=600, 
                  font=('Segoe UI', 16), 
                  anchor='center').pack(pady=20)
        
        # Variable to store selected option
        self.selected_option = tk.StringVar()
        
        # Options frame
        options_frame = ttk.Frame(question_container, style='Main.TFrame')
        options_frame.pack(expand=True, fill='x', pady=20)
        
        # Options as radio buttons
        for option in current_q['options']:
            option_radio = ttk.Radiobutton(
                options_frame, 
                text=option, 
                variable=self.selected_option, 
                value=option,
                style='Modern.TRadiobutton'
            )
            option_radio.pack(pady=10, fill='x')
        
        # Bottom frame for submit and progress
        bottom_frame = ttk.Frame(question_container, style='Main.TFrame')
        bottom_frame.pack(fill='x', pady=20)
        
        # Submit button
        submit_btn = ttk.Button(
            bottom_frame, 
            text="Submit", 
            style='Modern.TButton', 
            command=self.check_answer
        )
        submit_btn.pack(side='right', padx=10)
        
        # Progress indicator
        progress_label = ttk.Label(
            bottom_frame, 
            text=f"Question {self.current_question_index + 1} of {len(self.questions)}",
            font=('Segoe UI', 12)
        )
        progress_label.pack(side='left', padx=10)
    
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
        
        # Results container
        results_container = ttk.Frame(self.result_frame, style='Main.TFrame')
        results_container.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Title
        ttk.Label(results_container, 
                  text="Quiz Completed!", 
                  style='Title.TLabel', 
                  anchor='center').pack(pady=20)
        
        # Calculate score
        score_percent = (self.score / len(self.questions)) * 100
        
        # Score details
        score_frame = ttk.Frame(results_container, style='Main.TFrame')
        score_frame.pack(expand=True, fill='x', pady=20)
        
        ttk.Label(score_frame, 
                  text=f"Your Score: {self.score} / {len(self.questions)}", 
                  font=('Segoe UI', 16)).pack()
        
        ttk.Label(score_frame, 
                  text=f"Percentage: {score_percent:.2f}%", 
                  font=('Segoe UI', 14)).pack(pady=10)
        
        # Performance message
        if score_percent >= 90:
            performance_msg = "Excellent Performance! 🏆"
            msg_color = 'green'
        elif score_percent >= 75:
            performance_msg = "Great Job! 👍"
            msg_color = 'blue'
        elif score_percent >= 60:
            performance_msg = "Good Performance 👏"
            msg_color = 'orange'
        else:
            performance_msg = "Keep Practicing 📚"
            msg_color = 'red'
        
        ttk.Label(score_frame, 
                  text=performance_msg, 
                  font=('Segoe UI', 14, 'bold'),
                  foreground=msg_color).pack(pady=10)
        
        # Restart Quiz Button
        restart_btn = ttk.Button(
            results_container, 
            text="Restart Quiz", 
            style='Modern.TButton', 
            command=self.restart_quiz
        )
        restart_btn.pack(pady=20)
        
        # Show result frame
        self.result_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    def restart_quiz(self):
        # Hide result frame
        self.result_frame.pack_forget()
        
        # Show setup frame
        self.setup_frame.pack(expand=True, fill='both', padx=20, pady=20)

class ModernCreateQuestionSetWindow:
    def __init__(self, master, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel(master)
        self.window.title("Create Question Set")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # Configure style similar to main app
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color scheme
        bg_color = '#F5F5F5'
        fg_color = '#333333'
        accent_color = '#2980B9'
        
        # Questions list
        self.questions = []
        
        # Main
