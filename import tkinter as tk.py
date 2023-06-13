import tkinter as tk
from tkinter import messagebox

class Question:
    def __init__(self, question_text, options, correct_answer):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("400x300")
        self.current_user = None
        self.questions = []
        self.student_responses = []
        self.current_question_index = 0

        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)
        self.quiz_frame = tk.Frame(self)

        self.create_account()

    def create_account(self):
        self.login_frame.destroy()
        self.login_frame = tk.Frame(self)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.account_type_var = tk.StringVar()
        self.account_type_var.set("Student")

        self.account_type_label = tk.Label(self.login_frame, text="Account Type:")
        self.account_type_label.pack()
        self.student_radio_btn = tk.Radiobutton(self.login_frame, text="Student", variable=self.account_type_var, value="Student")
        self.student_radio_btn.pack()
        self.teacher_radio_btn = tk.Radiobutton(self.login_frame, text="Teacher", variable=self.account_type_var, value="Teacher")
        self.teacher_radio_btn.pack()

        self.login_btn = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_btn.pack(pady=10)

        self.create_account_btn = tk.Button(self.login_frame, text="Create Account", command=self.save_account)
        self.create_account_btn.pack(pady=10)

        self.login_frame.pack()

    def save_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        account_type = self.account_type_var.get()

        if username and password:
            # Save the account details here (e.g., in a database)
            messagebox.showinfo("Account Creation", "Account created successfully!")
            self.current_user = account_type

            if self.current_user == "Teacher":
                self.show_teacher_panel()
            else:
                self.show_student_panel()

        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        account_type = self.account_type_var.get()

        # Perform login authentication here (e.g., check username and password from database)
        # You can customize the login logic as per your requirements

        if username and password:
            messagebox.showinfo("Login", "Login successful!")
            self.current_user = account_type

            if self.current_user == "Teacher":
                self.show_teacher_panel()
            else:
                self.show_student_panel()

        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def show_teacher_panel(self):
        self.login_frame.destroy()
        self.quiz_frame = tk.Frame(self)

        self.add_question_btn = tk.Button(self.quiz_frame, text="Add Question", command=self.add_question)
        self.add_question_btn.pack(pady=10)

        self.logout_btn = tk.Button(self.quiz_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=10)

        self.quiz_frame.pack()

    def show_student_panel(self):
        self.login_frame.destroy()
        self.quiz_frame = tk.Frame(self)

        self.take_quiz_btn = tk.Button(self.quiz_frame, text="Take Quiz", command=self.take_quiz)
        self.take_quiz_btn.pack(pady=10)

        self.logout_btn = tk.Button(self.quiz_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=10)

        self.quiz_frame.pack()

    def add_question(self):
        question_window = tk.Toplevel(self)
        question_window.title("Add Question")
        question_window.geometry("400x300")

        question_label = tk.Label(question_window, text="Question:")
        question_label.pack()
        question_entry = tk.Entry(question_window)
        question_entry.pack()

        option_labels = []
        option_entries = []
        for i in range(4):
            option_label = tk.Label(question_window, text=f"Option {i+1}:")
            option_label.pack()
            option_labels.append(option_label)
            option_entry = tk.Entry(question_window)
            option_entry.pack()
            option_entries.append(option_entry)

        answer_label = tk.Label(question_window, text="Correct Answer (1-4):")
        answer_label.pack()
        answer_entry = tk.Entry(question_window)
        answer_entry.pack()

        save_question_btn = tk.Button(question_window, text="Save", command=lambda: self.save_question(question_entry.get(), [entry.get() for entry in option_entries], answer_entry.get()))
        save_question_btn.pack(pady=10)

    def save_question(self, question_text, options, correct_answer):
        if question_text and options and correct_answer:
            question = Question(question_text, options, correct_answer)
            self.questions.append(question)
            messagebox.showinfo("Question Saved", "Question saved successfully!")
        else:
            messagebox.showerror("Error", "Please enter question, options, and correct answer.")

    def take_quiz(self):
        if not self.questions:
            messagebox.showerror("Error", "No questions available.")
            return

        self.quiz_frame.destroy()
        self.quiz_frame = tk.Frame(self)

        question_label = tk.Label(self.quiz_frame, text=self.questions[self.current_question_index].question_text)
        question_label.pack()

        option_var = tk.IntVar()
        option_var.set(-1)

        option_radio_buttons = []
        for i, option in enumerate(self.questions[self.current_question_index].options):
            option_radio_btn = tk.Radiobutton(self.quiz_frame, text=option, variable=option_var, value=i)
            option_radio_btn.pack()
            option_radio_buttons.append(option_radio_btn)

        submit_btn = tk.Button(self.quiz_frame, text="Submit", command=lambda: self.check_answer(option_var.get()))
        submit_btn.pack(pady=10)

        self.quiz_frame.pack()

    def check_answer(self, selected_option):
        if selected_option == -1:
            messagebox.showerror("Error", "Please select an option.")
            return

        selected_question = self.questions[self.current_question_index]
        correct_answer = int(selected_question.correct_answer) - 1

        self.student_responses.append((selected_question.question_text, selected_option, correct_answer))

        if selected_option == correct_answer:
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", "Your answer is incorrect.")

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.take_quiz()
        else:
            self.show_scoreboard()

    def show_scoreboard(self):
        self.quiz_frame.destroy()
        self.quiz_frame = tk.Frame(self)

        total_questions = len(self.questions)
        correct_answers = sum([1 for response in self.student_responses if response[1] == response[2]])
        incorrect_answers = total_questions - correct_answers

        score_label = tk.Label(self.quiz_frame, text="Scoreboard")
        score_label.pack()

        correct_label = tk.Label(self.quiz_frame, text=f"Correct Answers: {correct_answers}/{total_questions}")
        correct_label.pack()

        incorrect_label = tk.Label(self.quiz_frame, text=f"Incorrect Answers: {incorrect_answers}/{total_questions}")
        incorrect_label.pack()

        self.logout_btn = tk.Button(self.quiz_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=10)

        self.quiz_frame.pack()

    def logout(self):
        self.quiz_frame.destroy()
        self.create_account()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.start()
